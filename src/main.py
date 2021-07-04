from cli.parser import parse_input
from scraping.ammunition import process_all_ammunition_tables


def main():
    cmd = input('~~~~~ EFT Wiki Scraper ~~~~~\n> ')
    while cmd != 'q':
        parse_input(cmd.split())
        cmd = input('> ')

    # process_all_ammunition_tables([])


if __name__ == '__main__':
    main()
