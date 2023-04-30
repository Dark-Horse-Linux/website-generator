# a representation of unique names in hierarchal order to represent item hierarchy
# useful for generating navbars and associated specific content types with each other

class Hier:
    def __init__( self, config, content_items ):
        self._bottom_up = content_items

        # throw an exception if the hiearchy doesn't add up
        self.validate_hierarchy(content_items)

        # top level is represented as "_top_"
        self._content_tree = self.build_tree(content_items, "_top_")
        self.top_down = self.build_instance_tree(self._content_tree)

    def validate_hierarchy( self, items ):
        unique_names = {item.unique_name for item in items}
        for item in items:
            if item.parent is not None and item.parent != "_top_" and item.parent not in unique_names:
                raise ValueError("Parent '{0}' of item '{1}' does not exist".format(item.parent, item.unique_name))
            if item.parent == item.unique_name:
                raise ValueError("Self-referential parent in content definition.")

    def build_tree( self, items, parent_unique_name=None ):
        tree = {}
        for item in items:
            if item.parent == parent_unique_name:
                tree[item.unique_name] = self.build_tree( items, item.unique_name )
        return tree

    def print_tree( self, tree, level=0 ):
        for unique_name, children in tree.items():
            print( "\t" * level + unique_name )
            self.print_tree( children, level + 1 )

    def build_instance_tree( self, tree ):
        instance_list = list()

        for unique_name, children in tree.items():
            item_instance = self._bottom_up.get_item_by_uname(unique_name)
            sorted_children = self.build_instance_tree(children)
            item_instance.children = sorted(sorted_children, key=lambda child: child.title)
            instance_list.append(item_instance)
        return instance_list

    def __repr__(self):
        return repr(self.top_down)