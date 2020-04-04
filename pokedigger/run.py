from poke_crawler.type_crawler import TypeCrawler
from poke_crawler.category_crawler import CategoryCrawler
from poke_crawler.region_crawler import RegionCrawler
from poke_crawler.pokemon_crawler import PokemonCrawler
from poke_crawler.pokemon_list_crawler import PokemonListCrawler
from multiprocessing import Pool

if __name__ == '__main__':
    TypeCrawler().run()
    CategoryCrawler().run()
    RegionCrawler().run()
    pokemon_urls = PokemonListCrawler(save_output=False).run()
    pokemon_crawler = PokemonCrawler(pokemon_urls)
    pokemon_crawler.run()