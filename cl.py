import urllib2
import re
import itertools
import sys
import time 

from bs4 import BeautifulSoup

listing_title = []
price_data = []


def getresults(query):
	
	global listing_title
	global price_data	

	query = query.replace(" ", "_")
	url = 'https://raleigh.craigslist.org/search/sss?sort=priceasc&query={}'.format(str(query))
	req = urllib2.Request(url)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page.read(), 'html.parser')
	
	results_found = soup.find("span", {"class" : "button pagenum"}).text

	if results_found != "no results":
		total_results = soup.find("span", {"class" : "totalcount"}).text
		print "Found {} results".format(total_results)
				
		if len(total_results) >= 1:
			
			if len(total_results) == 4:
				total_results = total_results[:2] + "00"
				total_results = int(total_results)
				more_results = True

			elif len(total_results) == 3:
				total_results = total_results[0] + "00"
				total_results = int(total_results)
				more_results = True

			elif len(total_results) <= 2:
				more_results = False
				listing_title = [link.text for link in soup.find_all("span", {"id" : "titletextonly"})]
				price_data = [str(price.text.strip("$")) \
	              			  for price in soup.find_all("span", {"class" : "price"})[::2]]

			price_data = []
			listing_title = []
			
			while total_results >= 0 and more_results != False:
				url = 'https://raleigh.craigslist.org/search/sss?s={}&query={}&sort=priceasc'.format(total_results, str(query))
				req = urllib2.Request(url)
				page = urllib2.urlopen(req)
				soup = BeautifulSoup(page.read(), 'html.parser')
				price = soup.find_all("span", {"class" : "price"})[::2]
				title = soup.find_all("span", {"id" : "titletextonly"})
				print "Scraping url: \n{}".format(url)		
	   			for value in price: price_data.append(value.text.strip("$"))
	   			for name in title: listing_title.append(name.text)
	   			time.sleep(1)	   			
	   			total_results -= 100
	   			if total_results == 0:
	   				url = 'https://raleigh.craigslist.org/search/sss?sort=priceasc&query={}'.format(str(query))
	   				print "Scraping url: \n{}".format(url)
	   				for value in price: price_data.append(value.text.strip("$"))
	   				for name in title: listing_title.append(name.text)
	   				break


	else:
		return "No results found"

def averageprice(price):
	"""Returns the average price"""
	
	total = 0
	for price in price_data:
		total += int(price.strip("$"))
	print "Average price: ${}".format(total / len(price_data))
	price = sorted(price, key=int)
	print "Low price: ${} \nHigh price: ${}".format(price[1], price[-1])

def rawdata(title, price):
	
	raw_dic = dict(itertools.izip(title, price))
	return raw_dic

def filtered_data(title, price, query):
	
	unfilered_dic = dict(itertools.izip(title, price))
	filtered_dic = {}

	for key, value in unfilered_dic.items():
		if query.replace("_", " ") in key.lower():
			filtered_dic[key] = value
	return filtered_dic

def sortdata(price, highlow=None):
	
	if highlow == True:
		return sorted(price, key=int, reverse=True)
	else:
		return sorted(price, key=int)

getresults("iphone 5")
print len(price_data)