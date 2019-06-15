import sys

from os import listdir, remove
from os.path import isfile, join

from pathlib import Path
from unittest import TestCase
from peewee import SqliteDatabase

test_path = Path(__file__).parent
bin_path = test_path.parent.parent / 'bin/'
web_path = test_path.parent.parent / 'website/'

sys.path.append(str(bin_path))
sys.path.append(str(web_path))

from updatedb import UpdateDB  # noqa
from common.mdtohtml import MDtoHTML  # noqa
from common.models.main import Article  # noqa
from common.database import dba  # noqa

# This needs it's own 'sandboxed' database to be in

# Setup database
DB_LOCATION = 'tests/blog.db'
DATABASE = SqliteDatabase(DB_LOCATION)

# Change dbs to this one
Article._meta.database = DATABASE
dba.database = DATABASE
UpdateDB.DATABASE = DATABASE

DATABASE.connect()
DATABASE.create_tables([ Article ])
UpdateDB.import_articles(testing=True)


class EmailProcessTest(TestCase):
    """Tests to make sure emails will be sent correctly if there is a new article"""

    def setUp(self):
        self.meta = "---\
            \ntitle: test\
            \ncategory: test\
            \ndate: 2000-02-08\
            \nthumbnail: test-thumb.png\
            \ntags: test\
            \ndescription: test\
            \n---\
        "

        self.mdp = str(MDtoHTML.MARKDOWN_PATH)
        self.test_link = self.mdp + '/test.md'

    def tearDown(self):
        try:
            remove(self.test_link)
            remove(DB_LOCATION)
        except OSError:
            pass

    def import_articles(self):
        article_db_num = Article.select().count()
        article_md_num = len([ f for f in listdir(self.mdp) if isfile(join(self.mdp, f)) ])

        new_article = UpdateDB.import_articles(testing=True)

        return new_article, article_db_num, article_md_num

    def test_will_email_correctly(self):
        new_article, article_db_num, article_md_num = self.import_articles()

        self.assertEqual( (article_md_num > article_db_num), new_article )
        self.assertEqual( (article_md_num == article_db_num), (not new_article) )

        if not new_article:
            # Test if new one is created
            with open(self.test_link, 'w+') as f:
                f.write(self.meta)

            new_article, article_db_num, article_md_num = self.import_articles()

            self.assertEqual( (article_md_num > article_db_num), new_article )
            self.assertEqual( (article_md_num == article_db_num), (not new_article) )
