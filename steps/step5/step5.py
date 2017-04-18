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
from time import sleep
from random import randrange, random
import pickle

# Import the module textui of the library 'clint' for easy handling of
# inputs and outputs in the CLI output
from clint.textui import prompt, puts, colored, indent, progress, validators
# prompt: print an option prompt for handle a valid option
# puts: custom print method
# colored: allow give color to a output
# indent: allow indent the text output
# progress: print a progress state in the output
# validators: allow validate an input with a regular expresion for example

# Initial state of the requests list
requests = []


class Request():
    def __init__(self, idrequest):
        # Make the requests list with a global scope
        global requests
        # Getting the requests list with the Requests.pickle file
        requests = get_storage_data('Requests')
        # Check an print if the any file was deleted
        puts(colored.yellow("\n".join(self._check_request_files())))
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
        requests.append(str(self._request_id))
        # Set or create the Requests.pickle file
        set_storage_data('Requests', requests)
        # Create a new file for the new request
        self._current_request = {
            "request_id": self._request_id,
            "first_name": self._first_name,
            "surname": self._surname,
            "password": self._password,
            "programme": self._programme,
            "module": self._module,
            "year": self._year,
            "campus": self._campus,
            "availables_times": '/'.join(self._availables_times)
        }
        # Set or create the current request file
        set_storage_data(str(self._request_id), self._current_request)
        # Display the current requests ingresed
        self._display_all()
        # Find if the current request has any match in all requests
        matches = find_matches(self._current_request)
        if matches:
            # Print a colored (cyan) announcement informing that matches were
            # found
            puts(colored.cyan(str(len(matches)) + " matches were found!"))
            _print_matches(matches)
         # Show a prompt of options asking if want to see the matches found
            match_opt = prompt.options(
                colored.green("Do you want tho see the matches?"),
                to_clint_options(["Yes", "No"]))
            if match_opt == "Yes":
                # If yes call the method that shows the matches
                _view_matches(matches)
            else:
                pass
        else:
            pass

    def _display_all(self):
        """
            Display all the data of the current request
        """
        os.system('clear')  # Clear the console
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
        os.system('clear')  # Clear the console
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

    def _check_request_files(self):
        """
            Check if the request files listed in the Requests.pickle file
            are properly created

            Returns:
                An errors list if one or more files not exists
        """
        errors = []  # Created and empty list
        if requests:
            for request_id in requests:
                temp_path = "./" + str(request_id) + ".pickle"
                # Method that validate if the file with the passed path as
                # argument exists
                if not os.path.exists(temp_path):
                     # Append an error string if the file not exists
                    errors.append("Warning: File for the request " +
                                  str(request_id) + " does not exists!")
        return errors

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


def _to_match_options(options):
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
            {'selector': key, 'prompt': "Request: " + temp[key], 'return': temp[key]})
    return opts


def find_matches(request):
    """
        Args:
            A request to find matches
        Returns:
            A list of matches
    """
    matches = []
    # Getting the lists of the requests ids
    all_request_ids = get_storage_data('Requests')
    all_saved_requests = []
    # for each id fund, get the corresponding request file data
    if all_request_ids:
        for id_request in requests:
            if str(id_request) != str(request["request_id"]):
                all_saved_requests.append(
                    get_storage_data(str(id_request)))
    # Create a set with only the matching values for evaluate
    matching_values = set(
        {request["campus"], request["programme"], request["module"]})
    matching_times = request["availables_times"]
    for req in all_saved_requests:
        rank = 0  # Max value will be 99
        req_times = set(req["availables_times"].split('/'))
        # The module, programme and campus criteria match
        # have the same rank weight
        for item in matching_values:
            if item in req["module"]:
                rank += 26
            if item in req["programme"]:
                rank += 26
            if item in req["campus"]:
                rank += 26
        # The time maching
        # The max value if match all the combinations
        # is 21 (7 days times 3 differents periods)
        for time in matching_times:
            if time in req_times:
                rank += 1
        if rank:  # If the rank value change the value it found a match
            matches.append(
                {"request_id": req['request_id'], "rank": rank})
    return matches


def _print_matches(_matches):
    for match in _matches:
        label = "Request " + str(match["request_id"]) + " Rank:"
        # Print the matches with a progress effect in the Rank value
        for i in progress.mill(range(match["rank"]), label=label, expected_size=100):
            sleep(random() * 0.02)


def _print_match(match):
    """
            Print all the matches listed in the _matches argument
            without request id, student name and password.

            Args:
                Matches list
    """
    _match = get_storage_data(str(match))
    title = "| Your information |"
    output = "  Programme: {}\n"\
             "  Module: {}\n"\
             "  Year: {}\n"\
             "  Campus: {}\n"\
             "  Availables Times:".format(
                 _match["programme"],
                 _match["module"],
                 _match["year"],
                 _match["campus"])
    header = '+' + '-' * (int(len(output) / 2) - 40) + title + '-' * \
        int((len(output) / 2) - 40) + '+'
    footer = '+' + '-' * (len(header) - 2) + '+'
    times_string = "    "
    req_times = set(_match["availables_times"].split('/'))
    for i in req_times:
        times_string = times_string + "> " + i + '\n    '
    lines = [header, output, times_string, footer]
    card = '\n'.join(lines)
    with indent(4):
        puts(card)


def _view_matches(_matches):
    """
        Show an options prompt of the all matches
    """
    match = ""
    options = []
    for ma in _matches:
        options.append(str(ma["request_id"]))
    options.append("Exit")
    while match != "Exit":
        match = prompt.options(
            colored.green("Select one match to see it:"),
            _to_match_options(options))
        if match != "Exit":
            _print_match(match)
        else:
            pass


def to_clint_options(options):
    """
        This method only format a list to be
        acceptable for the prompt.options method

        Args:
            A list of options
        Returns:
            A list of sets with prompt.options format
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
    """This function find a local pickle file and returns the data

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


def edit_request(_request_id):
    """
        This method permits edit an existing request
    """
    # Static Dictionaries
    _availables_times = set()
    _locations = ["Ayr", "Dumfries", "Paisley", "Hamilton"]
    _years = ["1st year", "2nd year", "3rd year", "4th year"]
    _programmes = ["BSc Computer Science", "BSc Networking", "BSc Multimedia",
                   "BSc Computer Games Development", "BSc Business Technology"]
    _modules = ["Introduction to programming", "Computing systems",
                "Introduction to networks", "Mathematics for computing",
                "Introduction to Web Development", "Professional Development",
                "Computing/Business Technology/Enterprise"]
    _times = ["Morning", "Afternoon", "Evening"]
    _days = ["Monday", "Tuesday", "Wednesday",
             "Thursday", "Friday", "Saturday", "Sunday"]
    request_stored = get_storage_data(str(_request_id))
    if request_stored:
        input_pass = prompt.query(
            "Input the password for the request " + str(_request_id))
        if input_pass == request_stored["password"]:
            _availables_times = set(
                request_stored["availables_times"].split("/"))
            first_name = prompt.query(
                "Input First Name: ", default=request_stored["first_name"])
            surname = prompt.query(
                "Input Surname: ", default=request_stored["surname"])
            programme = prompt.options("\nSelect a programme option",
                                       to_clint_options(_programmes),
                                       default=request_stored["programme"])
            module = prompt.options(
                "\nSelect a module option",
                to_clint_options(_modules), default=request_stored["module"])
            year = prompt.options(
                "\nSelect a year option",
                to_clint_options(_years), default=request_stored["year"])
            campus = prompt.options(
                "\nSelect a campus option",
                to_clint_options(_locations), default=request_stored["campus"])
            # Handle N times availables
            puts(colored.yellow("Availables Times (Duplicates are silently ignored)"))
            opt = 'Yes'
            while opt == 'Yes':
                day = prompt.options(
                    "\nSelect a day option", to_clint_options(_days))
                time = prompt.options(
                    "\nSelect a time option", to_clint_options(_times))
                # Uses a set because the duplicates are silently ignored
                _availables_times.add("{} {}".format(day, time))
                opt = prompt.options(
                    colored.green("Add another?"), to_clint_options(["Yes", "No"]))
            to_save = {
                "request_id": _request_id,
                "first_name": first_name,
                "surname": surname,
                "password": request_stored["password"],
                "programme": programme,
                "module": module,
                "year": year,
                "campus": campus,
                "availables_times": '/'.join(_availables_times)
            }
            set_storage_data(str(_request_id), to_save)
            matches = find_matches(to_save)
            if matches:
                puts(colored.cyan(str(len(matches)) + " matches were found!"))
                _print_matches(matches)
                match_opt = prompt.options(
                    colored.green("Do you want tho see the matches?"),
                    to_clint_options(["Yes", "No"]))
                if match_opt == "Yes":
                    _view_matches(matches)
                else:
                    pass
            else:
                pass
        else:
            puts(colored.red("Invalid password!"))
    else:
        puts(colored.red("Request Not found!"))


def do_menu():
    """
        this Method permits print the main menu of options
    """
    return prompt.options(
        colored.green("Welcome to UWS STUDY BUDDY"),
        to_clint_options(["Create New Request", "Edit a Request", "Exit"]))


def main():
    """
        Main fuction
    """
    # Getting the menu option for the menu prompt
    menu_opt = do_menu()
    # Repeat until the user choose the 'Exit' option from the prompt
    while menu_opt != "Exit":
        if menu_opt == "Create New Request":
            request_id = generate_random()
            request = Request(request_id)
            # Show the menu options again
            menu_opt = do_menu()
        if menu_opt == "Edit a Request":
            # Show a prompt requesting the Request ID
            request_id = prompt.query(
                "Input a Request ID: ",
                # Validate if the request id is a 6 digits number
                # with the regular expresion ^[0-9]{6,6}$
                # RegExp Explanation :
                # ^ : beginning anchor
                # [0-9] : Accept any digit between 0 and 9
                # {6,6} : The minimum and maximum value
                # $ : Exit anchor
                validators=[validators.RegexValidator("^[0-9]{6,6}$",
                                                      message="Input a 6 digits number")])
            # Call the edit request method
            edit_request(request_id)
            # Show the menu options again
            menu_opt = do_menu()



# run main() if this file is not being used otherwise, e.g. by test
if __name__ == "__main__":
    main()
