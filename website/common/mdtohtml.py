#!/usr/bin/env python

from markdown2 import markdown
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path


class MDtoHTML(object):

    _path = Path( __file__ ).parent
    MARKDOWN_PATH = _path / '../../articles'

    MD_EXTRAS = {
        'code-friendly' : None,
        'header-ids' : None,

        'html-classes' : {
            'img': 'img-responsive'
        },

        # https://meta.stackexchange.com/questions/72877/whats-the-exact-syntax-for-spoiler-markup/72878#72878
        'spoiler' : None,

        # https://github.com/trentm/python-markdown2/wiki/fenced-code-blocks
        'fenced-code-blocks' : {
            # TODO: get linenos to overflow properly when table text goes over width
            # 'linenos' : True
        },

        # https://blog.justinduch.com/article/babys_first_fork
        "iframes": {
            'width': '100%',
            'height': '380',
        },

        'target-blank-links': None,
        'metadata': None,
        'wiki-tables': None,
        'strike': None,
        'footnotes': None,
    }


    @staticmethod
    def _get_md_article(link):
        with open(str( MDtoHTML.MARKDOWN_PATH / f'{link}.md' ), 'r') as f:
            content = f.read()

        return content


    @staticmethod
    def convert_article(link):
        content = MDtoHTML._get_md_article(link)
        md      = markdown( content, extras=MDtoHTML.MD_EXTRAS )
        # html    = BeautifulSoup( markdown(md), features="html.parser" )

        article = {
            'link'        : link,
            'title'       : md.metadata['title'],
            'category'    : md.metadata['category'],
            'date'        : datetime.strptime(md.metadata['date'], "%Y-%m-%d"),
            'thumbnail'   : md.metadata['thumbnail'],
            'tags'        : md.metadata['tags'],
            'description' : md.metadata['description'],
            'content'     : md,
        }

        return article
