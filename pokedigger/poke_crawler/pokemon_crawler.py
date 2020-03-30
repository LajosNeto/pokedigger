"""
Pokemon crawler
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


URL = 'https://bulbapedia.bulbagarden.net/wiki/Meowth_(Pok%C3%A9mon)'
DATA_COLUMNS = ['number',
                'name',
                'japanese_name',
                'variant',
                'generation',
                'type',
                'category',
                'catch_rate',
                'hatch_time',
                'height',
                'weight',
                'leveling_rate',
                'base_hp',
                'base_attack',
                'base_defense',
                'base_sp_attack',
                'base_sp_defense',
                'base_speed',
                'base_total']

OUTPUT_FILE = 'pokemons.json'


class PokemonCrawler(BaseCrawler):

    def __init__(self):
        super().__init__(DATA_COLUMNS, OUTPUT_FILE)
        self.variants = []
        self.stats_soup = None
        self.type_effect_soup = None
        self.base_variant_hp = None
        self.base_variant_attack = None
        self.base_variant_defense = None
        self.base_variant_sp_attack = None
        self.base_variant_sp_deffense = None
        self.base_variant_speed = None
        self.base_variant_total = None
        self.base_damage_normal = []
        self.base_damage_weak = []
        self.base_damage_immune = []
        self.base_damage_resistant = []
    
    def run(self):
        page = requests.get(URL)
        main_soup = bs.BeautifulSoup(page.content, 'html.parser')
        self.__check_variants(main_soup)
        self.__get_stats_soup(main_soup)
        self.__get_base_stats()
        print(self.variants)
        for variant in self.variants:
            print(self.__get_variant_stats(variant))

    def __check_variants(self, soup):
        # TO DO -> GET VARIANT IMAGES
        tables = soup.find_all('table')
        pkmn_variants_table = tables[7]
        trs = [tr for tr in pkmn_variants_table.find_all('tr')]
        # append the first variant (always the main one)
        self.variants.append(trs[0].find('a')['title'])
        # if next <td> is not styled as empty, means that there are variants
        if not self.__check_empty_tag(trs[1]):
            for td in trs[1].find_all('td'):
                if not self.__check_empty_tag(td): 
                    self.variants.append(td.find('a')['title'])

    def __check_empty_tag(self, tag):
        return tag.get('style') == 'display:none;'
    
    def __get_stats_soup(self, soup):
        html = u""
        stat_tag = soup.find(id='Stats').parent
        for tag in stat_tag.next_siblings: 
            if tag.name == "h3": 
                break
            else: 
                html += str(tag) 
        self.stats_soup = bs.BeautifulSoup(html, 'html.parser')
    
    def __get_type_effect_soup(self, soup):
        html = u""
        type_effect_tag = soup.find(id="Type_effectiveness").parent
        for tag in type_effect_tag.next_siblings: 
            if tag.name == "h3": 
                break
            else: 
                html += str(tag) 
        self.type_effect_soup = bs.BeautifulSoup(html, 'html.parser')
    
    def __get_base_stats(self):
        base_stats_table = self.stats_soup.find('table')
        table_stats_trs = base_stats_table.find_all('tr')
        self.base_variant_hp = table_stats_trs[2].th.find('div',{'style': "float:right"}).text
        self.base_variant_attack = table_stats_trs[3].th.find('div',{'style': "float:right"}).text
        self.base_variant_defense = table_stats_trs[4].th.find('div',{'style': "float:right"}).text
        self.base_variant_sp_attack = table_stats_trs[5].th.find('div',{'style': "float:right"}).text
        self.base_variant_sp_deffense = table_stats_trs[6].th.find('div',{'style': "float:right"}).text
        self.base_variant_speed = table_stats_trs[7].th.find('div',{'style': "float:right"}).text
        self.base_variant_total = table_stats_trs[8].th.find('div',{'style': "float:right"}).text
    
    def __get_variant_stats(self, variant):
        header_tags = self.stats_soup.find_all('h5')
        variant_header_tag = None
        for tag in header_tags:
            if tag.text == variant:
                variant_header_tag = tag
        if(variant_header_tag):
            variant_stats_table = variant_header_tag.next_sibling.next_sibling
            table_stats_trs = variant_stats_table.find_all('tr')
            hp = table_stats_trs[2].th.find('div',{'style': "float:right"}).text
            attack = table_stats_trs[3].th.find('div',{'style': "float:right"}).text
            defense = table_stats_trs[4].th.find('div',{'style': "float:right"}).text
            sp_attack = table_stats_trs[5].th.find('div',{'style': "float:right"}).text
            sp_defense = table_stats_trs[6].th.find('div',{'style': "float:right"}).text
            speed = table_stats_trs[7].th.find('div',{'style': "float:right"}).text
            total = table_stats_trs[8].th.find('div',{'style': "float:right"}).text
            return(variant, (hp, attack, defense, sp_attack, sp_defense, speed, total))
        return (variant,(
            self.base_variant_hp, self.base_variant_attack, self.base_variant_defense, 
            self.base_variant_sp_attack, self.base_variant_sp_deffense, self.base_variant_speed, 
            self.base_variant_total))