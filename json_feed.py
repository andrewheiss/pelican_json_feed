# -*- coding: utf-8 -*-
"""
JSON Feed Generator
===================

A Pelican plugin to generate a JSON Feed file
"""

from __future__ import unicode_literals

import json
from datetime import datetime
from jinja2 import Markup
from operator import attrgetter
from pelican import signals, generators, writers


class JSONFeed(object):
    TOP_LEVEL_TRANS = {'link': {'key': 'home_page_url'},
            'feed_url': {'key': 'feed_url'},
            'description': {'key': 'description', 'tr': Markup.striptags},
            'favicon': {'key': 'favicon'},
            'icon': {'key': 'icon'},
            'author': {'key': 'author', 'tr': lambda n: {'name': str(n)}}}
    ITEMS_TRANS = {'link': {'key': 'url'},
            'title': {'key': 'title'},
            'content': {'key': 'content_html'},
            'description': {'key': 'description', 'tr': Markup.striptags},
            'pubdate': {'key': 'date_published', 'tr': datetime.isoformat},
            'updateddate': {'key': 'date_modified', 'tr': datetime.isoformat},
            'categories': {'key': 'tags', 'tr': lambda c: [str(t) for t in c]},
            'author': {'key': 'author', 'tr': lambda n: {'name': str(n)}}}

    def __init__(self, title, **kwargs):
        self.feed = {"version": "https://jsonfeed.org/version/1",
                     "title": title, 'items': []}
        self._enrich_dict(self.feed, self.TOP_LEVEL_TRANS, kwargs)

    def _enrich_dict(self, dict_, translations, kwargs):
        for local_key, json_feed_spec in translations.items():
            if not kwargs.get(local_key):
                continue
            value = kwargs[local_key]
            if 'tr' in json_feed_spec:
                value = json_feed_spec['tr'](value)
            dict_[json_feed_spec['key']] = value

    def add_item(self, unique_id, **kwargs):
        item = {'id': unique_id}
        self._enrich_dict(item, self.ITEMS_TRANS, kwargs)
        self.feed['items'].append(item)

    def write(self, fp, encoding='utf-8'):
        json.dump(self.feed, fp, encoding)


class JSONFeedGenerator(generators.ArticlesGenerator):

    def generate_feeds(self, writer):
        """Generate the feeds from the current context, and output files."""

        if self.settings.get('FEED_JSON'):
            writer.write_feed(self.articles, self.context,
                              self.settings['FEED_JSON'], feed_type='json')

        if self.settings.get('FEED_ALL_JSON'):
            all_articles = list(self.articles)
            for article in self.articles:
                all_articles.extend(article.translations)
            all_articles.sort(key=attrgetter('date'), reverse=True)

            writer.write_feed(all_articles, self.context,
                              self.settings['FEED_ALL_JSON'], feed_type='json')

        for cat, arts in self.categories:
            arts.sort(key=attrgetter('date'), reverse=True)
            if self.settings.get('CATEGORY_FEED_JSON'):
                writer.write_feed(arts, self.context,
                        self.settings['CATEGORY_FEED_JSON'] % cat.slug,
                        feed_title=cat.name, feed_type='json')

        for auth, arts in self.authors:
            arts.sort(key=attrgetter('date'), reverse=True)
            if self.settings.get('AUTHOR_FEED_JSON'):
                writer.write_feed(arts, self.context,
                        self.settings['AUTHOR_FEED_JSON'] % auth.slug,
                        feed_title=auth.name, feed_type='json')

        if self.settings.get('TAG_FEED_JSON'):
            for tag, arts in self.tags.items():
                arts.sort(key=attrgetter('date'), reverse=True)
                writer.write_feed(arts, self.context,
                        self.settings['TAG_FEED_JSON'] % tag.slug,
                        feed_title=tag.name, feed_type='json')

        if self.settings.get('TRANSLATION_FEED_JSON'):
            translations_feeds = defaultdict(list)
            for article in chain(self.articles, self.translations):
                translations_feeds[article.lang].append(article)

            for lang, items in translations_feeds.items():
                items.sort(key=attrgetter('date'), reverse=True)
                if self.settings.get('TRANSLATION_FEED_JSON'):
                    writer.write_feed(items, self.context,
                            self.settings['TRANSLATION_FEED_JSON'] % lang,
                            feed_type='json')

    def generate_output(self, writer):
        self.generate_feeds(writer)


class JSONFeedWriter(writers.Writer, object):

    def _create_new_feed(self, feed_type, feed_title, context):
        if feed_type != 'json':
            return super(JSONFeedWriter, self)\
                    ._create_new_feed(feed_type, feed_title, context)
        if feed_title:
            feed_title = context['SITENAME'] + ' - ' + feed_title
        else:
            feed_title = context['SITENAME']

        feed = JSONFeed(title=Markup(feed_title).striptags(),
                        link=(self.site_url + '/'),
                        feed_url=self.feed_url,
                        author=context.get('AUTHOR'),
                        favicon=context.get('FAVICON'),
                        icon=context.get('SITELOGO'),
                        description=context.get('SITESUBTITLE', ''))
        return feed


def get_generators(generators):
    return JSONFeedGenerator


def get_writer(writer):
    return JSONFeedWriter


def register():
    signals.get_writer.connect(get_writer)
    signals.get_generators.connect(get_generators)
