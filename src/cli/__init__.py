from argparse import ArgumentParser
from scraping.quests import scrape_all_quest_tables, process_all_quest_tables

QUEST_TRADERS = ['all', 'prapor', 'therapist', 'fence', 'skier', 'peacekeeper', 'mechanic', 'ragman', 'jaeger']
WEAPON_CLASSES = ['all', 'primary', 'secondary', 'stationary', 'melee', 'throwable']

parser = ArgumentParser(description='handle scraping and exporting operations')
subparsers = parser.add_subparsers()

# 'Print' subparser
print_subparser = subparsers.add_parser('print', help='handles printing operations')
print_subparser.add_argument('--quests', action='append', type=str, choices=QUEST_TRADERS,
                             help='trader\'s quests to print')
print_subparser.add_argument('--weapons', action='append', type=str, choices=WEAPON_CLASSES,
                             help='weapon classes to print')
print_subparser.set_defaults(export=False)

# 'Export' subparser
export_subparser = subparsers.add_parser('export', help='handles exporting operations')
export_subparser.add_argument('--quests', action='append', type=str, choices=QUEST_TRADERS,
                              help='trader\'s quests to export')
export_subparser.add_argument('--weapons', action='append', type=str, choices=WEAPON_CLASSES,
                              help='weapons classes to export')
export_subparser.set_defaults(export=True)
