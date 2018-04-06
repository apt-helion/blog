#!conf/env/bin/python3.6

import sys
import os
import app as app
from bs4 import BeautifulSoup

# Remember to run this from the root directory of the site

def add_to_db(title, category, blurb, created):
	location = f'/articles/{filename}'

	conn = utils.setupDB()
	cur  = conn.cursor()
	cur.execute("INSERT INTO articles values (null, %s, %s, %s, %s ,%s)",
				[title, category, blurb, location, created])
	conn.commit()
	print(f'\nSuccess: {filename} added to database\n')

def main():
	# Check if filename is actually a file path because I do that sometimes ;)
	if len(re.split('/', filename)) > 2:
		filename = re.split('/', filename)[-1]

	location =  f'html/articles/{filename}'

	with open(location) as article:
		soup = BeautifulSoup(article, 'html.parser')

	title    = soup.find(id="title").get_text()    or sys.exit('\nError: Cant\'t find title\n')
	category = soup.find(id="category").get_text() or sys.exit('\nError: Cant\'t find category\n')
	blurb    = soup.find(id="fp").get_text()[:240] or sys.exit('\nError: Cant\'t find blurb\n')
	date     = soup.find(id="date").get_text()     or sys.exit('\nError: Cant\'t find date\n')

	created = date.split(" ")[1]

	if blurb[len(blurb)-1] is ' ':
		blurb = blurb[:-1] # Remove if there is a space char at the end

	add_to_db(title, category, blurb, created)


if __name__ == '__main__':
	try:
		filename = sys.argv[1]
	except:
		print("\nError: no file specified")
		print("Usage: cgi-bin/lib/add_to_db.py <filename>\n")
		sys.exit()

	utils = app.App(os.path.split(__file__), {})
	main()
