#!/usr/bin/python

import urllib2
import re 

from bs4 import BeautifulSoup

#Get user query and replace all spaces with underscores
user_search = raw_input("Enter search: ").replace(" ", "_")


number_of_items = raw_input("Results to include: ")


	
#Check to see if user entered a number
if len(number_of_items) == 0:
	number_of_items = False 

#Craigslist limits searches to 2500 max results
elif int(number_of_items) > 2500 and number_of_items != False:
	print "Max results is 2500"
	number_of_items = 2500

#Fix this to where a number will be rounded down. Example 138 to 100 or 243 to200 
elif number_of_items.isdigit() == True:
	if len(number_of_items) == 4:
		number_of_items = number_of_items[:2] + "00"
		number_of_items = int(number_of_items)
		print number_of_items
	else:
		number_of_items = number_of_items[:2] + "0"
		number_of_items = int(number_of_items)
		print number_of_items

 



#Request variables 
url = 'https://raleigh.craigslist.org/search/sss?sort=rel&query={}'.format(str(user_search))
req = urllib2.Request(url)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page.read(), 'html.parser')


#Query lists
listing_title = [link.text for link in soup.find_all("span", {"id" : "titletextonly"})]

#Check if results were found
no_results = soup.find("span", {"class" : "button pagenum"}).text

if no_results == "no results":
	no_results = False
	print "No results found"

else:
	results_found = soup.find("span", {"class" : "totalcount"}).text
	print "Found {} results".format(results_found)



item_price = soup.find_all("span", {"class" : "price"})
#price_data = item_price[:]

#Have to append every 2nd element because two prices are listed
#for every item and will throw off averages
price_data = [x.text.strip("$") for x in item_price[::2]]
print sorted(price_data, key=int)


#Example url for number of items (s={}).format(number_of_items)
#https://raleigh.craigslist.org/search/sss?s=100&query=iphone&sort=rel

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

