# Craigslist-Data
Easily scrape massive amounts of data off Craigslist using Python and Beautiful Soup.
## Features 
~Supports scraping data from all 728 Craigslist cities

~Search for mulitiple queires

~Search for queires in specfic categories

~Saves all scraped data in a .txt file in the current directory 
## Requirements
Python 3.X.X 

`https://www.python.org/downloads/`

Beautiful Soup 4

`pip install beautifulsoup4`

## Usage
![alt tag](https://raw.githubusercontent.com/bandrews568/Craigslist-Data/master/usage1.png)
**Examples**
![alt tag](https://raw.githubusercontent.com/bandrews568/Craigslist-Data/master/usage2.png)

```python
from craigslist_data import CraigslistData

queries = ["iphone6", "macbook_pro"]
urls = ["https://raleigh.craigslist.org"]
category = ["i"]

craigslist_data = CraigslistData(queries, urls, category)
# Scrape data for all queires and categories.
craigslist_data.scrapedata()
# Access all the item data
# item_data is a list of tuples
craigslist_data.item_data
# Save data to a txt file in the current directory
craigslist_data.writetofile()
```



**IMPORTANT**

Any spaces entered on command line must be replaced with an underscore
