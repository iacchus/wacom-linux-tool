#!/usr/bin/env python

# https://plumbum.readthedocs.io/en/latest
from plumbum import local

XSETWACOM = local["xsetwacom"]

COMMANDS = {
    "list_devices": ("--list", "devices"),
    "get_option": lambda device, option: ("--get", device, option),
    "set_option": lambda device, option, value: ("--set", device, option,
                                                 value),
    "set_button": lambda device, button, value: ("--set", device, "Button",
                                                 button, value),
}

# plumbum's LocalCommand.run() -> (exit_code, stdout, stderr,)
EXIT_CODE = 0
STDOUT = 1
STDERR = 2


class Device:

    def __init__(self, name, id, dev_type):
        """Represents a device, which can be a `pad`, a `stylus`, an `eraser`
            etc
        """
        self.name = name
        self.id = id
        self.dev_type = dev_type


    def get_option(self, option):
        """Reads an option parameter from the device's atual configuration"""

        command = COMMANDS["get_option"](self.name, option)
        return XSETWACOM.run(command)

    def set_option(self, option, value):
        """Sets an option parameter to the device's atual configuration"""

        command = COMMANDS["set_option"](self.name, option, value)
        return XSETWACOM.run(command)

    def set_button(self, button, value):
        """Sets a button parameter to the device's atual configuration"""

        command = COMMANDS["set_button"](self.name, button, value)
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
    list_devices_output = XSETWACOM.run(command)[STDOUT]

    for device in list_devices_output. \
            strip(). \
            splitlines():

        raw_output = device.split("\t")
        name = raw_output[0].strip()
        id = raw_output[1].split(" ")[-1].strip()
        dev_type = raw_output[2].strip().split(" ")[-1]

        devices_dict.update({name: Device(name=name, id=id,
                                          dev_type=dev_type)})

    return devices_dict

DEVICES = get_devices()

if __name__ == "__main__":

    # my devices, for easy later reference
    pad = "Wacom Intuos S Pad pad"
    stylus = "Wacom Intuos S Pen stylus"
    eraser = "Wacom Intuos S Pen eraser"

    # ExpressKeys are:
    # 3     9        ->    11    13
    # 1     8        to    12    14

    # Pen
    # - tip: 1
    # - button closer to the tip: 15
    # - other button: 16

    #DEVICES[stylus].set(option="Mode", value="Absolute")
    DEVICES[stylus].set_option(option="Mode", value="Relative")

    DEVICES[stylus].set_button(button="1", value="button +1")
    DEVICES[stylus].set_button(button="2", value="button +15")
#     DEVICES[stylus].set_button(button="3", value="button 16")
    DEVICES[stylus].set_button(button="3", value="button +3")
    DEVICES[stylus].set_button(button="8", value="button 3")  # wtf

    DEVICES[pad].set_button(button="3", value="button 11")
    DEVICES[pad].set_button(button="1", value="button 12")
    DEVICES[pad].set_button(button="9", value="button 13")
    DEVICES[pad].set_button(button="8", value="button 14")

    print(DEVICES)
