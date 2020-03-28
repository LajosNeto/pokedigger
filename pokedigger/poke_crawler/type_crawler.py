"""
Pokemon type crawler
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


import pandas as pd
import logging
import requests
import bs4 as bs
from .base import BaseCrawler
import cssutils
cssutils.log.setLevel(logging.CRITICAL)


URL = 'https://bulbapedia.bulbagarden.net/wiki/Type'
DATA_COLUMNS = ['type', 'color_code']
OUTPUT_FILE = 'pokemon_types.json'


class TypeCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(DATA_COLUMNS, OUTPUT_FILE)
    
    def run(self):
        page = requests.get(URL) 
        soup = bs.BeautifulSoup(page.content, 'html.parser')
        types_table = self.__find_type_table(soup.find_all("table"))
        if(types_table): self.__find_types(types_table)
        self.save()
    
    def __find_type_table(self, tables):
        for table in tables:
            has_span = table.find('a')
            return table if(has_span and has_span.text == 'Types') else None
    
    def __find_types(self, table):
        for td in table.find_all('td'):
            span = td.find('a')
            if span:
                type_text = span.text
                type_color = cssutils.parseStyle(td['style'])['background']
                self.update_data([[type_text, type_color]])