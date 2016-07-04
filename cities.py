#Used to make dictionary of cities

import re
import urllib2

from bs4 import BeautifulSoup

url = "https://www.craigslist.org/about/sites"
req = urllib2.Request(url)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page.read(), 'html.parser')
city_dic = {}

for link in soup.find_all('a'):
	if link.text:
		city_dic[link.text] = re.sub("//", "", link.get('href'))
	else:
		pass

print city_dic 
