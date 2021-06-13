import requests

from bs4 import BeautifulSoup


def make_soup(url):
    """
    Gets the html 'soup' for the provided webpage url

    :param url: webpage url
    :return: parsed html 'soup'
    """
    page = requests.get(url=url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup
