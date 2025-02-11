#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: POCSAG Sender via HackRF
# Author: ON1ARF & Tauebenuss
# Description: Sending Pocsag Messages via HACKRF One
##################################################

import math
import time
import argparse
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes, pfb
import osmosdr
import pocsag_generator

class PocsagSender(gr.top_block):
    def __init__(self, RIC=1122551, SubRIC=0, Text='Testmessage by HACRF One', pagerfreq=148625000, pocsagbitrate=2400):
        super().__init__("POCSAG Sender via HackRF")
        
        self.RIC = RIC
        self.SubRIC = SubRIC
        self.Text = Text
        self.pagerfreq = pagerfreq
        self.pocsagbitrate = pocsagbitrate

        self.tx_gain = 3
        self.symrate = 38400
        self.samp_rate = 12000000
        self.max_deviation = 4500.0
        self.af_gain = 190

        self.pocsag_generator = pocsag_generator.PocsagSender(
            number=RIC, source=SubRIC, sleeptime=5, text=Text
        )
        
        self.pfb_arb_resampler = pfb.arb_resampler_ccf(
            float(self.samp_rate) / float(self.symrate), taps=None, flt_size=16
        )
        self.pfb_arb_resampler.declare_sample_delay(0)

        self.osmosdr_sink = osmosdr.sink(args="numchan=1 hackrf")
        self.osmosdr_sink.set_sample_rate(self.samp_rate)
        self.osmosdr_sink.set_center_freq(self.pagerfreq, 0)
        self.osmosdr_sink.set_freq_corr(0, 0)
        self.osmosdr_sink.set_gain(0, 0)
        self.osmosdr_sink.set_if_gain(self.tx_gain, 0)
        self.osmosdr_sink.set_bb_gain(20, 0)
        self.osmosdr_sink.set_antenna('', 0)
        self.osmosdr_sink.set_bandwidth(0, 0)

        self.blocks_repeat = blocks.repeat(gr.sizeof_char, self.symrate // self.pocsagbitrate)
        self.blocks_multiply_const = blocks.multiply_const_vcc((self.af_gain / 100,))
        self.blocks_char_to_float = blocks.char_to_float(1, self.af_gain * 0.7 / 1000)
        self.analog_frequency_modulator = analog.frequency_modulator_fc(
            2.0 * math.pi * self.max_deviation / float(self.symrate)
        )
        
        self.connect(self.pocsag_generator, self.blocks_repeat)
        self.connect(self.blocks_repeat, self.blocks_char_to_float)
        self.connect(self.blocks_char_to_float, self.analog_frequency_modulator)
        self.connect(self.analog_frequency_modulator, self.blocks_multiply_const)
        self.connect(self.blocks_multiply_const, self.pfb_arb_resampler)
        self.connect(self.pfb_arb_resampler, self.osmosdr_sink)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Sending Pocsag Messages via HACKRF One')
    parser.add_argument('--RIC', type=int, default=1122551, help='Set RIC (default: 1122551)')
    parser.add_argument('--SubRIC', type=int, default=0, help='Set SubRIC (default: 0)')
    parser.add_argument('--Text', type=str, default='Testmessage by HACRF One', help='Set message text')
    parser.add_argument('--pagerfreq', type=int, default=148625000, help='Set transmission frequency (default: 148625000 Hz)')
    parser.add_argument('--pocsagbitrate', type=int, default=2400, help='Set POCSAG bitrate (default: 2400 bps)')
    return parser.parse_args()


def main():
    args = parse_arguments()
    tb = PocsagSender(RIC=args.RIC, SubRIC=args.SubRIC, Text=args.Text, pagerfreq=args.pagerfreq, pocsagbitrate=args.pocsagbitrate)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
