#!/usr/bin/env python

import sys

from os import listdir, getcwd, environ
from os.path import isfile, join
from pathlib import Path
from datetime import datetime

project_path = Path(__file__).parent
website_path = project_path.parent / 'website/'
sys.path.append(str(website_path))

from config import Config
from common.models.main import Article
from common.mdtohtml import MDtoHTML
from common.database import dba

from emailsubscribers import send_emails

MARKDOWN_PATH = 'website/article/markdown'

if __name__ == '__main__':
    table_exists = dba.scalar('SHOW TABLES LIKE "Articles"', [])
    articles_sot = [ MDtoHTML.convert_article(Path(f).stem) for f in listdir(MARKDOWN_PATH) if isfile(join(MARKDOWN_PATH, f)) ]

    if table_exists is not None:
        articles_bee = dba.dict('SELECT * FROM Articles', [])

        new_article = None

        for sot in articles_sot:
            new = True

            for bee in articles_bee:
                if sot['link'] == bee['link']:
                    new = False

                if sot['content'] != bee['content']:
                    sot['updated'] = datetime.now().strftime('%Y-%m-%d')
                else:
                    sot['updated'] = bee.get('updated') or bee['date']

            if new: new_article = sot

        dba.empty('DROP TABLE IF EXISTS Articles', [])

    Config.DATABASE.create_tables([Article])

    for article in articles_sot:
        Article.create_from_dict(article)

    if environ.get('PRODUCTION') and new_article is not None:
        send_emails(new_article['link'])
