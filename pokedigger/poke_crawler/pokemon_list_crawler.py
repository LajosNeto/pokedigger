"""
Pokemon list crawler
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


import re
import pandas as pd
import logging
import requests
import bs4 as bs
from .base import BaseCrawler
from .utils.string_utils import vulgar_fraction_translator
import cssutils
cssutils.log.setLevel(logging.CRITICAL)


URL = 'https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_category'
DATA_COLUMNS = ['pokemon', 'url']
OUTPUT_FILE = 'pokemons_url.json'
BASE_POKEMON_URL = 'https://bulbapedia.bulbagarden.net'


class PokemonListCrawler(BaseCrawler):

    def __init__(self, save_output=True):
        super().__init__(DATA_COLUMNS, OUTPUT_FILE)
        self.save_output = save_output
    
    def run(self):
        page = requests.get(URL)
        main_soup = bs.BeautifulSoup(page.content, 'html.parser')
        self.__get_pokemons_url(main_soup)
        if self.save_output: 
            self.save()
        else:
            return self.data
    
    def __get_pokemons_url(self, soup):
        """Retrieves pokemon urls

        Gets the first <table> from retrieved soup.
        The first <table> is the element where all pokemons <td> tags
        containing the pokemon name and url are located at it's inner <span> tags.

        Parameters
        ----------
        soup : bs4.BeautifulSoup
            Page soup object
        """
        pokemons_table = soup.find('table')
        trs = pokemons_table.find_all('tr')
        for i in range(2,len(trs)):
            main_span = trs[i].find_all('td')[1].find('a')
            self.update_data([[main_span['title'], BASE_POKEMON_URL+main_span['href']]]) 
