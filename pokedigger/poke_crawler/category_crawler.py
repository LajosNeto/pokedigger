"""
Pokemon category crawler
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


import re
import pandas as pd
import logging
import requests
import bs4 as bs
from .base import BaseCrawler
import cssutils
cssutils.log.setLevel(logging.CRITICAL)


URL = 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_category'
DATA_COLUMNS = ['name']
OUTPUT_FILE = 'pokemon_category.json'


class CategoryCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(DATA_COLUMNS, OUTPUT_FILE)
    
    def run(self):
        page = requests.get(URL)
        soup = bs.BeautifulSoup(page.content, 'html.parser')
        category_table = self.__find_category_table(soup)
        self.__find_categories(category_table)
        self.save()

    def __find_category_table(self, soup): 
        category_title = soup.find('h2',text='List of categories') 
        for tag in category_title.next_siblings: 
            if tag.name == 'table': return tag
    
    def __find_categories(self, table):
        categories_list = []
        category_trs = table.find_all('tr')[2:]
        for tr in category_trs:
            categories_list.append(re.findall('\n+(.*?)\n', tr.text, flags=re.IGNORECASE)[2].strip())
        self.update_data(set(categories_list))