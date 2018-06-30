"""This script gets information of products from avito.ru.
And writes to text file in such manner: name, price and url.

Usage:
    $ python avito_getter.py

Note:
    This script specifically was written to work with games' category to monitor prices and etc.
    However, it was not tested if other categories would work, but I believe one can easily modify.
    Just make sure there is "?p=" at the end of the url.
    If not - add it yourself, the script relies on it to work properly.

    Avito may block your IP if you there are too many pages at given category,
    You can restrict it setting pages to a desireable integer.

"""
import requests
from bs4 import BeautifulSoup
# NOTE: Beware that many sites may block your IP for botting.
class Goods():
    """Class stores the name, price and url, which can be later writtien to file.

    Args:
        name (str): String name which briefly describe the good (as is from url).
        price (str): String price the seller set.
        url (str): String URL to the product the seller is selling.

    Attributes:
        name (str): String name which briefly describe the good (as is from url).
        price (int): Integer price the seller set.
        url (str): String URL to the product the seller is selling.

    """

    def __init__(self, name, price, url):
        self.name = name.strip()
        self.price = int(price.strip().replace(" ", "")[:-1])
        self.url = url.strip()


    def get_good(self):
        """Returns attributes of the class as a single string.

        Returns:
            String of class Goods attributes.

        """
        return self.name + " " + str(self.price) + " " + self.url + "\n"


def get_content(url):
    """Returns page's content using URL.

    Args:
        url (str): Human readable url.

    Returns:
        HTTPResponse object based on URL.

    """
    try:
        page = requests.get(url).text
    except requests.exceptions.ConnectionError as exception:
        print(str(exception))
    return page


def get_soup(page):
    """Beatiful Soup wrapper of HTTPResponse.data .

    Args:
        response (HTTPResponse): an HTTPResponse instance.

    Returns:
        BeatifulSoup instance of response.data with html.parser.

    """
    return BeautifulSoup(page, "lxml")


def retrieve_page_number(base):
    """Gets a number of pages they are available to browse.

    Args:
        base (str): URL of the first page.

    Returns:
        pages (int): Number of pages available to browse.

    """
    response = get_content(base)
    soup = get_soup(response)
    # NOTE: It is a good idea to put this in try block,
    # because the web-site may block your IP and BeautifulSoup would return an empty list.
    try:
        pages = soup.find_all("a", attrs={"class": "pagination-page"})[-1]['href']
        pages = int(pages[67:])
    except IndexError:
        with open("error.txt", 'w', encoding="UTF-16") as error_file:
            error_file.write(soup.text)
    return pages


def retrieve_info(soup):
    """Retreives information from a page: name, price, url. Appends it to a list. Returns list.

    Args:
        soup (BeautifulSoup obj): BeautifulSoup object.
    Returns:
        catalog (list): List of Goods' objects.

    """
    catalog = []
    try:
        for product in soup.select("div.item_table-header"):
            name = product.find('a').text
            price = product.find('span').text
            url = "https://www.avito.ru/" + product.a['href']
            item = Goods(name, price, url)
            catalog.append(item)
    except Exception:
        print("well that sucks")
    return catalog


def iterate_catalog(url):
    """Iterates catalog list of Goods' objects, writes such information to a text file.

    Args:
        url (str): URL to request page content.

    """
    response = get_content(url)
    soup = get_soup(response)
    with open("goods.txt", 'a', encoding="utf-8") as goods_file:
        catalog = retrieve_info(soup)
        for item in catalog:
            goods_file.write(item.get_good())


def main(base):
    """Main-module function, iterates all web-pages they are at avito.ru.

    Args:
        base (str): URL that can be used to request next pages.

    """
    pages = retrieve_page_number(base)
    for page in range(pages):
        url = base + str(page + 1)
        iterate_catalog(url)


if __name__ == "__main__":
    BASE_URL = "avito.ru/amurskaya_oblast/igry_pristavki_i_programmy/igry_dlya_pristavok?p="
    main(BASE_URL)
