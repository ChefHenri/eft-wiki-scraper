from dotenv import load_dotenv

# 'Escape from Tarkov' traders
TRADERS = ['Prapor', 'Therapist', 'Skier', 'Peacekeeper', 'Mechanic', 'Ragman', 'Jaeger', 'Fence']

# Base scraping urls
EFT_WIKI_QUESTS_BASE_URL = 'https://escapefromtarkov.fandom.com/wiki/Quests'
EFT_WIKI_WEAPONS_BASE_URL = 'https://escapefromtarkov.fandom.com/wiki/Weapons'

# Out directories
QUEST_OUT_DIR_ENV_KEY = 'QUEST_OUT_DIR'
WEAPONS_OUT_DIR_ENV_KEY = 'WEAPONS_OUT_DIR'

# Load environment variables
load_dotenv()
