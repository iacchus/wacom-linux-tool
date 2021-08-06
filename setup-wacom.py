#!/usr/bin/env python

# https://plumbum.readthedocs.io/en/latest
from plumbum import local

XSETWACOM = local["xsetwacom"]

COMMANDS = {
    "list_devices": ("--list", "devices"),
    "get_option": lambda device, option: ("--get", device, option),
    "set_option": lambda device, option, value: ("--set", device, option,
                                                 value)
}

# plumbum's LocalCommand.run() -> (exit_code, stdout, stderr,)
EXIT_CODE = 0
STDOUT = 1
STDERR = 2

class Device:
    def __init__(self, name, id, dev_type):
        self.name = name
        self.id = id
        self.dev_type = dev_type

    def get(self, option):
        """Gets a parameter from the device's atual configuration"""
        command = COMMANDS["get_option"](self.name, option)
        return XSETWACOM.run(command)

    def set(self, option, value):
        """Sets a parameter to the device's atual configuration"""
        command = COMMANDS["set_option"](self.name, option, value)
        return XSETWACOM.run(command)

    def __str__(self):
        return f"name: {self.name} id: {self.id} type: {self.dev_type}"

    def __repr__(self):
        return f"<Device '{self.name}' (id {self.id})>"

def get_devices():

    devices_dict = dict()

    # output example:
    #
    # >>> xsetwacom["--list", "devices"]()
    # 'Wacom Intuos S Pad pad          \tid: 18\ttype: PAD       \nWacom Intuo\
    # s S Pen stylus       \tid: 19\ttype: STYLUS    \nWacom Intuos S Pen eras\
    # er       \tid: 20\ttype: ERASER    \n'
    #
    command = COMMANDS["list_devices"]
    output = XSETWACOM.run(command)[STDOUT]

    for device in output. \
            strip(). \
            splitlines():

        raw_output = device.split("\t")
        name = raw_output[0].strip()
        id = raw_output[1].split(" ")[-1].strip()
        dev_type = raw_output[2].strip().split(" ")[-1]

        devices_dict.update({name: Device(name=name, id=id, dev_type=dev_type)})

    return devices_dict

DEVICES = get_devices()

pad = "Wacom Intuos S Pad pad"
stylus = "Wacom Intuos S Pen stylus"
eraser = "Wacom Intuos S Pen eraser"

#DEVICES[stylus].set(option="Mode", value="Absolute")
DEVICES[stylus].set(option="Mode", value="Relative")

if __name__ == "__main__":

    print(get_devices())
