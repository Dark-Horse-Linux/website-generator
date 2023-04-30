import os
from configparser import ConfigParser


class Site:
    def __init__( self, config ):
        self._config = config
        self._site_parser = ConfigParser()

        site_config_file = os.path.join( config.content_dir, 'site.ini' )
        self._site_parser.read(site_config_file)

        self.logo_path = self._site_parser.get('main', 'logo')
        self.title = self._site_parser.get( 'main', 'title')
        self.landing = self._site_parser.get( 'main', 'landing')
        self.owner = self._site_parser.get('main', 'owner')


# paths can be provided as relative paths or absolute paths
class Config:
    def __init__(self, filename ):
        self._parser = ConfigParser(allow_no_value=True)
        self._parser.read(filename)

        self.theme_dir = self._parser.get("themes", "theme_dir")
        self.theme_name = self._parser.get("themes", "theme")

        self.content_dir = self._parser.get("general", "content_dir")
        self.artifact_root_dir = self._parser.get('output', 'artifact_root_dir')

        # convert all paths to absolute paths
        self.theme_dir = os.path.abspath( self.theme_dir )
        self.content_dir = os.path.abspath( self.content_dir )
        self.artifact_root_dir = os.path.abspath( self.artifact_root_dir )

        self.site = Site( self )