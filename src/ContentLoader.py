from src.Page import Pages
from src.Hier import Hier
from configparser import ConfigParser
import os
import feedparser
from datetime import datetime
from time import mktime
# imports all the different types of content
from src.ContentAbstraction import CompositeContent
from src.Feed import Feeds
from src.Product import Products
from src.Tearoff import Tearoffs


# loader of all types of content
class ContentLoader:
    def __init__( self, config ):
        self._config = config

        self._raw_content = CompositeContent()

        # load content of type 'Page'
        self._pages = Pages( config )

        # feeds specify what pages they are available to in a comma-delimited list
        # this allows the generator to make them available to generating certain pages by unique_name
        self._feeds = Feeds( config )

        # products to showcase in the websites (if different from a page)
        self._products = Products( config )

        # tearoffs are short descriptions with a call to action link attached to products and pages
        self._tearoffs = Tearoffs( config )

        self._raw_content.extend( self._pages )
        self._raw_content.extend( self._feeds )
        self._raw_content.extend( self._products )
        self._raw_content.extend( self._tearoffs )

        # create a hierarchical data structure representing the relation of content to parents/children
        self.content = Hier(config, self._raw_content)

    def __repr__(self):
        return repr(self.content.top_down)

    def __setitem__(self, key, value):
        self.content.top_down[key] = value

    def __delitem__(self, key):
        del self.content.top_down[key]

    def __iter__(self):
        return iter(self.content.top_down)

    def __len__(self):
        return len(self.content.top_down)