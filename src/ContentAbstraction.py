
class CompositeContent:
    def __init__(self):
        self.items = list()


    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return "{0}(items={1})".format(self.__class__.__name__, self.items)

    def extend(self, other):
        if not isinstance(other, CompositeContent):
            raise TypeError("The other instance must inherit from the BaseCollection class")

        merged_items = self.items + other.items
        self.items = merged_items
        return self

    def add_item( self, other ):
        if not isinstance(other, CompositeContent):
            raise TypeError("The new item must inherit from the BaseCollection class")
        self.items.append( other )

    def get_item_by_uname(self, name):
        for item in self.items:
            if item.unique_name == name:
                return item
        return None
