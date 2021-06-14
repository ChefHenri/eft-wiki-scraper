import bs4
import yaml

from . import EFT_WIKI_WEAPONS_BASE_URL, WEAPONS_OUT_DIR_ENV_KEY
from dataclasses import dataclass
from os import environ, path
from scraping.scraper import make_soup


def process_all_weapons_tables(classes, export=False):
    """ Handles scraping and exporting operations for all weapons tables """
    all_weapons = scrape_all_weapon_tables()

    for class_, weapons in all_weapons.items():
        if class_ in classes:
            if export:
                export_weapons_table(class_, weapons)
            else:
                print(weapons)
        else:
            continue


def scrape_all_weapon_tables():
    """
    Separates weapons tables and calls scraping operations

    :return: collection of weapons
    """
    soup = make_soup(EFT_WIKI_WEAPONS_BASE_URL)
    weapons_tables = soup.find_all('table', class_='wikitable')

    # Select weapons tables
    primary_weapons_tables = weapons_tables[0:8]
    secondary_weapons_table = weapons_tables[8:9]
    stationary_weapons_tables = weapons_tables[9:11]
    melee_weapons_table = weapons_tables[11:12]
    throwable_weapons_tables = weapons_tables[12:15]

    return {
        'primary': scrape_weapons_tables('primary', primary_weapons_tables),
        'secondary': scrape_weapons_tables('secondary', secondary_weapons_table),
        'stationary': scrape_weapons_tables('stationary', stationary_weapons_tables),
        'melee': scrape_weapons_tables('melee', melee_weapons_table),
        'throwable': scrape_weapons_tables('throwable', throwable_weapons_tables)
    }


def scrape_weapons_tables(class_, tables):
    """
    Scrapes weapon data from the provided weapons tables

    :param class_: the weapons class
    :param tables: the weapons tables
    :return: scraped weapon data
    """
    weapons = []

    for table in tables:
        for row in table.find_all('tr')[1:]:  # Skip table headers
            data = row.find_all('td')
            image = row.find('th')

            # TODO: trim 'img' source past '.png' file ending
            weapon = {
                'desc': data[-1].text.strip(),
                'img': {
                    'alt': image.a.img['alt'],
                    'href': image.a['href'],
                    'src': image.a.img['src'],
                    'title': image.a['title'],
                },
                'name': data[0].text.strip()
            }

            if class_ == 'primary' or class_ == 'secondary' or class_ == 'stationary':
                weapon['cartridge'] = {
                    'href': data[1].a['href'],
                    'text': data[1].a.text.strip()
                }
                weapon['modes'] = [text.strip() for text in data[2].contents if isinstance(text, bs4.NavigableString)]
                try:
                    weapon['fire_rate'] = int(data[3].text.strip())
                except ValueError:
                    weapon['fire_rate'] = None

                weapons.append(Firearm(**weapon))

            if class_ == 'melee':
                weapon['chop_dmg'] = int(data[1].text.strip())
                weapon['chop_rng'] = data[2].text.strip()
                weapon['stab_dmg'] = int(data[3].text.strip())
                weapon['stab_rng'] = data[4].text.strip()

                weapons.append(Melee(**weapon))

            if class_ == 'throwable':
                if len(data) > 3:
                    weapon['radius'] = data[2].text.strip()
                    weapon['frg_dmg'] = int(data[3].text.strip())
                    weapon['frg_count'] = int(data[4].text.strip())
                else:
                    weapon['radius'] = None
                    weapon['frg_dmg'] = None
                    weapon['frg_count'] = None

                weapon['delay'] = data[1].text.strip()

                weapons.append(Throwable(**weapon))

    return weapons


def export_weapons_table(class_, weapons):
    """
    Exports a class of weapons tables to a .yml file

    :param class_: the weapons class
    :param weapons: the weapons
    :return: None
    """
    with open(path.join(environ.get(WEAPONS_OUT_DIR_ENV_KEY), f'{class_.lower()}-weapons.yml'), 'w') as out_file:
        yaml.dump(weapons, out_file, default_flow_style=False)


@dataclass
class Weapon:
    """ Class to represent a weapon in 'Escape from Tarkov' """

    desc: str
    img: dict
    name: str

    def __init__(self, desc: str, img: dict, name: str):
        self.desc = desc
        self.img = img
        self.name = name


@dataclass
class Firearm(Weapon):
    """ Class to represent a firearm in 'Escape from Tarkov' """

    cartridge: dict
    fire_rate: int
    modes: list

    def __init__(self, cartridge: dict, desc: str, fire_rate: int, img: dict, modes: list, name: str):
        super().__init__(desc, img, name)
        self.cartridge = cartridge
        self.fire_rate = fire_rate
        self.modes = modes


@dataclass
class Melee(Weapon):
    """ Class to represent a melee weapon in 'Escape from Tarkov' """

    chop_dmg: int
    chop_rng: str
    stab_dmg: int
    stab_rng: str

    def __init__(self, chop_dmg: int, chop_rng: str, desc: str, img: dict, name: str, stab_dmg: int, stab_rng: str):
        super().__init__(desc, img, name)
        self.chop_dmg = chop_dmg
        self.chop_rng = chop_rng
        self.stab_dmg = stab_dmg
        self.stab_rng = stab_rng


@dataclass
class Throwable(Weapon):
    """ Class to represent a throwable weapon in 'Escape from Tarkov' """

    delay: str
    frg_count: int
    frg_dmg: int
    radius: str

    def __init__(self, delay: str, desc: str, frg_count: int, frg_dmg: int, img: dict, name: str, radius: str):
        super().__init__(desc, img, name)
        self.delay = delay
        self.frg_count = frg_count
        self.frg_dmg = frg_dmg
        self.radius = radius
