from place import Place
from operator import attrgetter


class PlaceList:
    """
    initiate the self attribute list_places
    :return: None
    """
    def __init__(self):
        self.list_places = []

    def load_places(self):
        """Load the places from csv file and append them to list_places"""
        in_file = open("places.csv","r")
        lines = in_file.readlines()
        for line in lines:
            place_item = line.split(',')
            place_item[3] = place_item[3].strip('\n')
            loaded_place = Place(place_item[0],place_item[1],place_item[2],place_item[3])

            self.list_places.append(loaded_place)


        in_file.close()


    def sort(self, key):
        """
        Sort the places based on the sort_choice selected
        :param key: self, key
        :return: none
        """
        self.list_places = sorted(self.list_places, key=attrgetter(key, "name"))

    def add_to_list(self, name, country, priority, is_required):
        newPlace = Place(name, country, priority, 'y')
        self.list_places.append(newPlace)


    def save_places(self):
        """save changes made to the places and then out file"""
        csv_string = ""
        for each in self.list_places:
            csv_string += "{},{},{},{}\n".format(each.name, each.country, each.priority, each.is_required)
        out_file = open("places.csv", 'w')
        out_file.seek(0)
        out_file.truncate()
        out_file.write(csv_string)
        out_file.close()
