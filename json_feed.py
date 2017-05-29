# -*- coding: utf-8 -*-
"""
JSON Feed Generator
===================

A Pelican plugin to generate a JSON Feed file
"""

from __future__ import unicode_literals

import json
from jinja2 import Markup
from operator import attrgetter
from pelican import signals, generators, writers


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
                                self.settings['FEED_ALL_JSON'],
                                feed_type='json')

        for cat, arts in self.categories:
            arts.sort(key=attrgetter('date'), reverse=True)
            if self.settings.get('CATEGORY_FEED_JSON'):
                writer.write_feed(arts, self.context,
                                  self.settings['CATEGORY_FEED_JSON']
                                  % cat.slug, feed_title=cat.name,
                                  feed_type='json')

        for auth, arts in self.authors:
            arts.sort(key=attrgetter('date'), reverse=True)
            if self.settings.get('AUTHOR_FEED_JSON'):
                writer.write_feed(arts, self.context,
                                  self.settings['AUTHOR_FEED_JSON']
                                  % auth.slug, feed_title=auth.name,
                                  feed_type='json')

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
                    writer.write_feed(
                        items, self.context,
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



class JSONFeed(object):

    def __init__(self, title, link, feed_url,
            author, favicon, icon, description):
        self.feed = {"version": "https://jsonfeed.org/version/1",
                     "title": title,
                     "home_page_url": link,
                     "feed_url": feed_url,
                     "description": description,
                     "items": []}
        if author:
            self.feed['author'] = {'name': author}
        if favicon:
            self.feed['favicon'] = favicon
        if icon:
            self.feed['icon'] = icon

    def add_item(self, title, link, unique_id, description,
            content, categories, author_name, pubdate, updateddate):

        item = {'id': unique_id,
                'url': link,
                'title': title,
                'content_html': content,
                'description': description,
                'date_published': pubdate.isoformat(),
                'tags': [str(cat) for cat in categories],
                'author': {'name': str(author_name)}}
        if updateddate:
            item['date_modified'] = updateddate.isoformat()
        self.feed['items'].append(item)

    def write(self, fp, encoding='utf-8'):
        json.dump(self.feed, fp, encoding)


def get_generators(generators):
    return JSONFeedGenerator


def get_writer(writer):
    return JSONFeedWriter


def register():
    signals.get_writer.connect(get_writer)
    signals.get_generators.connect(get_generators)
