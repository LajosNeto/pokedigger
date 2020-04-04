![alt text](https://res.cloudinary.com/lajosneto/image/upload/v1586006294/pokedigger/background_full.png)
# Pokedigger

### What
This is my IronHack data analytics project for the Python and web scrapping module!
Pokedigger is a tool for scrapping pokemon related data from Bulbapedia : https://bulbapedia.bulbagarden.net/wiki/Main_Page

<br>

### Crawlers implemented
- Types crawler (https://bulbapedia.bulbagarden.net/wiki/Type)
- Category crawler (https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_category)
- Region / Generation crawler (https://en.wikipedia.org/wiki/Pok%C3%A9mon_universe)
- Pokemon list crawler (https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_category)
- Pokemons details crawler
  - Base pokemon
  - Pokemon variants
  - Base stats (also for variants)
  - Type effectiveness
    - Damage normal (also for variants)
    - Damage weak (also for variants)
    - Damage immune (also for variants)
    - Damage resistant (also for variants)

<br>

### Roadmap
- Add new attributes on Pokemon details crawler (number, weight, height, types, hatch time and EV)
- Implement a data saving module for storing retrieved information into a database (SQL and NoSQL)
- Implement a REST API for retrieving Pokemon data

<br>

### Known issues
Some pokemons details pages do not follow the overall pattern from the majority of the other ones.
There are some known pages with this kind of issue that the Pokemon Crawler currently does not work on :(.
From all 894 pokemons, 10 are currently not being fetched, for more details, you can check the error output
file at : pokedigger/pokedigger/poke_crawler/output/reports/error_pokemons.json

<br>
<br>
<br>

image source : https://pokemonrevolution.net/forum/index.php?threads/hoenn-excavation-sites-guide.113459/
