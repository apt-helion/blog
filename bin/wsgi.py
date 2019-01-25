import os
import sys

sys.path.insert(0, '/var/www/blog.justinduch.com/env/lib/python3.6/site-packages')
sys.path.insert(0, '/var/www/blog.justinduch.com/env/src/simplerr')

from simplerr import dispatcher

site     = '/var/www/blog.justinduch.com/website'
hostname = 'localhost'
port     = 80
wsgi     = dispatcher.wsgi(site, hostname, port)

application = wsgi.make_app()
