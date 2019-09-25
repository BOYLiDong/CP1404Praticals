
# create your Place class in this file

class Place:
    def __init__(self, name="", country="", priority=0, is_required=""):
        """Determine items a place would help"""
        self.country = country
        self.name = name
        self.priority = priority
        self.is_required = is_required

    def __str__(self):
        """Display an announcement when a place is inpputed"""
        if self.is_required == "n":
            is_required = "Visited"
            return ("You have visited {} by {} ({})".format(self.name, self.priority),self.country)
        else:
            is_required = "y"
            return ("You have not visited {} by {} ({})".format(self.name, self.priority),self.country)

    def mark_visited(self):
        """Mark the place visited"""
        self.is_required = 'n'
        return self.is_required

