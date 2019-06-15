from unittest import TestCase

from common.models.main import Article


class ArticleModelTest(TestCase):
    """Tests to make sure the Article model still works with current models"""

    def setUp(self):
        self.category = 'development'
        self.test_article_link = 'test_article'
        self.test_article = Article.create(link=self.test_article_link, title='Test Article')


    def tearDown(self):
        self.test_article.delete_instance()


    def test_get_article(self):
        article = Article.get_article(self.test_article_link)

        self.assertIsInstance(article, Article)
        self.assertEqual(article.title, 'Test Article')


    def test_get_category(self):
        articles = Article.get_category(self.category)

        for article in articles:
            self.assertEqual(article.category, self.category)
