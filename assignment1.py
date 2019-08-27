"""
Dong Li
Date started: 20 August 2018
Simple "travel tracker" that allows a user to track places
https://github.com/JCUS-CP1404/ Assignment 1--Dong li
"""
from operator import itemgetter

MENU = """Menu":
L - List places
A - Add new Place
M - Mark a place as visited
Q - Quit
"""

"""
Load the CSV file of places
For each line of the CSV file, strip the carriage return and store them into an element of a list
For each element on the list, split the strings at commas
Close the file
Return the list of place data
"""


def file_load():  # Load the CSV file containing all the places and their details
    in_file = open("places.csv", "r")
    place_list = [line.strip() for line in in_file.readlines()]
    place_data = [data.split(",") for data in place_list]
    in_file.close()
    return place_data


def place_name_length(place_data):  # Find the maximum size of the name field to line the place list up
    max_name_length = 0
    for i in range(len(place_data)):
        name_length = len(place_data[i][0])
        if name_length > max_name_length:
            max_name_length = name_length
    return max_name_length


def place_country_length(place_data):  # Find the maximum size of the country field to line the place list up
    max_country_length = 0
    for i in range(len(place_data)):
        country_length = len(place_data[i][1])
        if country_length > max_country_length:
            max_country_length = country_length
    return max_country_length


def list_places(place_data):  # Display a lined up list of all places with their details
    place_data.sort(key=itemgetter(1,0))

    max_name_length = place_name_length(place_data)
    max_country_length = place_country_length(place_data)

    place_count = 1
    place_visited_count = 0
    for i in range(len(place_data)):
        print("{}.".format(i), end=" ")
        if place_data[i][1] == 'y':
            print("*", end=" ")
        else:
            print(" ", end=" ")
            place_visited_count += 1
        print("{:{}} - {:{}} ({})".format(place_data[i][0], max_name_length, place_data[i][1],
                                          max_country_length, place_data[i][2]))
        place_count += 1

    print("{} places visited, {} places left to visit ".format(place_visited_count, place_count - place_visited_count))


def text_error_check(user_input):  # Error checking function, used when the user adds a song
    if user_input == "":
        print("input can not be blank")
        return False
    else:
        return True


def add_places():  # Adding a place into the list
    place_to_add = []
    place_name = ""
    place_country = ""
    place_priority = ""
    valid_input = False
    while not valid_input:
        place_name = str(input("Name: "))
        valid_input = text_error_check(place_name)
    place_to_add.append(place_name)

    valid_input = False
    while not valid_input:
        place_country = str(input("Country: "))
        valid_input = text_error_check(place_country)
    place_to_add.append(place_country)

    valid_input = False
    while not valid_input:
        try:
            place_priority = int(input("Priority: "))
            if place_priority < 0:
                print("Number must be >= 0")
                valid_input = False
            else:
                valid_input = True
        except ValueError:
            print("Invalid input; Enter a valid number")

    place_to_add.append(place_priority)
    place_to_add.append("y")
    print("{} by {} ({}) added to the place list".format(place_to_add[0], place_to_add[1], place_to_add[2]))
    return place_to_add


"""
If there is at least one place to visit:
    Input place number of the place to visit
    If the input is less than 0:
        Output "Number must be >= 0"
    Else if the input is more than the last number in the place list:
        Output "Invalid place number"
    If a Value error occurred, output "Invalid input"
    
    If the status of the place number inputted is required:
        Output "(place name) by (place country) learned"
    Else output "You already visited (place name)
    
Else output "No more places to visit!"
Return the place_data list
"""


def visit_place(place_data):  # Allow the user to mark a place as visited
    user_input = int()
    place_to_visit = False
    for i in range(len(place_data)):
        if place_data[i][3] == 'y':
            place_to_visit = True

    if place_to_visit:
        valid_input = False
        while not valid_input:
            try:
                print("Enter the number of a place to mark as visited")
                user_input = int(input(">>> "))
                if user_input < 0:
                    print("Number must be >= 0")
                elif user_input > (len(place_data) - 1):
                    print("Invalid place number")
                else:
                    valid_input = True
            except ValueError:
                print("Invalid input; Enter a valid number")
        if place_data[user_input][3] == 'y':
            place_data[user_input][3] = 'n'
            print("{} by {} visited".format(place_data[user_input][0], place_data[user_input][1]))
        else:
            print("You already visited {}".format(place_data[user_input][0]))
        return place_data

    else:
        print("No more places to visited!")
        return place_data


def file_save(place_data):  # Save the places to the CSV file when the user quits the program
    out_file = open("places.csv", "w")
    for i in range(len(place_data)):
        out_file.write("{},{},{},{}\n".format(place_data[i][0], place_data[i][1],
                                              place_data[i][2], place_data[i][3]))
    out_file.close()
    print("{} places saved to places.csv".format(len(place_data)))


def main():
    place_data = file_load()
    print("Travel Tracker 1.0 - by Lindsay Ward")
    print("{} places visited".format(len(place_data)))
    place_data.sort(key=itemgetter(1, 0))
    print(place_data)
    choice = ""
    while choice != "Q":
        print(MENU)
        choice = str(input(">>> ")).upper()
        if choice == "L":
         list_places(place_data)
        elif choice == "A":
            place_to_add = add_places()
            place_data.append(place_to_add)
            place_data.sort(key=itemgetter(1, 0))
        elif choice == "M":
            place_data = visit_place(place_data)
        elif choice == "Q":
            break
        else:
            print("Invalid menu choice")
    file_save(place_data)
    print("Have a nice day :)")

if __name__ == '__main__':
    main()