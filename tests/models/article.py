# Imports {{{1
from unittest import TestCase

from common.models.main import Article
from datetime import date


class ArticleModelTest(TestCase):
    """Tests to make sure the Article model still works with current migration"""


    def setUp(self):
        self.category = 'development'
        self.test_article_link_wip = 'test_article_wip'
        self.test_article_link = 'test_article'

        self.test_article_wip = Article.create(link=self.test_article_link_wip, title='Test Article WIP')
        self.test_article = Article.create(link=self.test_article_link, title='Test Article', wip='no')


    def tearDown(self):
        self.test_article_wip.delete_instance()
        self.test_article.delete_instance()


    def test_get_article(self):
        article_wip = Article.get_article(self.test_article_link_wip)
        article = Article.get_article(self.test_article_link)

        self.assertEqual(article_wip, None)

        self.assertIsInstance(article, Article)
        self.assertEqual(article.title, 'Test Article')


    def test_get_category(self):
        articles = Article.get_category(self.category)

        for article in articles:
            self.assertEqual(article.category, self.category)
