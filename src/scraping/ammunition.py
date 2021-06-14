import bs4
import yaml

from dataclasses import dataclass


def process_all_ammunition_tables(types, export=False):
    """ Handles scraping and exporting operations for all ammunition tables """
    pass


def scrape_all_ammunition_tables():
    """
    Separates ammunition tables by class and calls scraping operations

    :return: a collection of ammunition classes, types, and their cartridges
    """
    pass


def scrape_ammunition_tables(class_, tables):
    """
    Scrapes cartridge data from the provided ammunition tables

    :param class_: the cartridge class
    :param tables: the ammunition tables
    :return: a collection of ammunition types and their cartridges
    """
    pass


def scrape_ammunition_table(type_):
    """
    Scrapes cartridge data from the associated ammunition type's table

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
