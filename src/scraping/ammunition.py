import bs4
import yaml

from . import AMMO_CLASSES, EFT_WIKI_AMMO_BASE_URL
from dataclasses import dataclass
from scraping.scraper import make_soup


def process_all_ammunition_tables(types, export=False):
    """ Handles scraping and exporting operations for all ammunition tables """
    pass


def scrape_all_ammunition_tables():
    """
    Separates ammunition tables by class and calls scraping operations

    :return: a collection of ammunition classes, types, and their cartridges
    """
    soup = make_soup(EFT_WIKI_AMMO_BASE_URL)

    ammunition_class_tables = soup.find_all('table', class_='wikitable')

    pistol_cart_table = ammunition_class_tables[0]
    pdw_cart_table = ammunition_class_tables[1]
    rifle_cart_table = ammunition_class_tables[2]
    shotgun_cart_table = ammunition_class_tables[3]
    grenade_cart_table = ammunition_class_tables[4]

    return {
        'pistol': scrape_ammunition_class_table('pistol', pistol_cart_table),
        'pdw': scrape_ammunition_class_table('pdw', pdw_cart_table),
        'rifle': scrape_ammunition_class_table('rifle', rifle_cart_table),
        'shotgun': scrape_ammunition_class_table('shotgun', shotgun_cart_table),
        'grenade': scrape_ammunition_class_table('grenade', grenade_cart_table)
    }


def scrape_ammunition_class_table(class_, table):
    """
    Scrapes cartridge data from the provided ammunition class table

    :param class_: the cartridge class
    :param table: the ammunition table
    :return: a collection of ammunition types and their cartridges
    """
    rows = table.find_all('tr')

    ammo_types = []

    for row in rows[1:]:  # skip table headers
        data = row.find_all('td')

        ammo_type = {
            'class': class_,
            'img': {},
            'meta': {},
            'name': data[1].text.strip(),
            'used_by': {}
        }

        # Process 'img' data
        img = data[0].find('img')
        ammo_type['img']['alt'] = data[0].find('img')['alt']
        if '.png' in img['alt']:
            ammo_type['img']['src'] = img['src'].split('.png')[0] + '.png'
        else:
            ammo_type['img']['src'] = img['src'].split('.gif')[0] + '.gif'

        # Replace breakpoints with '\n' for simpler data extract
        uses = [br.replace_with('\n') for br in data[2].find_all('br')]
        uses = list(filter(None, data[2].text.split('\n')))
        for use in uses:
            if class_ == 'shotgun' or class_ == 'grenade':  # Parse uses for 'shotgun' and 'grenade' cartridge types
                use_class = class_
                use_weapons = use.split()
            else:  # Parse uses for 'pistol', 'pdw', and 'rifle' cartridge types
                use = use.split(':')
                use_class = use[0].lower()
                use_weapons = [wep.strip() for wep in use[1].split(', ')]
            ammo_type['used_by'][use_class] = use_weapons

        # Set name metadata
        ammo_type['meta']['name_ref'] = {
            'href': data[1].a['href'],
            'text': data[1].a['title']
        }

        # Set 'used by' metadata
        ammo_type['meta']['used_by_refs'] = [{
            'href': a['href'],
            'text': a['title']
        } for a in data[2].find_all('a')]

        ammo_types.append(ammo_type)

    print(ammo_types)
    return ammo_types


def scrape_ammunition_type_table(type_, table):
    """
    Scrapes cartridge data from the provided ammunition type table

    :param table: the ammunition table
    :param type_: the ammunition type
    :return: a collection of cartridges
    """
    pass


def export_ammunition_tables(class_, cartridges):
    """
    Exports a class of ammunition to a .yml file

    :param class_: the ammunition class
    :param cartridges: the collection of cartridges
    :return: None
    """
    pass


@dataclass
class AmmoType:
    """ Class to represent an ammunition type in 'Escape from Tarkov' """

    carts: list
    class_: str
    icon: dict
    type_: str
    used_by: list

    def __init__(self, carts: list, class_: str, icon: dict, type_: str, used_by: list):
        self.carts = carts
        self.class_ = class_
        self.icon = icon
        self.type_ = type_
        self.used_by = used_by


@dataclass
class Cartridge:
    """ Class to represent a cartridge in 'Escape from Tarkov' """

    ballistics: dict
    class_: str
    effects: dict
    icon: str
    name: str
    sold_by: list
    type_: str

    def __init__(self, ballistics: dict, class_: str, effects: dict, icon: str, name: str, sold_by: list, type_: str):
        self.ballistics = ballistics
        self.class_ = class_
        self.effects = effects
        self.icon = icon
        self.name = name
        self.sold_by = sold_by
        self.type_ = type_
