#!//usr/bin/python

# Sets a percentual of total area of wacom,
#   putting it at the center of the pad.

from sys import argv
from subprocess import Popen

XA = 0
YA = 0
XB = 15200
YB = 9500

percent = int(argv[1])

device = "Wacom Intuos S Pen stylus"

sizex = (XB/100) * percent
sizey = (YB/100) * percent

offsetx = XB / (100/(percent/2))
offsety = YB / (100/(percent/2))

xa = round(offsetx)
ya = round(offsety)
xb = round(sizex + offsetx)
yb = round(sizey + offsety)

#command = f'xsetwacom set "{device}" "Area" "{xa} {ya} {xb} {yb}"'

command = ['xsetwacom', 'set', f'{device}', 'Area', f'{xa} {ya} {xb} {yb}']

print(" ".join(command))

Popen(command)
