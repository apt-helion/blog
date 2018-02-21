#!conf/env/bin/python3.6

import sys
import os
import app as app
from bs4 import BeautifulSoup

def add_to_db(title, category, blurb, created):
	location = f'/articles/{filename}'

	conn = utils.setupDB()
	cur  = conn.cursor()
	cur.execute("INSERT INTO articles values (null, %s, %s, %s, %s ,%s)",
				[title, category, blurb, location, created])
	conn.commit()
	print(f'{sys.argv[1]} added to database')

def main():
	location = f'html/articles/{filename}'

	with open(location) as article:
		soup = BeautifulSoup(article, 'html.parser')

	title    = soup.find(id="title").get_text()
	category = soup.find(id="category").get_text()
	blurb    = soup.find(id="fp").get_text()[:240]
	date     = soup.find(id="date").get_text()

	created = date.split(" ")[1]

	add_to_db(title, category, blurb, created)


if __name__ == '__main__':
	try:
		filename = sys.argv[1]
		utils = app.App(os.path.split(__file__), {})
		main()
	except:
		print("\nError: no file specified")
		print("Usage: cgi-bin/lib/add_to_db.py <filename>\n")

