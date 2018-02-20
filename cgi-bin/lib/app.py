#!/usr/bin/env python3.6

#Modules for CGI and Templating 
from __future__ import print_function
import sys
import os
import cgi, cgitb
import jinja2
import json
import MySQLdb

class App:
	# Main Func
	def __init__(self, callingFile, stash, *args, **kwargs):
		self.callingFile = callingFile
		self.stash       = stash

	def escapejs(input):
		if input:
			return input.replace("'", "\\'")
		return ''

	# Renders page - stash is an object that will contain all variables to be passed to jinja
	def render(self):
		fileName = "templates/" + self.callingFile[1]
		jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader(self.callingFile[0]), autoescape=True)
		jinja_env.filters['escapejs'] = App.escapejs
		print("content-type:text/html\n\n")
		print(jinja_env.get_template(fileName).render(stash=self.stash))

	def render_json(self, out={}):
		print("Content-Type: application/json\n\n")
		print(json.dumps(out))

	def render_redirect(self, fileName='Location:/login\n\n'):
		print("Status: 301 Redirect")
		print(fileName)

	# Main Func End

	# Utils
	@staticmethod
	def setupDB():
		projectRoot = os.path.realpath(os.path.dirname(__file__))
		jsonUrl = os.path.join(projectRoot, 'database.json')
		data = json.load(open(jsonUrl))
		conn = MySQLdb.connect(host=data['host'], user=data['user'], passwd=data['passwd'], db=data['db'])
		return conn

	# Utils
	@staticmethod
	def eprint(*args, **kwargs):
		print(*args, file=sys.stderr, **kwargs)

	@staticmethod
	def print_headers(headers):
		for key in headers.keys():
			print(key +": "+headers[key]+"\n")
		print("\n")

	# Utils End

