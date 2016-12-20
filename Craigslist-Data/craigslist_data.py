import os
import re
import sys
import time
import logging
import itertools
import urllib.request

from argparser import parseargs
from searchdata import ITEM_CATEGORY

from bs4 import BeautifulSoup


class CraigslistData:
    logger = logging.getLogger(__file__)
    logging.basicConfig(level=logging.ERROR and logging.INFO)

    def __init__(self, query, urls, category):
        self.query = query
        self.urls = urls
        self.category = category
        self.full_urls = []
        self.item_data = []

    def makesoup(self, url):
        try:
            request_page = urllib.request.Request(url)
            page = urllib.request.urlopen(request_page)
            soup = BeautifulSoup(page.read(), 'html.parser')
        except Exception as error:
            self.logger.error(error)
            raise
        return soup

    def checkcategory(self, category_list):
        if 'default' in category_list:
            pass
        else:
            for category in category_list:
                if not category in ITEM_CATEGORY:
                    self.logger.error('Invalid category: {}'.format(category))
                    return False
        return True

    def checkurls(self, url_list):
        check_valid_url = re.compile('https://(.*).craigslist.org')
        for url in url_list:
            if not check_valid_url.match(url):
                self.logger.error('Invalid URL: {}'.format(url))
                return False
        return True

    @property
    def valid_data(self):
        return self.checkurls(self.urls) and self.checkcategory(self.category)

    def makefullurls(self, url_list):
        assert self.valid_data

        default_url = '/search/sss?&query={query}&s='
        category_url = '/search/{category}?&query={query}&s='

        if 'default' in self.category:
            for url in url_list:
                for query in self.query:
                    full_default_url = url + default_url.format(query=query)
                    self.full_urls.append(full_default_url)
        else:
            # Cubic runtime--Fix this later!
            for url in url_list:
                for query in self.query:
                    for category in self.category:
                        full_url = url + category_url.format(category=category,
                                                             query=query)
                        self.full_urls.append(full_url)

    def checkresults(self, soup_object, url):
        check_results = soup_object.find(
            'span', {'class': 'button pagenum'}).text

        if check_results == 'no results':
            self.logger.info('No search results: ' + url)
            return 'no results'
        else:
            total_results = soup_object.find(
                'span', {'class': 'totalcount'}).text
            self.logger.info('Found {total} results: '.format(
                total=total_results) + url)
            rounded_down_total = self.roundtotaldown(total_results)
            return rounded_down_total

    def roundtotaldown(self, total_results):
        if len(total_results) == 4:
            rounded_down_total = int(total_results[:2] + '00')
        elif len(total_results) == 3:
            rounded_down_total = int(total_results[0] + '00')
        else:
            rounded_down_total = int(total_results)
        return rounded_down_total

    def scrapeitemdata(self, url, soup_object=None):
        if soup_object is None:
            soup_object = self.makesoup(url)

        title_info = soup_object.find_all('a', {'class': 'result-title hdrlnk'})
        price_info = soup_object.find_all('span', {'class': 'result-price'})[::2]
        url_info = soup_object.find_all('a', {'class': 'result-title hdrlnk'})

        title_list = []
        price_list = []
        url_list = []

        first_half_url = re.sub('/search/\w.+$', '', url)

        for title in title_info:
            title_list.append(title.text)

        for price in price_info:
            price_list.append(price.text)

        for url in url_info:
            second_half_url = url['href']
            full_item_url = first_half_url + second_half_url
            url_list.append(full_item_url)

        zip_data = zip(title_list, price_list, url_list)
        full_item_detail = list(zip_data)
        self.item_data.extend(full_item_detail)

    def scrapedata(self):
        self.makefullurls(self.urls)
        soup_objects = [(self.makesoup(url), url) for url in self.full_urls]

        for obj, url in soup_objects:
            total_results = self.checkresults(obj, url)
            if total_results == 'no results':
                continue
            elif total_results < 100:
                self.scrapeitemdata(url, soup_object=obj)
            else:
                remaining_results = total_results
                while remaining_results >= 0:
                    url += "{}".format(remaining_results)
                    self.scrapeitemdata(url)
                    url = re.sub('s=\d*$', 's=', url)
                    remaining_results -= 100

    def writetofile(self):
        filename = time.strftime('%m-%d-%Y_%H:%M.txt')

        with open(filename, 'w+') as file:
            for item in self.item_data:
                item = str(item) + '\n'
                file.write(item)

        results_location = os.getcwd()
        filename_location = 'File location: {}'.format(results_location)
        name_of_file = 'Filename: {}'.format(filename)
        self.logger.info(filename_location)
        self.logger.info(name_of_file)


if __name__ == '__main__':
    args = parseargs()
    craigslist_data = CraigslistData(args.query, args.urls, args.category)
    craigslist_data.scrapedata()
    craigslist_data.writetofile()
