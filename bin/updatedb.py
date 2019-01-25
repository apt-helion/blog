#!/usr/bin/env python

import sys
import itertools

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

if __name__ == '__main__':
    mdp = str(MDtoHTML.MARDOWN_PATH)

    table_exists = dba.scalar('SHOW TABLES LIKE "Articles"', [])
    articles_sot = [ MDtoHTML.convert_article(Path(f).stem) for f in listdir(mdp) if isfile(join(mdp, f)) ]

    if table_exists is not None:
        # Get old articles to see if stuff has changed
        articles_bee = dba.dict('SELECT * FROM Articles', [])
        new_article  = None

        for sot, bee in itertools.product(articles_sot, articles_bee):
            is_new = True

            if sot['link'] == bee['link']:
                is_new = False

                # Set updated field to today if content or desc is different
                # Else get old updated field, or date
                if sot['content'] != bee['content'] or sot['description'] != bee['description']:
                    sot['updated'] = datetime.now().strftime('%Y-%m-%d')
                else:
                    sot['updated'] = bee.get('updated') or bee['date']

            if is_new: new_article = sot

        dba.empty('DROP TABLE IF EXISTS Articles', [])

    # Create table from current Article model
    Config.DATABASE.create_tables([ Article ])

    # Add data from source of truth
    for article in articles_sot: Article.create_from_dict(article)

    if environ.get('PRODUCTION') and new_article is not None:
        send_emails(new_article['link'])
