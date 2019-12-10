# Midnite_NMEA

Hardware:
Raspberry Pi Zero + BMP280 + HP33A

Software:
Raspbian (read only) + Python3

3 Python components

1) NmeaCommunicator - Python program to recieve NMEA strings from all connected devices on port 2010 and send to all connected devices on port 2000

2) NmeaBMP280 - Python program to receive Pressure and Tempreture from the bosch BMP280, convert it to NMEA and send it to port NmeaCommunicator on port 2010

3) NmeaHP33A - Python program to receive NMEA strings from the HP33A and send it to the NmeaCommunicator on port 2010.


Goals:
1) Build a reliable ships computer providing a wifi access point which draws little power, collects NMEA strings and distrabutes to all connected devices on port 2000.
2) Imporve Python, Ansible and Git skills.
