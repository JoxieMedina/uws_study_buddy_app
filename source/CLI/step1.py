#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solution for COMP07027 Coursework 2017
Written by B00319125
2017-04

Python version: 3
LIBRARIES:
    Python Command Line Interface Tools (CLINT): $ pip3 install clint

"""
import os
from random import randrange

# Import the library CLINT
from clint.textui import prompt, puts, colored, indent

requests = []


class Request():
    
    def __init__(self, idrequest):
        # Setting the defaults values
        self._request_id = idrequest
        self._fist_name = ""
        self._surname = ""
        self._password = ""
        self._programme = ""
        self._year = ""
        self._module = ""
        # Set to save the availables days and times
        self._availables_times = set()
        self._campus = ""
        # Static Dictionaries
        self._locations = ["Ayr", "Dumfries", "Paisley", "Hamilton"]
        self._years = ["1st year", "2nd year", "3rd year", "4th year"]
        self._programmes = ["BSc Computer Science", "BSc Networking", "BSc Multimedia",
                            "BSc Computer Games Development", "BSc Business Technology"]
        self._modules = ["Introduction to programming", "Computing systems",
                         "Introduction to networks", "Mathematics for computing",
                         "Introduction to Web Development", "Professional Development",
                         "Computing/Business Technology/Enterprise"]
        self._times = ["Morning", "Afternoon", "Evening"]
        self._days = ["Monday", "Tuesday", "Wednesday",
                      "Thursday", "Friday", "Saturday", "Sunday"]
        # Calls
        self._create_request()
        # Saving the request id for not use in the future
        requests.append(self._request_id)
        self._display_all()

    def _display_all(self):
        os.system('clear')
        title = "| Your information |"
        output = "  RequestID: {}\n"\
                 "  Name: {} {}\n"\
                 "  Password: {}\n"\
                 "  Programme: {}\n"\
                 "  Module: {}\n"\
                 "  Year: {}\n"\
                 "  Campus: {}\n"\
                 "  Availables Times:".format(
                     self._request_id,
                     self._fist_name.capitalize(),
                     self._surname.capitalize(),
                     self._password,
                     self._programme,
                     self._module,
                     self._year,
                     self._campus)
        header = '+' + '-' * (int(len(output) / 2) - 60) + title + '-' * \
            int((len(output) / 2) - 60) + '+'
        footer = '+' + '-' * (len(header) - 2) + '+'
        times_string = "    "
        for i in self._availables_times:
            times_string = times_string + "> " + i + '\n    '
        lines = [header, output, times_string, footer]
        card = '\n'.join(lines)
        with indent(4):
            puts(card)

    def _create_request(self):
        self._fist_name = prompt.query("Input First Name: ")
        self._surname = prompt.query("Input Surname: ")
        self._password = prompt.query("Input Password: ")
        self._programme = prompt.options("\nSelect a programme option",
                                         self.to_clint_options(self._programmes))
        self._module = prompt.options(
            "\nSelect a module option", self.to_clint_options(self._modules))
        self._year = prompt.options(
            "\nSelect a year option", self.to_clint_options(self._years))
        self._campus = prompt.options(
            "\nSelect a campus option", self.to_clint_options(self._locations))
        # Handle N times availables
        puts(colored.yellow("Availables Times (Duplicates are silently ignored)"))
        opt = 'Yes'
        while opt == 'Yes':
            day = prompt.options(
                "\nSelect a day option", self.to_clint_options(self._days))
            time = prompt.options(
                "\nSelect a time option", self.to_clint_options(self._times))
            # Uses a set because the duplicates are silently ignored
            self._availables_times.add("{} {}".format(day, time))
            opt = prompt.options(
                colored.green("Add another?"), self.to_clint_options(["Yes", "No"]))

    def to_clint_options(self, options):
        """This function returns the dictionary for prompt options in
        CLINT

        Returns:
            A Dictionary of options to clint prompt
        """
        temp = dict(zip(range(1, len(options) + 1), options))
        opts = []
        for key in temp:
            opts.append(
                {'selector': key, 'prompt': temp[key], 'return': temp[key]})
        return opts


def generate_random():
    """Parse a seat designator into a valid row and letter.

        Returns:
            A new valid 6 digits random number.
    """
    global requests

    new_id = 0  # use a distinguished, invalid value to start the loop
    # reject candidate ID if invalid or already exists
    while new_id == 0 or new_id in requests:
        new_id = randrange(1e5, 1e6)  # generate a candidate 6-digit number
    return new_id


def main():
    """
        Main fuction
    """
    opt = 'Yes'
    while opt == 'Yes':
        request_id = generate_random()
        request = Request(request_id)
        opt = prompt.options(
            colored.green("Create another Request?"), request.to_clint_options(["Yes", "No"]))



# run main() if this file is not being used otherwise, e.g. by test
if __name__ == "__main__":
    main()
