"""
Pokemon world regions crawler
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


import re
import requests
import bs4 as bs
from .base import BaseCrawler


URL = 'https://en.wikipedia.org/wiki/Pok%C3%A9mon_universe'
DATA_COLUMNS = ['generation', 'name']
OUTPUT_FILE = 'pokemon_regions.json'

class RegionCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(DATA_COLUMNS, OUTPUT_FILE)
    
    def run(self):
        page = requests.get(URL) 
        soup = bs.BeautifulSoup(page.content, 'html.parser')
        contents_div = soup.find(id='toc')
        regions_uls = contents_div.find('ul').find('ul')
        for index, li in enumerate(regions_uls.find_all('li')):
            self.update_data([[index+1, re.search('[a-zA-Z]+', li.text).group()]])
        self.save()