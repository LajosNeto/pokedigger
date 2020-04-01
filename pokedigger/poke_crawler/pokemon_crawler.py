"""
Pokemon crawler
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


# TEST : https://bulbapedia.bulbagarden.net/wiki/Corviknight_(Pok%C3%A9mon)

URL = 'https://bulbapedia.bulbagarden.net/wiki/Mewtwo_(Pok%C3%A9mon)'
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
        self.__get_type_effect_soup(main_soup)
        self.__get_base_stats()
        self.__get_base_type_effect()
        print(self.variants)
        for variant in self.variants:
            print(self.__get_variant_type_effect(variant))
        # print(self.base_damage_normal, self.base_damage_weak, self.base_damage_immune, self.base_damage_resistant)

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
    
    def __get_base_type_effect(self):
        """Retrieves pokemon base variant type effect data.

        Gets the first <table> from the type variant soup.
        Within the next step, all inner tables are retrieved :
        <table> 1 -> damage normal types
        <table> 21 -> damage weak types
        <table> 41 -> damage immune types
        <table> 61 -> damage resistant types
        The <span> tag is only used it it's style is "display:inline-block;", otherwise, it means that the current type
        is not used/displayed.

        Parameters
        ----------
        variant : str
            Pokemon variant name whose type effect data is currently being fetched
        """
        base_type_effect_table = self.type_effect_soup.find('table').find_all('table')
        for effect_span in base_type_effect_table[1].find_all('span',{'style': "display:inline-block;"}):
            a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
            if(len(a) == 2):
                self.base_damage_normal.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
        for effect_span in base_type_effect_table[21].find_all('span',{'style': "display:inline-block;"}):
            a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
            if(len(a) == 2):
                self.base_damage_weak.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
        for effect_span in base_type_effect_table[41].find_all('span',{'style': "display:inline-block;"}):
            a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
            if(len(a) == 2):
                self.base_damage_immune.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
        for effect_span in base_type_effect_table[61].find_all('span',{'style': "display:inline-block;"}):
            a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
            if(len(a) == 2):
                self.base_damage_resistant.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
    
    def __get_variant_type_effect(self, variant):
        """Retrieves pokemon variant type effect data.

        The first step is done to retrieve all <h4> and <h5> tags from the type effect soup.
        All type effect <table> are preceded by a <h4> or <h5> tag with the pokemon variant string.
        We take the next table below the found header tag, this is the type effect section/table for the provided variant.
        
        The type effect table for specified variant is composed by several inner <table> tags containing several <span> tags where 
        the type effect multiplier data is stored.
        <table> 3 -> damage normal types
        <table> 5 -> damage weak types
        <table> 7 -> damage immune types
        <table> 9 -> damage resistant types
        The <span> tag from each inner <table> is only used it it's style is "display:inline-block;", otherwise, it means that the 
        current type is not used/displayed.

        If no <h4> or <h5> tag with the variant string is found, the base variant data is returned.

        Parameters
        ----------
        variant : str
            Pokemon variant name whose type effect data is currently being fetched
        """
        header_tags = self.type_effect_soup.find_all(['h4', 'h5'])
        variant_header_tag = None
        for tag in header_tags:
            if tag.text == variant:
                variant_header_tag = tag
        if(variant_header_tag):
            damage_normal_data = []
            damage_weak_data = []
            damage_immune_data = []
            damage_resistant_data = []
            variant_type_effect_table = variant_header_tag.next_sibling.next_sibling
            inner_tables = [child for child in variant_type_effect_table.children]
            for effect_span in inner_tables[3].find_all('span',{'style': "display:inline-block;"}):
                a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
                if(len(a) == 2):
                    damage_normal_data.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
            for effect_span in inner_tables[5].find_all('span',{'style': "display:inline-block;"}):
                a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
                if(len(a) == 2):
                    damage_weak_data.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
            for effect_span in inner_tables[7].find_all('span',{'style': "display:inline-block;"}):
                a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
                if(len(a) == 2):
                    damage_immune_data.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
            for effect_span in inner_tables[9].find_all('span',{'style': "display:inline-block;"}):
                a = re.findall('\n+(.*?)\n', effect_span.text.replace('×',''), flags=re.IGNORECASE)
                if(len(a) == 2):
                    damage_resistant_data.append(a[0].strip()+'_'+vulgar_fraction_translator(a[1].strip()))
            return (damage_normal_data, damage_weak_data, damage_immune_data, damage_resistant_data)
        return (self.base_damage_normal, self.base_damage_weak, self.base_damage_immune, self.base_damage_resistant)
            

