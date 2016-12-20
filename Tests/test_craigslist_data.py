import unittest

from craigslist_data import CraigslistData


class TestCraigslistData(unittest.TestCase):
    def setUp(self):
        self.query = ['iphone7', 'iphone6']
        self.urls = [
            'https://raleigh.craigslist.org',
            'https://topeka.craigslist.org'
        ]
        self.invalid_url = ['raleigh.craigslist.org']
        self.valid_category = ['ccc', 'act']
        self.invalid_category = ['ccc', 'invalid']
        self.default_category = ['default']
        self.craigslist_data = CraigslistData(self.query,
                                              self.urls,
                                              self.valid_category)
        self.craigslist_data_default = CraigslistData(self.query,
                                                      self.urls,
                                                      self.default_category)

    def test_checkcategory_default(self):
        craigslist_data = self.craigslist_data_default
        check_category = craigslist_data.checkcategory(self.default_category)
        self.assertTrue(check_category)

    def test_checkcategory_valid(self):
        craigslist_data = self.craigslist_data_default
        check_category = craigslist_data.checkcategory(self.valid_category)
        self.assertTrue(check_category)

    def test_checkcategory_invalid(self):
        craigslist_data = CraigslistData(self.query,
                                         self.urls,
                                         self.invalid_category)
        check_category = craigslist_data.checkcategory(self.invalid_category)
        self.assertFalse(check_category)

    def test_checkurls_valid(self):
        craigslist_data = self.craigslist_data
        check_urls = craigslist_data.checkurls(self.urls)
        self.assertTrue(check_urls)

    def test_checkurls_invalid(self):
        craigslist_data = self.craigslist_data
        check_urls = craigslist_data.checkurls(self.invalid_url)
        self.assertFalse(check_urls)

    def test_makefullurls_default(self):
        craigslist_data = self.craigslist_data_default
        valid_url_default = [
            'https://raleigh.craigslist.org/search/sss?&query=iphone7&s=',
            'https://raleigh.craigslist.org/search/sss?&query=iphone6&s=',
            'https://topeka.craigslist.org/search/sss?&query=iphone7&s=',
            'https://topeka.craigslist.org/search/sss?&query=iphone6&s=',
        ]
        craigslist_data.makefullurls(self.urls)
        self.assertEqual(craigslist_data.full_urls, valid_url_default)

    def test_makefullurls_category(self):
        craigslist_data = self.craigslist_data
        valid_url_category = [
            'https://raleigh.craigslist.org/search/ccc?&query=iphone7&s=',
            'https://raleigh.craigslist.org/search/act?&query=iphone7&s=',
            'https://raleigh.craigslist.org/search/ccc?&query=iphone6&s=',
            'https://raleigh.craigslist.org/search/act?&query=iphone6&s=',
            'https://topeka.craigslist.org/search/ccc?&query=iphone7&s=',
            'https://topeka.craigslist.org/search/act?&query=iphone7&s=',
            'https://topeka.craigslist.org/search/ccc?&query=iphone6&s=',
            'https://topeka.craigslist.org/search/act?&query=iphone6&s=',
        ]
        craigslist_data.makefullurls(self.urls)
        self.assertEqual(craigslist_data.full_urls, valid_url_category)

    def test_roundtotaldown(self):
        craigslist_data = self.craigslist_data
        round_total_down = craigslist_data.roundtotaldown
        self.assertEqual(round_total_down('1234'), 1200)
        self.assertEqual(round_total_down('999'), 900)
        self.assertEqual(round_total_down('59'), 59)


if __name__ == '__main__':
    unittest.main()
