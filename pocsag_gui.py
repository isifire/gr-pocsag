import sys
import subprocess

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
)

class PocsagGui(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("POCSAG Sender via HackRF")
        self.setGeometry(200, 200, 500, 400)

        # Labels y campos de entrada
        self.ric_label = QLabel("RIC:")
        self.ric_input = QLineEdit()
        self.ric_input.setText("1107305")  # Establecer valor por defecto
        self.ric_input.setPlaceholderText("Ejemplo: 1122551")

        self.subric_label = QLabel("SubRIC:")
        self.subric_input = QLineEdit()
        self.subric_input.setText("0")
        self.subric_input.setPlaceholderText("Ejemplo: 0")

        self.text_label = QLabel("Mensaje:")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Ejemplo: Hola Mundo")

        self.freq_label = QLabel("Frecuencia (MHz):")
        self.freq_input = QLineEdit()
        self.freq_input.setText("148.625")
        self.freq_input.setPlaceholderText("Ejemplo: 148.625")

        self.bitrate_label = QLabel("Bitrate POCSAG (bps):")
        self.bitrate_input = QLineEdit()
        self.bitrate_input.setText("2400")
        self.bitrate_input.setPlaceholderText("Ejemplo: 2400")

        # Botón de envío
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_pocsag)

        # Consola de salida
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)

        # Layout principal
        layout = QVBoxLayout()

        layout.addWidget(self.ric_label)
        layout.addWidget(self.ric_input)

        layout.addWidget(self.subric_label)
        layout.addWidget(self.subric_input)

        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input)

        layout.addWidget(self.freq_label)
        layout.addWidget(self.freq_input)

        layout.addWidget(self.bitrate_label)
        layout.addWidget(self.bitrate_input)

        layout.addWidget(self.send_button)
        layout.addWidget(self.output_console)

        self.setLayout(layout)

    def send_pocsag(self):
        ric = self.ric_input.text().strip()
        subric = self.subric_input.text().strip()
        text = self.text_input.text().strip() + " "  # Añadir un espacio al final


        freq = self.freq_input.text().strip()
        bitrate = self.bitrate_input.text().strip()

        if not all([ric, subric, text, freq, bitrate]):
            self.output_console.append("⚠️ Todos los campos son obligatorios.")
            return

        try:
            freq_hz = int(float(freq) * 1_000_000)  # Convertir MHz a Hz
            cmd = [
                "./pocsag_sender.py",
                "--RIC", ric,
                "--SubRIC", subric,
                "--Text", text,
                "--pagerfreq", str(freq_hz),
                "--pocsagbitrate", bitrate
            ]

            self.output_console.append(f"⏳ Enviando mensaje...\n{' '.join(cmd)}\n")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout, stderr = process.communicate()

            if stdout:
                self.output_console.append(f"✅ Salida:\n{stdout}")
            if stderr:
                self.output_console.append(f"❌ Error:\n{stderr}")

        except ValueError:
            self.output_console.append("⚠️ La frecuencia debe ser un número válido en MHz.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PocsagGui()
    window.show()
    sys.exit(app.exec())
