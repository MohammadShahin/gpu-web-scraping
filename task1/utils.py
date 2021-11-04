
from bs4 import BeautifulSoup
import requests


def read_link(link: str) -> BeautifulSoup:
    """
    A method to read a web page given its link. It returns the contents of the page.
    :param link: the link of the web page.
    :return: the contents of the page as BeautifulSoup.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(link, headers=headers)
    assert page.status_code == 200
    content = BeautifulSoup(page.content, 'html.parser')
    return content


def get_fixed_text(soup: BeautifulSoup, new_space: str = ' ') -> str:
    """
    A method to get the text of a BeautifulSoup object. It replaces the non-break space unicode (i.e. '\xa0') to the new
    space passed as an  argument.
    :param soup: the element to read the text from.
    :param new_space: the string to replace the non-break space.
    :return: a string representing the text inside the given soup after the proper modifications.
    """
    text = soup.get_text()
    non_break_space = '\xa0'
    text = text.replace(non_break_space, new_space)
    return text
