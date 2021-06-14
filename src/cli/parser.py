from . import parser
from scraping.quests import process_all_quest_tables
from scraping.weapons import process_all_weapons_tables


def parse_input(args: list):
    commands = parser.parse_args(args)
    if commands.quests:
        process_all_quest_tables(traders=commands.quests, export=commands.export)
    if commands.weapons:
        process_all_weapons_tables(classes=commands.weapons, export=commands.export)
