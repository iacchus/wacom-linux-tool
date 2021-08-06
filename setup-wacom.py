#!/usr/bin/env python

# https://plumbum.readthedocs.io/en/latest
from plumbum import local

COMMANDS = {
    "list_devices": ("--list", "devices"),
    "get_option": lambda option: ("--get", option),
    "set_option": lambda option, value: ("--set", option, value)
}

class Device:
    def __init__(self, name, id, dev_type):
        self.name = name
        self.id = id
        self.dev_type = dev_type

    def get(self, option):
        """Gets a parameter from the device's atual configuration"""
        command = COMMANDS["get_option"](option)
        return XSETWACOM.run(command)

    def set(self, option, value):
        """Sets a parameter to the device's atual configuration"""
        command = COMMANDS["set_option"](option, value)
        return XSETWACOM.run(command)

    def __str__(self):
        return f"name: {self.name} id: {self.id} type: {self.dev_type}"

    def __repr__(self):
        return f"<Device '{self.name}' (id {self.id})>"

def get_devices():

    devices_dict = dict()

    # output example:
    # >>> xsetwacom["--list", "devices"]()
    # 'Wacom Intuos S Pad pad          \tid: 18\ttype: PAD       \nWacom Intuos S Pen stylus       \tid: 19\ttype: STYLUS    \nWacom Intuos S Pen eraser       \tid: 20\ttype: ERASER    \n'
    command = COMMANDS["list_devices"]
    output = XSETWACOM.run(command)
    print(output)

    for device in output. \
            strip(). \
            splitlines():

        raw_output = device.split("\t")
        name = raw_output[0].strip()
        id = raw_output[1].split(" ")[-1].strip()
        dev_type = raw_output[2].strip().split(" ")[-1]

        devices_dict.update({name: Device(name=name, id=id, dev_type=dev_type)})

    return devices_dict


XSETWACOM = local["xsetwacom"]

pad = "Wacom Intuos S Pad pad"
stylus = "Wacom Intuos S Pen stylus"
eraser = "Wacom Intuos S Pen eraser"

DEVICES = get_devices()

#mode_relative = XSETWACOM["--set", stylus, "Mode", "Relative"]
#mode_absolute = XSETWACOM["--set", stylus, "Mode", "Absolute"]

DEVICES[stylus].set(option="Mode", value="Absolute")

if __name__ == "__main__":

    print(get_devices())
    pass
