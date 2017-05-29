# Pelican JSON Feed

This [Pelican](http://docs.getpelican.com/en/stable/) plugin generates a simple feed file that follows the [1.0 spec](https://jsonfeed.org/version/1) of the [JSON Feed standard](https://jsonfeed.org/).

## Installation

Make the following changes to `pelicanconf.py`:

1. Place the plugin directory in a path that's accessible in `PLUGIN_PATHS`:

        PLUGIN_PATHS = ['/path/to/all/plugins/here']  # Put this there
        PLUGIN_PATHS = ['/existing/path', '/path/to/this/plugin']  # Or just add it to the list

2. Include `json_feed` in the list of enabled plugins:

        PLUGINS = ['pelican_json_feed']

3. Configure the JSON feed like you'd configure the RSS or Atom ones:
          
        # available configuration variable are :
        # FEED_JSON, FEED_ALL_JSON, CATEGORY_FEED_JSON, AUTHOR_FEED_JSON   
        # TAG_FEED_JSON, TRANSLATION_FEED_JSON
        
        FEED_ALL_JSON = 'feeds/all.json'                                                
        CATEGORY_FEED_JSON = 'feeds/%s.json'
        
## Usage

When the plugin is enabled it'll write the feeds where you told it to through the above configuration variables. Add a links to those feeds in the head of your HTML:

    <link rel="alternate" type="application/json" title="JSON Feed" href="https://www.example.com/feeds/all.json">
    <link rel="alternate" type="application/json" title="JSON Feed" href="https://www.example.com/feeds/my_category.json">

