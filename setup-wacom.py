#!/usr/bin/env python

# https://plumbum.readthedocs.io/en/latest
from plumbum import local

xsetwacom = local["xsetwacom"]

pad = "Wacom Intuos S Pad pad"
stylus = "Wacom Intuos S Pen stylus"
eraser = "Wacom Intuos S Pen eraser"

def get_devices()
class Device:
    def __init__(self):
        pass

mode_relative = xsetwacom["--set", stylus, "Mode", "Relative"]
mode_absolute = xsetwacom["--set", stylus, "Mode", "Absolute"]

if __name__ == "__main__":