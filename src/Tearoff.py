from configparser import ConfigParser
from src.ContentAbstraction import CompositeContent
import os

def get_top_level_subdirectories( path ):
    try:
        entries = os.listdir( path )
        subdirectories = [ os.path.join( path, entry ) for entry in entries if os.path.isdir( os.path.join( path, entry ) ) ]
        return subdirectories
    except FileNotFoundError:
        print( "Error: The path '{0}' does not exist.".format( path ) )
        return []


class Tearoff:
    def __init__( self, tearoff_dir ):
        self.metadata_file = os.path.join( tearoff_dir, 'metadata.ini' )

        metadata_parser = ConfigParser()
        metadata_parser.read( self.metadata_file )

        self.title = metadata_parser.get( 'tearoff', 'title' )
        self.content = metadata_parser.get( 'tearoff', 'content' )
        self.link_title = metadata_parser.get( 'tearoff', 'link_title' )
        self.link_url = metadata_parser.get( 'tearoff', 'link_url' )
        self.unique_name = metadata_parser.get( 'tearoff', 'name' )

        # parent.unique_name
        self.parent = metadata_parser.get( 'tearoff', 'parent' )
        self.children = list()

    def __str__(self):
        return str( self.unique_name )

    def __repr__(self):
        return "Tearoff(title={0}, parent={1})".format( self.title, self.parent )


class Tearoffs(CompositeContent):
    def __init__( self, config ):
        super().__init__()
        self.tearoff_dir = os.path.join( config.content_dir, 'tearoffs' )
        self._item_paths = get_top_level_subdirectories( self.tearoff_dir )

        for iPath in self._item_paths:
            tearoff = Tearoff( iPath )
            self.items.append( tearoff )