from cli.parser import parse_input


def main():
    cmd = input('~~~~~ EFT Wiki Scraper ~~~~~\n> ')
    while cmd != 'q':
        parse_input(cmd.split())
        cmd = input('> ')


if __name__ == '__main__':
    main()
