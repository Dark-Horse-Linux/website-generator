import os
from src.ContentAbstraction import CompositeContent
from configparser import ConfigParser
import feedparser
from datetime import datetime
from time import mktime
import re

def get_top_level_subdirectories(path):
    try:
        entries = os.listdir(path)
        subdirectories = [os.path.join(path, entry) for entry in entries if os.path.isdir(os.path.join(path, entry))]
        return subdirectories
    except FileNotFoundError:
        print( "Error: The path '{0}' does not exist.".format( path ) )
        return []


class FeedEntry:
    def __init__(self, entry, parent_feed):
        self.title = entry
        self.url = entry['link']
        self.parent_feed = parent_feed

        if self.url.startswith("https://github.com"):
            self.is_commit_feed = True
        else:
            self.is_commit_feed = False

        if self.is_commit_feed:
            self.title = re.split('\/', self.url)[-1]
        else:
            self.title = entry['title']
        self.author = entry['author']
        self.summary = entry['summary']
        self.content = entry['content'][0]['value']

        try:
            self._date_raw = entry['published_parsed']
        except KeyError:
            self._date_raw = entry['updated_parsed']
        self._datetime_obj = datetime.fromtimestamp(mktime(self._date_raw))
        self.date = self._datetime_obj.strftime('%Y-%m-%d')

        self.tags = list()
        if not self.is_commit_feed:
            self._tags_raw = entry['tags']
            for raw_tag in self._tags_raw:
                self.tags.append(raw_tag['term'])
        else:
            self.tags = None

    def __repr__(self):
        return "FeedEntry(title={0})".format( self.title )


class Feed:
    def __init__( self, iPath ):
        self._metadata_file = os.path.join( iPath, 'metadata.ini' )

        metadata_parser = ConfigParser()
        metadata_parser.read(self._metadata_file)

        self.title = metadata_parser.get('feed', 'title')
        self.tags = metadata_parser.get('feed', 'tags')
        self.tag_filter = metadata_parser.getboolean('feed', 'tag_filter')
        self.feed_url = metadata_parser.get('feed', 'url')
        self.parent = metadata_parser.get('feed', 'parent')
        self.unique_name = metadata_parser.get('feed', 'name')

        feed_result = feedparser.parse(self.feed_url)
        self.children = None

        # fetch and parse feed
        try:
            self.subtitle = feed_result['feed']['subtitle']
        except KeyError:
            self.subtitle = ""

        self.site_url = feed_result['feed']['link']

        self._entries_raw = feed_result['entries']

        self.entries = list()
        for raw_entry in self._entries_raw:
            feed_entry = FeedEntry(raw_entry, parent_feed=self)
            if self.tag_filter:
                if [x in self.tags for x in feed_entry.tags if x in self.tags]:
                    self.entries.append( feed_entry )
            else:
                self.entries.append(feed_entry)

    def __repr__(self):
        return "Feed(title={0})".format( self.title )


class Feeds(CompositeContent):
    def __init__(self, config):
        super().__init__()
        self._feeds_dir = os.path.join(config.content_dir, 'feeds')
        self._item_paths = get_top_level_subdirectories(self._feeds_dir)

        for iPath in self._item_paths:
            feed = Feed(iPath)
            self.items.append(feed)

        self.sorted_entries = self.get_sorted_entries()

    def get_sorted_entries(self):
        all_entries = []
        for feed in self.items:
            all_entries.extend(feed.entries)

        sorted_entries = sorted(all_entries, key=lambda entry: entry.date, reverse=True)
        return sorted_entries

    def __repr__(self):
        return "Feeds(items={0})".format(len(self.items))