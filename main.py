import sys
import csv
import time
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QTextEdit
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QTimer, QDateTime

BAUD_RATE = 9600

class VitalWatchGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VitalWatch Pro - Smart Status Monitor")
        self.setGeometry(200, 100, 460, 860)

        self.sensor_labels = {}
        self.status_labels = {}

        self.csv_file = open("vital_log.csv", mode="a", newline="", encoding="utf-8")
        self.csv_writer = csv.writer(self.csv_file)

        self.serial = None
        self.last_received = QDateTime.currentDateTime()
        self.try_connect_serial()

        self.set_gradient_background()
        self.init_ui()

        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.update_data)
        self.data_timer.start(1000)

        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)

    def try_connect_serial(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino" in port.description or "USB-SERIAL" in port.description or "CH340" in port.description:
                try:
                    self.serial = serial.Serial(port.device, BAUD_RATE, timeout=1)
                    print(f"Connected to {port.device}")
                    time.sleep(2)
                    return
                except Exception as e:
                    print(f"Failed to open {port.device}: {e}")
        self.serial = None

    def set_gradient_background(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0a0f1f"))   
        gradient.setColorAt(0.5, QColor("#12233f"))   
        gradient.setColorAt(1.0, QColor("#1c2c4a"))   
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)

        title = QLabel("VitalWatch Pro\nStatus Dashboard")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        self.layout.addWidget(title)

        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont("Consolas", 12))
        self.datetime_label.setAlignment(Qt.AlignCenter)
        self.datetime_label.setStyleSheet("color: #bbb;")
        self.layout.addWidget(self.datetime_label)

        self.connection_status = QLabel()
        self.connection_status.setFont(QFont("Arial", 12, QFont.Bold))
        self.connection_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.connection_status)

        self.last_data_label = QLabel("Last data: N/A")
        self.last_data_label.setFont(QFont("Consolas", 10))
        self.last_data_label.setStyleSheet("color: #aaa;")
        self.last_data_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.last_data_label)

        self.sensors = [
            "TEMP", "HUM", "FLAME", "LIGHT",
            "SOUND", "SHOCK", "BALL", "REED", "TOUCH"
        ]

        for name in self.sensors:
            self.layout.addLayout(self.create_sensor_row(name))
            self.layout.addWidget(self.create_separator())

        self.serial_monitor = QTextEdit()
        self.serial_monitor.setReadOnly(True)
        self.serial_monitor.setMaximumHeight(150)
        self.serial_monitor.setStyleSheet("background-color: #111; color: #0f0; font-family: Consolas;")
        self.layout.addWidget(self.serial_monitor)

        self.setLayout(self.layout)

    def create_sensor_row(self, name):
        row = QHBoxLayout()

        label = QLabel(name)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("color: white;")

        value_label = QLabel("N/A")
        value_label.setFont(QFont("Arial", 13))
        value_label.setStyleSheet("""
            background-color: #1e3c59;
            padding: 6px 12px;
            border-radius: 10px;
            color: white;
        """)

        status_label = QLabel("Unknown")
        status_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_label.setStyleSheet("color: gray;")

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value_label)
        row.addWidget(status_label)

        self.sensor_labels[name] = value_label
        self.status_labels[name] = status_label

        return row

    def create_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: white;")
        return line

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.datetime_label.setText(current.toString("dddd, dd MMMM yyyy - hh:mm:ss AP"))

    def update_data(self):
        
        if self.serial is None or not self.serial.is_open:
            self.try_connect_serial()

        if self.serial and self.serial.is_open:
            self.show_connection_status("✅ Arduino Connected", "#2ecc71")
            try:
                while self.serial.in_waiting:
                    line = self.serial.readline().decode('utf-8').strip()
                    if line:
                        self.serial_monitor.append(line)
                        self.process_line(line)
                        self.last_received = QDateTime.currentDateTime()
                        self.last_data_label.setText("Last data: " + self.last_received.toString("hh:mm:ss"))
            except Exception as e:
                print("Serial error:", e)
                try:
                    self.serial.close()
                except:
                    pass
                self.serial = None
        else:
            self.show_connection_status("❌ Arduino Disconnected", "#e74c3c")

    def process_line(self, line):
        parts = line.split(",")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        csv_row = [timestamp]

        for part in parts:
            if ":" in part:
                key, val = part.split(":", 1)
                key = key.strip()
                val = val.strip()
                if key in self.sensor_labels:
                    self.sensor_labels[key].setText(val)
                    self.update_status_label(key, val)
                csv_row.append(f"{key}:{val}")

        self.csv_writer.writerow(csv_row)
        self.csv_file.flush()

    def update_status_label(self, key, value):
        label = self.status_labels.get(key)
        if not label:
            return

        status, color = self.evaluate_status(key, value)
        label.setText(status)
        label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def evaluate_status(self, key, value):
        try:
            if key == "TEMP":
                temp = float(value.replace("°C", "").strip())
                if temp > 38:
                    return "Critical", "red"
                elif temp > 35:
                    return "Warning", "orange"
                else:
                    return "Normal", "lime"
            elif key == "FLAME":
                return ("Critical", "red") if value.lower()=="fire detected" else ("Normal", "lime")
            elif key == "SHOCK":
                return ("Warning", "orange") if value.lower()=="impact" else ("Normal", "lime")
            elif key == "BALL":
                return ("Warning", "orange") if value.lower()=="active" else ("Normal", "lime")
            elif key == "SOUND":
                return ("Warning", "orange") if value.lower()=="loud" else ("Normal", "lime")
            elif key == "REED":
                return ("Warning", "orange") if value.lower()=="open" else ("Normal", "lime")
            elif key == "TOUCH":
                return ("Warning", "orange") if value.lower()=="touched" else ("Normal", "lime")
            elif key == "HUM":
                return "Normal", "lime"
            else:
                return "Normal", "lime"
        except:
            return "Unknown", "gray"

    def show_connection_status(self, text, color):
        self.connection_status.setText(text)
        self.connection_status.setStyleSheet(f"color: {color};")

    def closeEvent(self, event):
        if self.serial:
            self.serial.close()
        self.csv_file.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VitalWatchGUI()
    window.show()
    sys.exit(app.exec_())
