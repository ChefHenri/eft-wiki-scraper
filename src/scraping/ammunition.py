from dataclasses import dataclass

from scraping.scraper import make_soup
from . import AMMO_CLASSES, EFT_WIKI_BASE_URL, EFT_WIKI_AMMO_BASE_URL


def process_all_ammunition_tables(types, export=False):
    """ Handles scraping and exporting operations for all ammunition tables """
    data = scrape_all_ammunition_tables()


def scrape_all_ammunition_tables():
    """
    Separates ammunition tables by class and calls scraping operations

    :return: a collection of ammunition classes, types, and their cartridges
    """
    soup = make_soup(EFT_WIKI_AMMO_BASE_URL)

    ammunition_class_tables = soup.find_all('table', class_='wikitable')

    ammo_class_data = {}
    ammo_type_data = {}

    for class_, table in zip(AMMO_CLASSES, ammunition_class_tables):
        ammo_data = scrape_ammunition_class_table(class_.lower(), table)
        ammo_class_data[class_.lower()] = ammo_data['data']

        for (type_, ref) in ammo_data['refs']:
            soup = make_soup(EFT_WIKI_BASE_URL + ref)
            scrape_ammunition_type_table(type_, soup.find('table', class_='wikitable'))

    return {
        'ammo_classes': ammo_class_data,
        'ammo_types': ammo_type_data
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
    ammo_type_refs = []

    for row in rows[1:]:  # skip table headers
        data = row.find_all('td')

        ammo_type = {
            'class_': class_,
            'img': {},
            'meta': {},
            'type_': data[1].text.strip(),
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
        [br.replace_with('\n') for br in data[2].find_all('br')]

        # Filter out empty indexes
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

        ammo_types.append(AmmoType(**ammo_type))

        # Add current cartridge type to 'ammo_type_refs' for ammo type table scraping
        ammo_type_refs.append((
            ammo_type['meta']['name_ref']['text'],
            ammo_type['meta']['name_ref']['href']
        ))

    return {
        'data': ammo_types,
        'refs': ammo_type_refs
    }


def scrape_ammunition_type_table(type_, table):
    """
    Scrapes cartridge data from the provided ammunition type table

    :param class_: the ammunition class
    :param table: the ammunition table
    :param type_: the ammunition type
    :return: a collection of cartridges
    """
    rows = table.find_all('tr')

    cartridges = []

    if type_ == '7.62x25mm Tokarev':
        ric_idx = 9
        vel_idx = 6
    else:
        ric_idx = 6
        vel_idx = 9

    for row in rows[1:]:  # skip table headers
        headers = row.find_all('th')
        data = row.find_all('td')

        img = headers[0].a.img

        # FIXME: Shift indexes for '12.7x108mm' cart type
        # TODO: Yield indexes (?)

        cartridge = {
            'ballistics': {
                'acc': data[3].text.strip(),
                'arm_dmg': int(data[2].text.strip()),
                'dmg': int(data[0].text.strip()),
                'frg': data[5].text.strip(),
                'pen': int(data[1].text.strip()),
                'rec': data[4].text.strip(),
                'ric': data[ric_idx].text.strip(),
                'vel': int(data[vel_idx].text.strip()),
            },
            'effects': {
                'heavy': data[8].text.strip(),
                'light': data[7].text.strip(),
                'spc': data[10].text.strip()
            },
            'icon': {
                'alt': img['alt'],
                'src': img['src']
            },
            'name': {
                'href': headers[1].a['href'],
                'text': headers[1].a['title']
            },
            'sld_by': [],
            'type_': type_
        }

        print(cartridge)

        cartridges.append(Cartridge(**cartridge))

    return cartridges


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

    class_: str
    img: dict
    meta: dict
    type_: str
    used_by: list

    def __init__(self, class_: str, img: dict, meta: dict, type_: str, used_by: list):
        self.class_ = class_
        self.img = img
        self.meta = meta
        self.type_ = type_
        self.used_by = used_by


@dataclass
class Cartridge:
    """ Class to represent a cartridge in 'Escape from Tarkov' """

    ballistics: dict
    effects: dict
    icon: dict
    name: dict
    sld_by: list
    type_: str

    def __init__(self, ballistics: dict, effects: dict, icon: dict, name: dict, sld_by: list, type_: str):
        self.ballistics = ballistics
        self.effects = effects
        self.icon = icon
        self.name = name
        self.sld_by = sld_by
        self.type_ = type_
