import sys

"""Test Application
Use this section for diagnosing apache issues, uncomment the following
section, and comment out everything after `from simpler..`
"""
# def test_application(environ, start_response):
#     status = '200 OK'
#
#     output = u''
#     output += u'sys.version = %s\n' % repr(sys.version)
#     output += u'sys.prefix = %s\n' % repr(sys.prefix)
#     output += u'sys.path = %s\n' % repr(sys.path)
#
#     response_headers = [('Content-type', 'text/plain'),
#                         ('Content-Length', str(len(output)))]
#     start_response(status, response_headers)
#
#     return [output.encode('UTF-8')]
#
# application = test_application


"""Setup the simplerr wsgi application
Comment out everything below this to run the test_application instead.
"""
from simplerr import dispatcher
site = '/var/www/blog.justinduch.com/website'
hostname = 'localhost'
port = 80
wsgi = dispatcher.wsgi(site, hostname, port)
application = wsgi.make_app()
