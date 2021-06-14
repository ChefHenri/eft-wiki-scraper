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

    scrape_ammunition_class_table('pistol', pistol_cart_table)


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

        # TODO: trim 'img' source after '.gif' file ending
        ammo_type = {
            'class': class_,
            'img': {
                'alt': data[0].find('img')['alt'],
                'src': data[0].find('img')['src']
            },
            'meta': {},
            'name': data[1].text.strip(),
            'used_by': data[2].text.split('\n')
        }

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
