from scraping.quests import scrape_all_quest_tables
from scraping.weapons import scrape_all_weapon_tables


def main():
    # process_all_quest_tables()
    all_quests = scrape_all_quest_tables()
    all_weapons = scrape_all_weapon_tables()
    print(all_weapons['primary'])
    print(all_quests)


if __name__ == '__main__':
    main()
