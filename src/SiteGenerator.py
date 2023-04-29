import os
import shutil
from src.Page import Page
from src.Product import Product
from src.Tearoff import Tearoff
from src.Feed import Feed
from jinja2 import Environment, FileSystemLoader


def get_type(obj):
    return type(obj).__name__


class SiteGenerator:
    def __init__( self, config, content ):
        self.config = config

        # raw content with hierarchical associations set
        self.content = content.content.top_down

        # output directory where content is generated
        self.output_root_dir = self.config.artifact_root_dir

        # copy everything from content/rsrc to output/rsrc
        self.content_rsrc_src = os.path.join( self.config.content_dir, 'rsrc' )
        self.rsrc_dest = os.path.join( self.output_root_dir, 'rsrc' )
        self.copy_dir_contents( self.content_rsrc_src, self.rsrc_dest )

        # copy everything from themes/$theme_name/rsrc to output/rsrc
        self.theme_root_dir = os.path.join( self.config.theme_dir, self.config.theme_name )
        self.theme_rsrc = os.path.join( self.theme_root_dir, 'rsrc' )
        self.copy_dir_contents( self.theme_rsrc, self.rsrc_dest )

        # iterate through all content items and generate accordingly
        self.generate_content_loop( self.content )
        # allow for a landing page
        self.generate_index()

    def generate_content_loop(self, obj_list, original_obj_list=None):
        if original_obj_list is None:
            original_obj_list = obj_list
        for item in obj_list:
            self.generate_content_item( item, original_obj_list )
            if len(item.children) > 0:
                self.generate_content_loop(item.children, original_obj_list)

    def generate_index(self):
        env = Environment(
            loader=FileSystemLoader(self.theme_root_dir),
            extensions=['jinja2.ext.loopcontrols']
        )
        env.filters['get_type'] = get_type
        url_prefix = self.output_root_dir
        target_path = os.path.join(url_prefix, "index.html")
        index_tmpl = env.get_template('index.tmpl')
        index_content = index_tmpl.render(
            config=self.config
        )
        with open( target_path, "w" ) as output_file:
            output_file.write(index_content)

    def generate_content_item( self, content_item, all_content_items ):

        # child-only types are rendered as part of the parent type
        if isinstance( content_item, Feed ):
            return

        if isinstance( content_item, Tearoff ):
            return

        env = Environment(
            loader=FileSystemLoader(self.theme_root_dir),
            extensions=['jinja2.ext.loopcontrols']
        )
        env.filters['get_type'] = get_type
        relevant_tearoffs = list()
        relevant_feeds = list()

        url_prefix = self.output_root_dir
        target_path = os.path.join(url_prefix, content_item.unique_name + "/index.html" )

        if isinstance( content_item, Product ):
            url_prefix = os.path.join( url_prefix, 'products' )
            target_path = os.path.join( url_prefix, content_item.unique_name + "/index.html")
            content_tmpl = env.get_template('product.tmpl')
            for child in content_item.children:
                if isinstance( child, Tearoff ):
                    if child.parent == content_item.unique_name:
                        relevant_tearoffs.append(child)
                if isinstance( child, Feed ):
                    if child.parent == content_item.unique_name:
                        relevant_feeds.append( child )

        if isinstance( content_item, Page ):
            url_prefix = os.path.join( url_prefix, 'pages' )
            target_path = os.path.join( url_prefix, content_item.unique_name + "/index.html" )
            content_tmpl = env.get_template('page.tmpl')
            for child in content_item.children:
                if isinstance( child, Tearoff ):
                    if child.parent == content_item.unique_name:
                        relevant_tearoffs.append(child)
                if isinstance( child, Feed ):
                    if child.parent == content_item.unique_name:
                        relevant_feeds.append( child )

        all_entries = []
        for ifeed in relevant_feeds:
            all_entries.extend(ifeed.entries)
        sorted_entries = sorted(all_entries, key=lambda entry: entry.date, reverse=True)

        content_html = content_tmpl.render(
            config=self.config,
            all_content=all_content_items,
            tearoffs=relevant_tearoffs,
            feeds=relevant_feeds,
            sorted_feeds=sorted_entries,
            this_content=content_item
        )

        os.makedirs( os.path.dirname(target_path), exist_ok=True )
        with open( target_path, "w" ) as output_file:
            output_file.write(content_html)

    # preserves files in rsrc_dest that are not in rsrc_src to allow cascade merging by subsequent copying
    def copy_dir_contents(self, src, dst):

        if not os.path.exists( dst ):
            os.makedirs( dst )

        for root, dirs, files in os.walk(src):
            relative_path = os.path.relpath(root, src)
            dest_dir = os.path.join( dst, relative_path )

            for d in dirs:
                os.makedirs( os.path.join( dest_dir, d ), exist_ok=True )

            for f in files:
                shutil.copy2( os.path.join( root, f ), os.path.join( dest_dir, f ) )
