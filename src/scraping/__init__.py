from dotenv import load_dotenv

# 'Escape from Tarkov' traders
TRADERS = ['Prapor', 'Therapist', 'Skier', 'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger', 'Fence']
AMMO_CLASSES = ['Pistol', 'PDW', 'Rifle', 'Shotgun', 'Grenade']

# Base scraping urls
EFT_WIKI_AMMO_BASE_URL = 'https://escapefromtarkov.fandom.com/wiki/Ammunition'
EFT_WIKI_QUESTS_BASE_URL = 'https://escapefromtarkov.fandom.com/wiki/Quests'
EFT_WIKI_WEAPONS_BASE_URL = 'https://escapefromtarkov.fandom.com/wiki/Weapons'

# Out directories
AMMO_OUT_DIR_ENV_KEY = 'AMMO_OUT_DIR'
QUEST_OUT_DIR_ENV_KEY = 'QUEST_OUT_DIR'
WEAPONS_OUT_DIR_ENV_KEY = 'WEAPONS_OUT_DIR'

# Load environment variables
load_dotenv()
