import re
import sys
import time
import urllib2
import itertools

from citydict import CITY_DICT
from bs4 import BeautifulSoup

class CraigslistData(object):
	
	def __init__(self):
		self.query = sys.argv[1]
		self.og_query = sys.argv[1]
		self.user_city_dic = {}
		self.city_not_found = []
		self.title = []
		self.price = []
		self.link = []
		self.complete_list = []

	def makesoup(self, url):
		req = urllib2.Request(url)
		page = urllib2.urlopen(req)
		soup = BeautifulSoup(page.read(), 'html.parser')
		return soup
	
	def get_cities(self):
		if sys.argv[2].endswith(".txt"): 			
			try:
				with open(sys.argv[2], 'r') as f:
					user_cities = re.split(",", f.read().strip('\n').lower())
				for city in user_cities:
					if city in CITY_DICT:
						self.user_city_dic[city] = "https://" + CITY_DICT.get(city) + \
					    'search/sss?sort=priceasc&query={}&s='.format(str(self.query))

					elif city.startswith("https://") and city.endswith(".org"):
						strip_city = re.compile("https://(.*).craigslist.org") ASD 
						
						city_found = str(strip_city.findall(city)).strip("'[]'")
						self.user_city_dic[city_found] = city + \
													'/search/sss?sort' + \
								'=priceasc&query={}&s='.format(str(self.query))

					else:
						self.city_not_found.append(city)
			except:
				raise IOError("{} file not found".format(sys.argv[2]))
		
		else: #Got passed a list of cities from command line
			user_cities = sys.argv[2].lower().split(",")
			for city in user_cities:
				if city in CITY_DICT:
					self.user_city_dic[city] = "https://" + CITY_DICT.get(city) + \
					'search/sss?sort=priceasc&query={}&s='.format(str(self.query))

				else:
					self.city_not_found.append(city)
			
	def scrape_data(self):

		for key, value in self.user_city_dic.items():
			results_found = self.makesoup(value).find("span", \
							{"class" : "button pagenum"}).text
			
			if results_found != "no results":
				total_results = self.makesoup(value).find("span", \
								{"class" : "totalcount"}).text
				
				print 'Found {} results for "{}" in {}'.format(total_results, 
														self.og_query,
														key)

				if len(total_results):
					if len(total_results) == 4:
						raw_total = int(total_results[:2] + "00")
						more_pages = True

					elif len(total_results) == 3:
						raw_total = int(total_results[0] + "00")
						more_pages = True

					else:
						"""
						Craigslist will suggest results from nearby cities
						if there isn't many local results. Total results
						takes into account only the local area results. So
						we void out the extra nonlocal results by incrementing
						total_count to equal total_results then break the loop.
						Checking to see if the href starts with // will cancel 
						the links of the extra nonlocal results out.
						"""
						more_pages = False
						total_count = 0

						for listing in self.makesoup(value).find_all( \
										"span", {"id" : "titletextonly"}):
							if total_count != int(total_results):
								self.title.append(listing.text)
								total_count += 1
							elif total_count == int(total_results):
								break

						total_count = 0
						
						for amount in self.makesoup(value).find_all( \
									"span", {"class" : "price"})[::2]:
							if total_count != int(total_results):
								self.price.append(amount.text)
								total_count += 1
							elif total_count == int(total_results):
								break
						
						for url in self.makesoup(value).find_all( \
										"a", {"class": "hdrlnk"}):
							if url.get("href").startswith("//"):
								pass
							else:
								self.link.append("https://{}.".format(key) + \
										"craigslist.org" + url.get("href"))

				results_total = raw_total if more_pages else None
				
				while results_total >= 0 and more_pages:

					value = value + "{}".format(results_total)
					_title = self.makesoup(value).find_all( \
						"span", {"id" : "titletextonly"})
					_price = self.makesoup(value).find_all( \
						"span", {"class" : "price"})[::2] #prices repeat
					_link = self.makesoup(value).find_all( \
						"a", {"class": "hdrlnk"})

					print "Scraping url: {}".format(value)					
					
					for amount in _price:
						self.price.append(amount.text)

					for name in _title:
						self.title.append(name.text)

					for url in _link:
						self.link.append("https://{}.craigslist.org".format(key) + \
										url.get("href"))
								
					value = re.sub("s=\d*$", "s=", value)
					results_total -= 100
										
			else:
				print 'No results found for "{}" in {}'.format(self.og_query, key)

		if len(self.city_not_found):
			print "Couldn't find URL's for {}".format(self.city_not_found)

	def write_to_file(self):
		complete_list = zip(self.title, self.price, self.link)
		
		with open(time.strftime("%m-%d-%Y_%H:%M.txt"), "w+") as f:
			for line in complete_list:
				f.write(str(line) + "\n\n")
				
	def main(self):
		self.get_cities()
		self.scrape_data()
		self.write_to_file()

if __name__ == '__main__':	
	CraigslistData().main()
