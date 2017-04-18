#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solution for COMP07027 Coursework 2017
Written by B00319125
2017-04

Python version: 3
LIBRARIES:
    Python Command Line Interface Tools (CLINT): $ pip3 install clint
    Reference: https://github.com/kennethreitz/clint/

"""
import os
from random import randrange
import pickle
import pprint as pp
# Import the module textui of the library 'clint' for easy handling of
# inputs and outputs in the CLI output
from clint.textui import prompt, puts, colored, indent
# prompt: print an option prompt for handle a valid option
# puts: custom print method
# colored: allow give color to a output
# indent: allow indent the text output

# Initial state of the requests list
requests = []


class Request():
    def __init__(self, idrequest):        
        # Make the requests list with a global scope
        global requests
        # Getting the requests list with the Requests.pickle file
        requests = get_storage_data('Requests')
        # Setting the defaults values
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
        # Set or create the Requests.pickle file
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
        # Display the current requests ingresed
        self._display_all()

    def _display_all(self):
        """
            Display all the data of the current request
        """
        os.system('clear') # Clear the console

        title = "| Your information |"
        # Creating the output and format it
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
        # Create a header banner with the title to show a highlighted output
        header = '+' + '-' * (int(len(output) / 2) - 60) + title + '-' * \
            int((len(output) / 2) - 60) + '+'
        # The header and footer banners are created calculating the lenth of
        # the output
        footer = '+' + '-' * (len(header) - 2) + '+'
        # Append all the available times in one string
        times_string = "    "
        for i in self._availables_times:
            times_string = times_string + "> " + i + '\n    '
        # Put all the lines in one list
        lines = [header, output, times_string, footer]
        # Join all
        card = '\n'.join(lines)
        # Indent with 4 spaces the output
        with indent(4):
            # Use of the context manager 'with' to use the indent method only
            # in the line bellows
            puts(card)

    def _display_restricted(self):
        """
            Print a restricted view of the request data
            without request id, student name and password.
        """
        os.system('clear')# Clear the console
        title = "| Your information |"
        # Creating the output and format it
        output = "  Programme: {}\n"\
                 "  Module: {}\n"\
                 "  Year: {}\n"\
                 "  Campus: {}\n"\
                 "  Availables Times:".format(
                     self._programme,
                     self._module,
                     self._year,
                     self._campus)
        # Create a header banner with the title to show a highlighted output
        header = '+' + '-' * (int(len(output) / 2) - 40) + title + '-' * \
            int((len(output) / 2) - 40) + '+'
        # The header and footer banners are created calculating the lenth of
        # the output
        footer = '+' + '-' * (len(header) - 2) + '+'
        # Append all the available times in one string
        times_string = "    "
        for i in self._availables_times:
            times_string = times_string + "> " + i + '\n    '
        # Put all the lines in one list
        lines = [header, output, times_string, footer]
        # Join all
        card = '\n'.join(lines)
        # Indent with 4 spaces the output
        with indent(4):
            # Use of the context manager 'with' to use the indent method only
            # in the line bellows
            puts(card)

    def _create_request(self):
        """
            This method allows handle all the input
            and create a request
        """
        # Show the prompts for inputs
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
        # Repeat until the user no longer wants to enter more times
        # If input a repeated time this will be ignored
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
    """
        This method only format a list to be
        acceptable for the prompt.options method

        Args:
            A list of options
        Returns:
            A list of sets with prompt.options format
    """
    # Create a set with number key
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
        # Use a try  / finally exceptions for if something goes wrong
        try:
            # The context manager 'with' permits no worry about closing the
            # file
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
    # The context manager 'with' permits no worry about closing the file
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
    # Getting the menu option for the menu prompt
    menu_opt = prompt.options(
        colored.green("Welcome to UWS STUDY BUDDY"),
        to_clint_options(["Create New Request", "Exit"]))
    # Repeat until the user choose the 'Exit' option from the prompt
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
            pp.pprint(request_created)
            # Show the menu options again
            menu_opt = prompt.options(
                colored.green("\nUWS STUDY BUDDY"),
                to_clint_options(["Create New Request", "Exit"]))


# run main() if this file is not being used otherwise, e.g. by test
if __name__ == "__main__":
    main()
