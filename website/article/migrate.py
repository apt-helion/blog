#!/usr/bin/env python

import sys
from markdownify import markdownify as md

sys.path.append('/Users/justin/Documents/code/blog/website')
from common.models.main import *

if __name__ == '__main__':
    arts = Article.select()

    for first in arts:
        with open('./markdown/'+first.link+'.md', 'w+') as f:
            f.write(first.thumbnail+'\n\n')
            f.write(md(first.content))
