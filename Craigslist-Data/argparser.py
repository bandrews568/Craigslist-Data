# Used to parse arguments off command line
import argparse


def parseargs():
    description = 'Easily scrape massive amounts of data off Craigslist'
    query_help_text = '''Enter a query or queries seperated by a space.
				 	NOTE: Any spaces in words need to be replaced with a
				 	underscore.'''
    url_help_text = '''Enter a url(s) seperated by a space.
					NOTE: Any spaces in words need to be replaced with a
				 	underscore.'''
    category_help_text = '''Enter a category or categories seperated by a space.
					NOTE: Any spaces in words need to be replaced with a
				 	underscore.'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-q', '--query', required=True, nargs='*',
                        help=query_help_text)

    parser.add_argument('-u', '--urls', required=True, nargs='*',
                        help=url_help_text)

    parser.add_argument('-cat', '--category', nargs='*', default='default',
                        help=category_help_text)

    return parser.parse_args()
