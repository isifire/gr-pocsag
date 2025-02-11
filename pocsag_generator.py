import numpy as np
from gnuradio import gr
from bitstring import BitArray
import time

class PocsagSender(gr.sync_block):
    def __CalculateCRCandParity(self, datatype, data):
        cw = data << 11

        if datatype == 1:
            cw |= 0x80000000

        local_cw = cw
        
        for _ in range(21):
            if (cw & 0x80000000) > 0:
                cw ^= 0xED200000
            cw <<= 1

        local_cw |= (cw >> 21)

        parity = sum(1 for _ in range(32) if (local_cw << _) & 0x80000000)
        local_cw += (parity % 2)

        return local_cw

    def __createpocsagmsg(self, address, source, txt):
        if not (0 < address <= 0x1FFFFF):
            raise ValueError("Invalid address")
        if not (0 <= source <= 3):
            raise ValueError("Invalid source")
        if len(txt) == 0:
            raise ValueError("Text cannot be empty")

        syncpattern = 0xAAAAAAAA
        synccodeword = 0x7CD215D8
        idlepattern = 0x7AC9C197

        codeword = [idlepattern] * 32
        addressline = (address >> 3) << 2 | source
        cwnum = (address % 8) << 1
        codeword[cwnum] = self.__CalculateCRCandParity(0, addressline)
        
        ts = [ord(c) for c in txt] + [0x04]
        ts = [x % 128 for x in ts]
        textbits = ''.join(BitArray(uint=c, length=7).bin[::-1] for c in ts)

        bitstoadd = (20 - len(textbits) % 20) % 20
        textbits += '01' * (bitstoadd // 2) + ('0' if bitstoadd % 2 else '')
        
        ncw = len(textbits) // 20
        startbit, stopbit = 0, 20

        for i in range(int(ncw)):
            thiscw = int(textbits[startbit:stopbit], 2)
            startbit, stopbit = stopbit, stopbit + 20
            cwnum += 1
            codeword[cwnum] = self.__CalculateCRCandParity(1, thiscw)

        ret = [syncpattern] * 18 + [synccodeword] + codeword[:16]
        if cwnum >= 16:
            ret.append(synccodeword)
            ret += codeword[16:32]
            nbatch = 2
        else:
            nbatch = 1

        return nbatch, ret

    def __init__(self, number=2060073, source=0, sleeptime=5, text="ON1ARF pocsag Python gnuradio"):
        gr.sync_block.__init__(
            self,
            name='pocsag generator',
            in_sig=[],
            out_sig=[np.int8]
        )

        self.set_output_multiple(640)
        self.state = 0
        self.sleeptime = sleeptime
        self.number = int(number)
        self.source = int(source)

        nbatch, psmsg = self.__createpocsagmsg(number, source, text)
        self.pocsagmsg = [0] * (20 if nbatch == 1 else 32)

        for thismsg in psmsg:
            self.pocsagmsg.extend([1 if c == '1' else -1 for c in BitArray(uint=thismsg, length=32).bin])

        self.pocsagmsg.extend([0] * (20 if nbatch == 1 else 32))
        self.msglen = len(self.pocsagmsg)

    def work(self, input_items, output_items):
        if self.state == 0:
            output_items[0][:self.msglen] = np.array(self.pocsagmsg, dtype=np.int8)
            self.state = 1
            return self.msglen
        self.state = 0
        return -1
