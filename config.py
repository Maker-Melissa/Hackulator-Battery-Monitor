"""
" Edit below this line to fit your needs
"""
# Path to icons
ICONPATH = "/home/pi/batterymonitor/images/battery"

# Fully charged voltage, voltage at the percentage steps and shutdown voltage. This is where you edit when finetuning the batterymonitor
# by using the monitor.py script.
VOLTAGE_FULL = 4.15
VOLTAGE_EMPTY = 3.2

# Value (in ohms) of the lower resistor from the voltage divider, connected to the ground line (1 if no voltage divider). 
# Default value (2000) is for a lipo battery, stepped down to about 3.2V max.
LOWRESVAL = 2000

# Value (in ohms) of the higher resistor from the voltage divider, connected to the positive line (0 if no voltage divider).
# Default value (6800) is for a lipo battery, stepped down to about 3.2V max.
HIGHRESVAL = 6800

# ADC voltage reference (3.3V for Raspberry Pi)
ADCVREF = 3.3

# MCP3002/MCP3008 channel to use (from 0 to 7)
ADCCHANNEL = 0

# Refresh rate (seconds)
REFRESH_RATE = 15

# Voltage value measured by the MCP3002/MCP3008 when batteries are fully charged. It should be near 3.3V due to Raspberry Pi GPIO compatibility)
# Be careful to edit below this line.
SVOLTAGE_FULL = (VOLTAGE_FULL) * (HIGHRESVAL) / (LOWRESVAL+HIGHRESVAL)
SVOLTAGE_EMPTY = (VOLTAGE_EMPTY) * (HIGHRESVAL) / (LOWRESVAL+HIGHRESVAL)

# MCP3002/MCP3008 scaling
ADC_FULL = SVOLTAGE_FULL / (ADCVREF / 1024.0)
ADC_EMPTY = SVOLTAGE_EMPTY / (ADCVREF / 1024.0)
