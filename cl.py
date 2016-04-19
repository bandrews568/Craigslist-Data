#!/usr/bin/python

import urllib2

from bs4 import BeautifulSoup

#Get user query and replace all spaces with underscores
user_search = raw_input("Enter search: ").replace(" ", "_")

#Request variables 
url = 'https://raleigh.craigslist.org/search/sss?sort=rel&query={}'.format(str(user_search))
req = urllib2.Request(url)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page.read(), 'html.parser')


#Query lists
listing_title = [link.text for link in soup.find_all("span", {"id" : "titletextonly"})]

#Check for results
no_results = soup.find("span", {"class" : "button pagenum"}).text

if no_results == "no results":
	no_results = False
	print "No results found"

else: #Results were found
	results_found = soup.find("span", {"class" : "totalcount"}).text
	print "Found {} results".format(results_found)
	
	if len(results_found) >= 1:
		
		if len(results_found) == 4:
			results_found = results[:2] + "00"
			results_found = int(results_found)
			print results_found
		
		elif len(results_found) == 3:
			results_found = results_found[0] + "00"
			results_found = int(results_found)
			print results_found
	
	else:
		more_results = False 



item_price = soup.find_all("span", {"class" : "price"})
#Have to append every 2nd element because two prices are listed
#for every item and will throw off averages
price_data = [x.text.strip("$") for x in item_price[::2]]
print sorted(price_data, key=int)


#Example url for number of items (s={}).format(number_of_items)
#https://raleigh.craigslist.org/search/sss?s=100&query=iphone&sort=rel



