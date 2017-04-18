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
import pickle
import pprint as pp
# Import the library CLINT
from clint.textui import prompt, puts, colored, indent

requests = []


class Request():
    def __init__(self, idrequest):
        # Setting the defaults values
        global requests
        requests = get_storage_data('Requests')
        self._request_id = idrequest
        self._first_name = ""
        self._surname = ""
        self._password = ""
        self._programme = ""
        self._year = ""
        self._module = ""
        self._campus = ""
        # Set to save the availables days and times
        self._availables_times = set()
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
        # Update the request list
        requests.append(self._request_id)
        set_storage_data('Requests', requests)
        # Create a new file for the new request
        set_storage_data(str(self._request_id), {
            "request_id": self._request_id,
            "first_name": self._first_name,
            "surname": self._surname,
            "password": self._password,
            "programme": self._programme,
            "module": self._module,
            "year": self._year,
            "campus": self._campus,
            "availables_times": '/'.join(self._availables_times)
        })
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
                     self._first_name.capitalize(),
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

    def _display_restricted(self):
        """
            Print a restricted view of the request data
            without request id, student name and password.
        """
        os.system('clear')
        title = "| Your information |"
        output = "  Programme: {}\n"\
                 "  Module: {}\n"\
                 "  Year: {}\n"\
                 "  Campus: {}\n"\
                 "  Availables Times:".format(
                     self._programme,
                     self._module,
                     self._year,
                     self._campus)
        header = '+' + '-' * (int(len(output) / 2) - 40) + title + '-' * \
            int((len(output) / 2) - 40) + '+'
        footer = '+' + '-' * (len(header) - 2) + '+'
        times_string = "    "
        for i in self._availables_times:
            times_string = times_string + "> " + i + '\n    '
        lines = [header, output, times_string, footer]
        card = '\n'.join(lines)
        with indent(4):
            puts(card)

    def _create_request(self):
        self._first_name = prompt.query("Input First Name: ")
        self._surname = prompt.query("Input Surname: ")
        self._password = prompt.query("Input Password: ")
        self._programme = prompt.options("\nSelect a programme option",
                                         to_clint_options(self._programmes))
        self._module = prompt.options(
            "\nSelect a module option", to_clint_options(self._modules))
        self._year = prompt.options(
            "\nSelect a year option", to_clint_options(self._years))
        self._campus = prompt.options(
            "\nSelect a campus option", to_clint_options(self._locations))
        # Handle N times availables
        puts(colored.yellow("Availables Times (Duplicates are silently ignored)"))
        opt = 'Yes'
        while opt == 'Yes':
            day = prompt.options(
                "\nSelect a day option", to_clint_options(self._days))
            time = prompt.options(
                "\nSelect a time option", to_clint_options(self._times))
            # Uses a set because the duplicates are silently ignored
            self._availables_times.add("{} {}".format(day, time))
            opt = prompt.options(
                colored.green("Add another?"), to_clint_options(["Yes", "No"]))


def to_clint_options(options):
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


def get_storage_data(filename):
    """This function find a local pickle file and returns the data

    Returns:
        A Dictionary or list wich is stored in the picke file
    """
    temp = []
    temp_path = "./" + filename + ".pickle"
    if os.path.exists(temp_path):
        try:
            with open(filename + ".pickle", mode="rb") as storage:
                temp = pickle.load(storage)
        finally:
            pass
    if temp is None:
        return []
    return temp


def set_storage_data(filename, data):
    """
    This function set or create a pickle file if is not found
    a local pickle file and returns the data

    """
    # Saving Persistend data into a file
    # The with snippet permits no worry about closing the file
    with open(filename + ".pickle", mode="wb") as storage:
        return pickle.dump(data, storage)


def generate_random():
    """Parse a seat designator into a valid row and letter.

        Returns:
            A new valid 6 digits random number.
    """
    new_id = 0  # use a distinguished, invalid value to start the loop
    while new_id == 0 or new_id in requests:  # reject candidate ID if invalid or already exists
        new_id = randrange(1e5, 1e6)  # generate a candidate 6-digit number
    return new_id


def main():
    """
        Main fuction
    """
    menu_opt = prompt.options(
        colored.green("Welcome to UWS STUDY BUDDY"),
        to_clint_options(["Create New Request", "Exit"]))
    while menu_opt != "Exit":
        if menu_opt == "Create New Request":
            request_id = generate_random()
            request = Request(request_id)
            # Getting the stored files contents
            requests_file = get_storage_data("Requests")
            request_created = get_storage_data(str(request_id))
            # Print the stored files contents
            puts(colored.blue("Request.pickle file content: \n"))
            pp.pprint(requests_file)
            puts(colored.blue(str(request_id) + ".pickle file content: \n"))
            pp.pprint(requests_file)
            menu_opt = prompt.options(
                colored.green("\nUWS STUDY BUDDY"),
                to_clint_options(["Create New Request", "Exit"]))


# run main() if this file is not being used otherwise, e.g. by test
if __name__ == "__main__":
    main()
