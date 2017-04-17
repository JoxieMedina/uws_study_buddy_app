#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from time import sleep
from random import random
from clint.textui import progress


if __name__ == '__main__':
    for i in progress.mill(range(20), label='Request: ',expected_size=100):
        sleep(random() * 0.05)
    # with progress.Bar(label="Request 10092: ", expected_size=20) as bar2:
    #     bar2.show(20)

    # ppdas = ""

    # for i in range(1, 20):
    #     ppdas.join("#")
    # print(ppdas)

    # with progress.Bar(label="nonlinear", expected_size=10) as bar:
    #     last_val = 0
    #     for val in (1, 2, 3, 9, 10):
    #         sleep(2 * (val - last_val))
    #         bar.show(val)
    #         last_val = val

    # for i in progress.dots(range(100)):
    #     sleep(random() * 0.2)

    # Override the expected_size, for iterables that don't support len()
    D = dict(zip(range(100), range(100)))
    for k, v in progress.bar(D.items(), expected_size=len(D)):
        sleep(random() * 0.2)


#  def show_locations_options(self):
#         self.print_dictionary(self._locations)
#         option = self.get_single_input()
#         if not option:
#             print("Enter an option to continue")
#             self.show_locations_options()
#         else:
#             try:
#                 if option not in self._locations.keys():
#                     print("Invalid option {} try again".format(option))
#                     self.show_locations_options()
#                 else:
#                     print("Great option: {} ".format(self._locations[option]))
#                     return option
#             except ValueError, KeyError:
#                 pass

    # def print_dictionary(self, toprint):
    #     for key in toprint:
    #         print ("{key} - {value}".format(key=key, value=toprint[key]))

    # def get_single_input(self):
    #     """ Wait for a single character keypress and return the value,
    #     also is verifig the system values for differents UNIX Based systems
    #     Reference: http://code.activestate.com/recipes/134892/
    #     Return: The key pressed"""
    #     # Getting the File descriptor for evaluate the UNIX version
    #     filedescriptor = sys.stdin.fileno()
    #     # Temporaly saving the original or default values
    #     defaults = termios.tcgetattr(filedescriptor)
    #     try:
    #         # Change the mode of the file descriptor fd to raw. I
    #         tty.setraw(sys.stdin.fileno())
    #         # Getting the character
    #         char = sys.stdin.read(1)
    #     finally:
    #         # Return the mode of the file descriptor to defaults
    #         termios.tcsetattr(filedescriptor, termios.TCSADRAIN, defaults)
    #     return char
