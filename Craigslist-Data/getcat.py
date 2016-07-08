#Used to scrape category links

import urllib2

from bs4 import BeautifulSoup

url = "https://raleigh.craigslist.org/"
req = urllib2.Request(url)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page.read(), 'html.parser')
category_list = []

for link in soup.find_all('a'):
	if link.get("data-cat"):	
		category_list.append(link.get("data-cat").replace(" ", "_"))

print category_list

