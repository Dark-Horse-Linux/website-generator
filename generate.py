from src.Config import Config
from src.ContentLoader import ContentLoader
from src.SiteGenerator import SiteGenerator


def main():
    config = Config('config.ini')
    content = ContentLoader( config )
    generator = SiteGenerator( config, content )


if __name__ == '__main__':
    main()
