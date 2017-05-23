# Pelican JSON Feed

This [Pelican](http://docs.getpelican.com/en/stable/) plugin generates a simple feed file that follows the [1.0 spec](https://jsonfeed.org/version/1) of the [JSON Feed standard](https://jsonfeed.org/).

## Installation

Make the following changes to `pelicanconf.py`:

1. Place the plugin directory in a path that's accessible in `PLUGIN_PATHS`:

        PLUGIN_PATHS = ['/path/to/all/plugins/here']  # Put this there
        PLUGIN_PATHS = ['/existing/path', '/path/to/this/plugin']  # Or just add it to the list

2. Include `json_feed` in the list of enabled plugins:

        PLUGINS = ['pelican_json_feed']

3. Configure the feed's description and icon:

        JSON_FEED_DESCRIPTION = "Description of feed/site goes here"
        JSON_FEED_ICON = "http://www.example.com/icon.png"

## Usage

When the plugin is enabled, a `feed.json` file will be placed in the root of the output folder when the site is generated. Add a link to this feed in the head of your HTML:

    <link rel="alternate" type="application/json" title="JSON Feed" href="https://www.example.com/feed.json">
