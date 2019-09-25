"""
Name:Dong Li
Date:22 Sep 2019
Brief Project Description:This program is create the GUI that display placelist.Users can add places in placelist，sort placelist by priority,
 country,name and can clear what they input.
GitHub URL:https://github.com/JCUS-CP1404/a2--jc484329
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from place import Place
from placelist import PlaceList
from kivy.properties import StringProperty
from kivy.properties import ListProperty

class PlacesToVisitApp(App):
    """ Main program:Display a list of places in a GUI model using Kivy app"""
    message = StringProperty()        # Define status text
    news = StringProperty()
    current_sort = StringProperty()   # Define sort
    sort_choices = ListProperty()

    def __init__(self, **kwargs):
        """Construct main app"""
        super(PlacesToVisitApp, self).__init__(**kwargs)
        self.place_list = PlaceList()
        self.sort_choices = ["name", "country", "priority", "is_required"]
        self.current_sort = self.sort_choices[0]
        self.place_list.load_places()

    def build(self):
        """
        Build the Kivy GUI.
        :return: reference to the root Kivy widgit
        """
        self.title = "Places to visit by Dong Li"          # Name GUI name
        self.root = Builder.load_file('app.kv')    # Load app.kivy
        self.create_widget()                      # Create widget in GUI
        return self.root

    def change_sort(self, sorting_choice):
        """
        Function to change the sorting of the place list
        :param sorting_choice: Based on what choice the user selects, the place list will be sorted that way
        :return: sorted place list
        """
        self.message = "place have been sorted by: {}".format(sorting_choice)
        self.place_list.sort(sorting_choice)
        self.root.ids.entriesBox.clear_widgets()
        self.create_widget()
        sort_index = self.sort_choices.index(sorting_choice)
        self.current_sort = self.sort_choices[sort_index]

    def Clear_input(self):
        """Clear inputs after clicking the Clear button"""
        self.root.ids.place_name.text = ''     # Clear input
        self.root.ids.place_country.text = ''
        self.root.ids.place_priority.text = ''

    def create_widget(self):
        """Create widgets that lists the places from the csv file"""
        self.root.ids.entriesBox.clear_widgets()
        num_place = len(self.place_list.list_places)  # Determine the number of places in the list
        visited_place = 0
        for place in self.place_list.list_places:  # Loop from first place to last place
            name = place.name
            # assert isinstance(place.country)
            country = place.country
            priority = place.priority
            visited = place.is_required
            display_text = self.generateDisplayText(name, country, priority,
                                                    visited)  # Display place's information on the widget
            if visited == "n":
                visited_place += 1
                button_color = self.getColor(visited)
            else:
                button_color = self.getColor(visited)

            temp_button = Button(text=display_text, id=place.name,
                                 background_color=button_color)  # Mark the place visited
            temp_button.bind(on_release=self.press_entry)  # Display message of the GUI status
            self.root.ids.entriesBox.add_widget(temp_button)
        self.message = "To visit: {}. visited: {}".format(num_place - visited_place,
                                                          visited_place)  # Display number of place visited or not visited

    def generateDisplayText(self, name, country, priority, visited):
        """Formating text display in the message"""
        if visited == "n":
            display_text = "{} by {} ({}) (Visited)".format(name, country, priority)
        else:
            display_text = "{} by {} ({})".format(name, country, priority)

        return display_text

    def getColor(self, visited):
        """Display colors of the place visited and not visited"""
        if visited == "n":
            button_color = [0.4, 0.6, 0, 1]
        else:
            button_color = [0.4, 0.7, 0.9, 1]
        return button_color

    def press_entry(self, button):
        """Display the 2nd message"""
        buttonText = button.text
        selectedPlace = Place()
        for place in self.place_list.list_places:
            placeDisplayText = self.generateDisplayText(place.name, place.country, place.priority, place.is_required)
            if buttonText == placeDisplayText:
                selectedPlace = place
                break

        selectedPlace.mark_visited()   # Mark the place visited
        self.root.ids.entriesBox.clear_widgets()  # Apply to GUI
        self.create_widget()

        self.news = "You have visited {}".format(selectedPlace.name)  # Display change in news

    def add_places(self):
        """
        Add the new place
        :return: Add the place inputted to the place list
        """
        if self.root.ids.place_name.text == "" or self.root.ids.place_country.text == "" or self.root.ids.place_priority.text == "":
            self.root.ids.status2.text = "All fields must be completed"
            return
        try:
            # Define place item inputted
            place_name = str(self.root.ids.place_name.text)
            place_country = str(self.root.ids.place_country.text)
            place_priority = int(self.root.ids.place_priority.text)
            is_required = "y"

            # Add place's input to the placelist
            self.place_list.add_to_list(place_name, place_country, place_priority, is_required)
            temp_button = Button(
                text=self.generateDisplayText(place_name, place_country, place_priority, is_required))
            temp_button.bind(on_release=self.press_entry)

            # Format new place item
            temp_button.background_color = self.getColor(is_required)
            self.root.ids.entriesBox.add_widget(temp_button)
            self.create_widget()

            # Clear input after adding place
            self.root.ids.place_name.text = ""
            self.root.ids.place_country.text = " "
            self.root.ids.place_priority.text = ""

        except ValueError:  # Display error when type is wrong
            self.news = "Please enter a valid priority"

    def on_stop(self):  # Stop GUI and save
        self.place_list.save_places()

        # Run the PlacesToLearnApp


PlacesToVisitApp().run()
