import urllib2
import re
import itertools
import sys
import time 

from bs4 import BeautifulSoup

listing_title = []
price_data = []
cl_data = {}


def getresults(query):
	
	global cl_data
	global listing_title
	global price_data

	def makesoup(address):
		req = urllib2.Request(address)
		page = urllib2.urlopen(req)
		soup = BeautifulSoup(page.read(), 'html.parser')
		return soup

	query = query.replace(" ", "_")
	url = 'https://raleigh.craigslist.org/search/sss?sort=priceasc&query={}'.format(str(query))
	results_found = makesoup(url).find("span", {"class" : "button pagenum"}).text

	if results_found != "no results":
		total_results = makesoup(url).find("span", {"class" : "totalcount"}).text
		print "Found {} results".format(total_results)
				
		if len(total_results) >= 1:
			
			if len(total_results) == 4:
				raw_total_results = total_results
				total_results = total_results[:2] + "00"
				total_results = int(total_results)
				more_results = True

			elif len(total_results) == 3:
				raw_total_results = total_results
				total_results = total_results[0] + "00"
				total_results = int(total_results)
				more_results = True

			elif len(total_results) <= 2:
				more_results = False
				listing_title = [link.text for link in makesoup(url).find_all("span", {"id" : "titletextonly"})]
				price_data = [str(price.text.strip("$")) \
	              			  for price in makesoup(url).find_all("span", {"class" : "price"})[::2]]
	        	cl_data = _makedic(listing_title, price_data)

			price_data = []
			listing_title = []
			scrape_total = raw_total_results
			scrape_count = 0
			
			while total_results >= 0 and more_results != False:
				url = 'https://raleigh.craigslist.org/search/sss?s={}&query={}&sort=priceasc'.format(total_results, str(query))
				price = makesoup(url).find_all("span", {"class" : "price"})[::2]
				title = makesoup(url).find_all("span", {"id" : "titletextonly"})
				print "Scraping url: \n{}".format(url)	
	   			for value in price: price_data.append(value.text.strip("$"))
	   			for name in title: listing_title.append(name.text)
	   			time.sleep(1)	   			
	   			total_results -= 100
	   			scrape_count += len(title)
	   			print "Scraped {}/{} items".format(scrape_count, scrape_total)
	   			if total_results == 0:
	   				url = 'https://raleigh.craigslist.org/search/sss?sort=priceasc&query={}'.format(str(query))
	   				price = makesoup(url).find_all("span", {"class" : "price"})[::2]
					title = makesoup(url).find_all("span", {"id" : "titletextonly"})
	   				print "Scraping url: \n{}".format(url)
	   				for value in price: price_data.append(value.text.strip("$"))
	   				for name in title: listing_title.append(name.text)
	   				cl_data = _makedic(listing_title, price_data)
	   				scrape_count += len(title)
	   				print "Scraped {}/{} items".format(scrape_count, scrape_total)
	   				break

	else:
		print "No results found"

def _makedic(title, price):
	"""	Called inside of getresults()
		Returns a dictionary with title as the key
	   	and price as the value. 
	""" 
	raw_dic = dict(itertools.izip(title, price))
	return raw_dic

def averageprice(price, lowhigh=None):
	""" Returns the average price from all elements in a list
	    or tuple.
	    Takes optional paramater of lowhigh that will print out
	    the lowest and highest price.
	"""	
	total = 0
	for value in price:
		total += int(value.strip("$"))
		print value
	print "Average price: ${}".format(total / len(price))
		
	if lowhigh:
		price = sorted(price, key=int)
		print "Low price: ${} \nHigh price: ${}".format(price[0], price[-1])

def filtered_data(dic, query):
	"""Filter results for a specfic string in
	   title.
	"""
	filtered_dic = {}

	for key, value in dic.items():
		if query.replace("_", " ") in key.lower():
			filtered_dic[key] = value
	return filtered_dic

def sortdata(dic, descending=None):
#Make it will where it return a sorted dictionary 
	if descending:
		return sorted(dic, key=int, reverse=True)
	else:
		return sorted(dic)

