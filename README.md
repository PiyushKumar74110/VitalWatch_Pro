# VitalWatch Pro - Smart Status Monitor 

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
| TEMP       | Temperature | Detects body/environment temperature |
| HUM        | Humidity | Measures air moisture (for comfort/health insights) |
| FLAME      | Flame Sensor | Detects presence of fire |
| LIGHT      | Light Sensor | Detects ambient brightness |
| SOUND      | Sound Sensor | Detects loud noise (shouting, alarms) |
| SHOCK      | Vibration/Shock | Detects physical impacts or tremors |
| BALL       | Tilt/Ball | Detects device orientation/movement |
| REED       | Reed Switch | Detects door/window open state |
| TOUCH      | Touch Sensor | Detects surface touch |

### Prerequisites

- Python 3.x
- PyQt5
- pyserial

### Install Dependencies
pip install pyqt5 pyserial

