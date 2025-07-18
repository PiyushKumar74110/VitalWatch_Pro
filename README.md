# VitalWatch Pro - Status Dashboard

VitalWatch Pro is a real-time health and safety monitoring dashboard built with PyQt5, designed to interface with an Arduino via serial communication. It provides visual feedback and logging for various sensors including temperature, humidity, flame, sound, shock, and more.

## Project Overview

This application provides a user-friendly interface for monitoring sensor data in real-time. It is ideal for use in:
- Patient monitoring rooms
- Elderly care environments

Data is received from an Arduino device over a serial port, parsed, displayed in a PyQt5 GUI, and logged into a CSV file for future reference.

## Features

- Real-time sensor value display
- Visual status indicators (Normal / Warning / Critical)
- Auto-detection and reconnection of Arduino
- Sensor data logging in CSV format (`vital_log.csv`)
- Live timestamp and last-data-received tracking
- Built-in serial monitor view

## Sensors Monitored

| Sensor     | Label    | Purpose |
|------------|----------|---------|
| TEMP       | Temperature | Detects environment temperature |
| HUM        | Humidity | Measures air moisture (for comfort/health insights) |
| FLAME      | Flame Sensor | Detects fire or sudden heat sources |
| LIGHT      | Light Sensor | Measures ambient light levels |
| SOUND      | Sound Sensor | Detects abnormal or loud noise levels |
| SHOCK      | Vibration/Shock | Identifies impact or vibration events |
| BALL       | Tilt/Ball | Detects orientation or tilting movement |
| REED       | Reed Switch | Detects door/window opening (magnetic trigger) |
| TOUCH      | Touch Sensor | Senses physical interaction or surface contact |

### Prerequisites

- Python 3.x
- PyQt5
- pyserial

### Install Dependencies
pip install pyqt5 pyserial

