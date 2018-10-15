#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from time import localtime, strftime
import array
import os
import math
from glob import glob
import gtk
import gobject
import os.path
from string import rstrip
import sys

from config import *
# User either mcp3002 or mcp3008 (they work slightly differently)
from mcp3002 import *

class BatteryMonitor:
    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.connect('activate', self.refresh)

        # Create menu
        menu = gtk.Menu()
        i = gtk.MenuItem("About...")
        i.show()
        i.connect("activate", self.show_about)
        menu.append(i)
        i = gtk.MenuItem("Quit")
        i.show()
        i.connect("activate", self.quit)
        menu.append(i)
        self.tray.connect('popup-menu', self.show_menu, menu)

        # Initialize and start battery display
        self.refresh(None)
        self.tray.set_visible(True)
        gobject.timeout_add(REFRESH_RATE * 1000, self.refresh, False)

    def show_menu(self, widget, event_button, event_time, menu):
        menu.popup(None, None,
            gtk.status_icon_position_menu,
            event_button,
            event_time,
            self.tray
        )

    def show_about(self, widget):
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            """
Battery Monitor for the MCP3002/MCP3008
By Melissa LeBlanc-Williams
""")
        dialog.run()
        dialog.destroy()

    def quit(self, widget):
        gtk.main_quit()

    def refresh(self, widget):
        def slurp(filename):
            f = open(filename)
            return f.read()
        b_volts = self.readVoltage(None)
        b_level = int(round(float(b_volts - VOLTAGE_EMPTY) / float(VOLTAGE_FULL - VOLTAGE_EMPTY) * 100))
        # Make sure these are in the range of 0-100%
        if b_level > 100:
            b_level = 100
        if b_level < 0:
            b_level = 0;
        b_file = ICONPATH + "." + str(b_level / 10) + ".png"
        self.tray.set_tooltip(
            "Battery Level: %d%% (%.2f Volts)" %
            (b_level, b_volts)
        )
        if os.path.exists(b_file):
            self.tray.set_from_file(b_file)
        self.tray.set_blinking(b_level <= 5)
        return True

    def readVoltage(self, widget):
        # Read value 3 times
        ret1 = readadc(ADCCHANNEL, SPICLK, SPIMOSI, SPIMISO, SPICS)
        ret2 = readadc(ADCCHANNEL, SPICLK, SPIMOSI, SPIMISO, SPICS)
        ret3 = readadc(ADCCHANNEL, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # Determine the average
        ret = (ret1 + ret2 + ret3) / 3
        # Calculate the Voltage
        return ((HIGHRESVAL + LOWRESVAL) * ret * (ADCVREF / 1024)) / HIGHRESVAL


###############################################################################
if __name__ == '__main__':
    app = BatteryMonitor()
    gtk.main()