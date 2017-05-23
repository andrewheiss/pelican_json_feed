# -*- coding: utf-8 -*-
"""
JSON Feed Generator
===================

A Pelican plugin to generate a JSON Feed file
"""

from __future__ import unicode_literals

import os.path
import json
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from codecs import open
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from pelican import signals

def format_date(date):
    if date.tzinfo:
        tz = date.strftime('%z')
        tz = tz[:-2] + ':' + tz[-2:]
    else:
        tz = "-00:00"
    return date.strftime("%Y-%m-%dT%H:%M:%S") + tz

class JSONFeedGenerator(object):

    def __init__(self, context, settings, path, theme, output_path, *null):

        self.output_path = output_path
        self.context = context
        self.now = datetime.now()
        self.siteurl = settings.get('SITEURL')
        self.author = settings.get('AUTHOR')
        self.feed_title = settings.get('SITENAME')
        self.feed_description = settings.get('JSON_FEED_DESCRIPTION')
        self.feed_icon = settings.get('JSON_FEED_ICON')
        self.json_nodes = []

        self.default_timezone = settings.get('TIMEZONE', 'UTC')
        self.timezone = getattr(self, 'timezone', self.default_timezone)
        self.timezone = timezone(self.timezone)

    def create_json_node(self, page):

        if getattr(page, 'status', 'published') != 'published':
            return

        soup_title = BeautifulSoup(page.title.replace('&nbsp;', ' '), 'html.parser')
        page_title = soup_title.get_text(' ', strip=True)

        soup_text = BeautifulSoup(page.content, 'html.parser')
        page_text = str(soup_text)

        page_url = self.siteurl + '/' + page.url

        page_date = getattr(page, 'date', self.now)

        node = {'id': page_url,
                'url': page_url,
                'title': page_title,
                'content_html': page_text,
                'date_published': format_date(page_date),
                'author': {'name': self.author}
                }

        self.json_nodes.append(node)

    def generate_output(self, writer):
        path = os.path.join(self.output_path, 'feed.json')

        pages = self.context['articles']

        for article in self.context['articles']:
            pages += article.translations

        for page in pages:
            self.create_json_node(page)

        feed = {'version': 'https://jsonfeed.org/version/1',
                'title': self.feed_title,
                'home_page_url': self.siteurl,
                'feed_url': self.siteurl + '/feed.json',
                'description': self.feed_description,
                'icon': self.feed_icon,
                'items': self.json_nodes}

        with open(path, 'w', encoding='utf-8') as fd:
            json.dump(feed, fd, indent=4, ensure_ascii=False)


def get_generators(generators):
    return JSONFeedGenerator


def register():
    signals.get_generators.connect(get_generators)
