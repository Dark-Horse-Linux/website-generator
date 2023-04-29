from configparser import ConfigParser
from src.ContentAbstraction import CompositeContent
import os
import uuid


def get_top_level_subdirectories( path ):
    try:
        entries = os.listdir( path )
        subdirectories = [ os.path.join( path, entry ) for entry in entries if os.path.isdir( os.path.join( path, entry ) ) ]
        return subdirectories
    except FileNotFoundError:
        print( "Error: The path '{0}' does not exist.".format( path ) )
        return []


class Product:
    def __init__( self, product_dir ):
        self.hash = uuid.uuid4().hex
        self._metadata_file = os.path.join( product_dir, 'metadata.ini' )

        metadata_parser = ConfigParser()
        metadata_parser.read( self._metadata_file )

        # title used in the landing splash
        self.title =            metadata_parser.get( 'product', 'title' )

        # unique name for the object referred to by other objects for parent/child relationship
        self.unique_name =      metadata_parser.get( 'product', 'uid' )

        self.description =      metadata_parser.get( 'product', 'description' )

        # product landings have a link to a dedicated page or some other url
        self.link_url =         metadata_parser.get( 'product', 'link_url' )
        # name for the link button
        self.link_url_description =  metadata_parser.get( 'product', 'link_url_description' )

        # primary vs secondary product (allows theme to differentiate between primary product and secondary product)
        self.type =             metadata_parser.get( 'product', 'type' )

        self.url = "../../products/{0}".format( self.unique_name )


        self.children = list()
        self.parent = "_top_"

    def __str__(self):
        return str( self.unique_name )

    def __repr__(self):
        return "Product(title={0})".format(self.title)


class Products(CompositeContent):
    def __init__( self, config ):
        super().__init__()
        self.product_dir = os.path.join( config.content_dir, 'products' )
        self._item_paths = get_top_level_subdirectories( self.product_dir )

        for iPath in self._item_paths:
            product = Product( iPath )
            self.items.append( product )