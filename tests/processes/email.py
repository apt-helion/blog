import sys

from pathlib import Path
from unittest import TestCase

test_path = Path(__file__).parent
bin_path  = test_path.parent.parent / 'bin/'
web_path  = test_path.parent.parent / 'website/'

sys.path.append(str(bin_path))
sys.path.append(str(web_path))

from updatedb import import_articles
from common.models.main import Article
from common.mdtohtml import MDtoHTML


TEST_META = """
---
title: test
category: test
date: 0000-00-00
thumbnail: test-thumb.png
tags: test
description: test
---
"""


class EmailProcessTest(TestCase):
    """Tests to make sure emails will be sent correctly"""

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_will_email(self):
        pass


    def test_will_not_email(self):
        pass
