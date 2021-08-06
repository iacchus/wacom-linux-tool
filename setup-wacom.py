#!/usr/bin/env python

# https://plumbum.readthedocs.io/en/latest
from plumbum import local

xsetwacom = local["xsetwacom"]
XSETWACOM = local["xsetwacom"]

pad = "Wacom Intuos S Pad pad"
stylus = "Wacom Intuos S Pen stylus"
eraser = "Wacom Intuos S Pen eraser"

def get_devices():

    device_list = list()

    # >>> xsetwacom["--list", "devices"]()
    # 'Wacom Intuos S Pad pad          \tid: 18\ttype: PAD       \nWacom Intuos S Pen stylus       \tid: 19\ttype: STYLUS    \nWacom Intuos S Pen eraser       \tid: 20\ttype: ERASER    \n'
    output = xsetwacom["--list", "devices"]()

    for device in output. \
                      strip().\
                      splitlines():

        raw_output = device.split("\t")
        name = raw_output[0].strip()
        id = raw_output[1].split(" ")[-1].strip()
        dev_type = raw_output[2].strip().split(" ")[-1]

        device_list.append(Device(name=name, id=id, dev_type=dev_type))

    return device_list

class Device:
    def __init__(self, name, id, dev_type):
        self.name = name
        self.id = id
        self.dev_type = dev_type

    def get_option(self, option):
        command = COMMANDS["get_option"](option)
        return XSETWACOM.run(command)

    def set_option(self, option, value):
        command = COMMANDS["set_option"](option, value)
        return XSETWACOM.run(command)

    def __str__(self):
        return f"name: {self.name} id: {self.id} type: {self.dev_type}"

    def __repr__(self):
        return f"<Device '{self.name}' (id {self.id})>"


DEVICES = get_devices()

COMMANDS = {
    "get_option": lambda option: ("--get", option),
    "set_option": lambda option, value: ("--set", option, value)
}
mode_relative = xsetwacom["--set", stylus, "Mode", "Relative"]
mode_absolute = xsetwacom["--set", stylus, "Mode", "Absolute"]

if __name__ == "__main__":

    print(get_devices())
    pass