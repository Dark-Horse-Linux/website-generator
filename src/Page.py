from configparser import ConfigParser
import os
import markdown
from src.ContentAbstraction import CompositeContent
import uuid

def get_top_level_subdirectories(path):
    try:
        entries = os.listdir(path)
        subdirectories = [os.path.join(path, entry) for entry in entries if os.path.isdir(os.path.join(path, entry))]
        return subdirectories
    except FileNotFoundError:
        print( "Error: The path '{0}' does not exist.".format( path ) )
        return []


# reads a page from the pages_dir
# a page draws its:
# - content from a markdown file named 'content.md'
# - metadata from an ini file named 'metadata.ini'
class Page:
    def __init__( self, page_dir, config ):
        self.hash = uuid.uuid4().hex
        self._metadata_file = os.path.join( page_dir, 'metadata.ini' )
        self._markdown_file = os.path.join( page_dir, 'content.md' )

        metadata_parser = ConfigParser()
        metadata_parser.read( self._metadata_file )

        # the title of the page
        self.title = metadata_parser.get( 'metadata', 'title' )

        # a unique identifier for each page
        self.unique_name = metadata_parser.get( 'metadata', 'uid' )

        # the unique_name property for the parent page object
        self.parent = metadata_parser.get( 'metadata', 'parent' )

        # the intended url of the generated page, relative to config.artifact_root_dir
        self.url = "../../pages/{0}".format( self.unique_name )

        self._raw_markdown = self.get_raw_markdown(self._markdown_file)
        self.html_content = markdown.markdown(self._raw_markdown)
        self.children = None


    def get_raw_markdown( self, filename ):
        with open( filename, 'r' ) as markdown_file:
            markdown_string = markdown_file.read()
        return markdown_string

    def __str__(self):
        return "Page(title={0})".format( self.title )

    def __repr__(self):
        return "Page(title={0})".format( self.title )


# a self-loading collection of pages
class Pages(CompositeContent):
    def __init__( self, config ):
        super().__init__()
        self.pages_dir = os.path.join(config.content_dir, 'pages')
        self._item_paths = get_top_level_subdirectories(self.pages_dir)

        for iPath in self._item_paths:
            page = Page( iPath, config )
            self.items.append(page)
