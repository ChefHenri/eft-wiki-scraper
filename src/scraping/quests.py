import yaml

from . import EFT_WIKI_QUESTS_BASE_URL, QUEST_OUT_DIR_ENV_KEY, TRADERS
from dataclasses import dataclass
from os import environ, path
from scraping.scraper import make_soup


def process_all_quest_tables(traders, export=False):
    """ Handles scraping and exporting operations for all trader quests """
    all_quests = scrape_all_quest_tables()

    for trader, quests in all_quests.items():
        if trader in traders:
            if export:
                export_quest_table(trader=trader, quests=quests)
            else:
                print(quests)
        else:
            continue


def scrape_all_quest_tables():
    """
    Calls functions to parse quest info from the respective trader's quest table

    :return: collection of trader quests
    """
    soup = make_soup(EFT_WIKI_QUESTS_BASE_URL)

    quests = {}

    for trader in TRADERS:
        quests[trader.lower()] = scrape_quest_table(trader, table=soup.find('table', class_=f'{trader}-content'))

    return quests


def scrape_quest_table(trader, table):
    """
    Scrapes quest information from the provided quest table

    :param trader: the trader
    :param table: the quest table
    :return: scraped info
    """
    quests = []

    for row in table.find_all('tr')[2:]:  # Skips table name header and table column headers
        headers = row.find_all('th')
        data = row.find_all('td')

        # Get the quest info
        quest_name = headers[0].text.strip()
        quest_type = headers[1].text.strip()
        quest_objectives = [li.text.strip() for li in data[0].ul.find_all('li')]
        quest_rewards = [li.text.strip() for li in data[1].ul.find_all('li')]

        # Get the quest hrefs
        quest_ref = {'href': headers[0].a['href'], 'text': headers[0].a.text}
        quest_obj_refs = [{'href': a['href'], 'text': a.text} for a in data[0].ul.find_all('a')]
        quest_reward_refs = [{'href': a['href'], 'text': a.text} for a in data[1].ul.find_all('a')]

        # Gather quest refs
        quest_metadata = {'ref': quest_ref, 'obj_refs': quest_obj_refs, 'reward_refs': quest_reward_refs}

        quests.append(Quest(meta=quest_metadata,
                            name=quest_name,
                            objectives=quest_objectives,
                            rewards=quest_rewards,
                            trader=trader,
                            type_=quest_type))

    return quests


def export_quest_table(trader, quests):
    """
    Exports a trader's quests to a .yml file

    :param trader: the trader for the quests
    :param quests: the trader's quests
    :return: None
    """
    with open(path.join(environ.get(QUEST_OUT_DIR_ENV_KEY), f'{trader.lower()}-quests.yml'), 'w') as out_file:
        yaml.dump(quests, out_file, default_flow_style=False)


@dataclass
class Quest:
    """ Class to represent a quest in 'Escape from Tarkov' """

    meta: dict
    name: str
    objectives: list
    rewards: list
    trader: str
    type_: str

    def __init__(self, meta: dict, name: str, objectives: list, rewards: list, trader: str, type_: str):
        self.meta = meta
        self.name = name
        self.objectives = objectives
        self.rewards = rewards
        self.trader = trader
        self.type_ = type_
