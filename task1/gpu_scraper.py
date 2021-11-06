import time
from typing import Tuple, List

from bs4 import BeautifulSoup
from task1.utils import read_link, get_fixed_text


COLUMNS = ['store_name', 'gpu_model', 'gpu_name', 'fetch_ts', 'gpu_price', 'in_stock', 'url']


class GpuScraper:
    """
    A class to scrap a site given its link and the important elements' selectors.
    """

    def __init__(self, base_link: str, gpu_page_link: str, store_name: str, gpu_features_element: str,
                 gpu_name_element: str, gpu_price_element: str, in_stock_element: str, gpu_link_element: str,
                 page_iterator_element: str, page_start_from_zero: bool, gpu_model_key: str, feature_separator: str):
        """
        The main constructor of the scraper, it is used to store the information related to the site that needs to be
        scraped.
        :param base_link: the base link of the site (store).
        :param gpu_page_link: the link of the gpu list page.
        :param store_name: the name of the store.
        :param gpu_name_element: the CSS selector of the name element in the gpu page.
        :param gpu_price_element: the CSS selector of the price element in the gpu page.
        :param in_stock_element: the CSS selector of the in-stock element in the gpu page.
        :param gpu_link_element: the CSS selector of the gpu link in the gpu list page.
        :param page_iterator_element: the CSS selector of the page iterator in the gpu list page.
        :param page_start_from_zero: a boolean indicating whether the page numbers start from zero (or one).
        :param gpu_features_element: the CSS selector of the features element in the gpu page.
        :param gpu_model_key: when features of some gpu are scraped, they are like (key, value) pairs. This argument
        represents the key value of the gpu model.
        :param feature_separator: when features of some gpu are scraped, they are like (key, value) pairs separated by
        some string, for example ':'. This argument is for this separator.
        """
        self.base_link = base_link
        self.gpu_page_link = gpu_page_link
        self.store_name = store_name
        self.gpu_features_element = gpu_features_element
        self.gpu_name_element = gpu_name_element
        self.gpu_price_element = gpu_price_element
        self.in_stock_element = in_stock_element
        self.gpu_link_element = gpu_link_element
        self.page_iterator_element = page_iterator_element
        self.page_start_from_zero = page_start_from_zero
        self.gpu_model_key = gpu_model_key
        self.feature_separator = feature_separator
        self.data = None
        self.last_scrape = None

    def scrape(self) -> Tuple[List[dict], float]:
        """
        A method to run the scraping process. It goes through the gpus list pages one by one, then iterates over all the
        gpus in the each gpu page. For each gpu, it collects the necessary information and finally returns the output as
        a list of dictionaries representing the data scraped (each element represents a gpu), and the timestamp of the
        last fetch process.
        :return: the output of the scraping process as a list of dictionaries (each element represents a gpu).
        COLUMNS, and the timestamp of the last fetch process.
        """
        page_num = 0 if self.page_start_from_zero else 1
        self.data = []
        while True:
            page_content = read_link(self.gpu_page_link + str(page_num))
            self.handle_page(page_content)
            if self.is_last_page(page_content, page_num + self.page_start_from_zero):
                break
            page_num += 1
        return self.data, self.last_scrape

    def get_gpu_model(self, gpu_content: BeautifulSoup) -> str:
        """
        A method to get the gpu model given the gpu page content. It goes through the features of the gpu, and finds its
        model. If it does not find the field of the gpu model, it returns an empty string.
        :param gpu_content: the contents of the gpu page.
        :return: the gpu model. If it does not find the field of the gpu model, it returns an empty string.
        """
        try:
            features = gpu_content.select(self.gpu_features_element)
            value = ''
            for feature in features:
                try:
                    feature_text = get_fixed_text(feature)
                    key, value = feature_text.split(self.feature_separator, 1)
                    if key == self.gpu_model_key:
                        value_list = [word for word in value.split() if word.isascii()]
                        value = ' '.join(value_list)
                        break
                except:
                    continue
            return value
        except Exception as e:
            print("Error while finding the GPU's model:", e)
            return ''

    def get_gpu_name(self, gpu_content: BeautifulSoup):
        """
        A method to get the gpu name given the gpu page content. It selects the name element, and finds the name. If it
        does not find the field of the gpu name, it returns an empty string.
        :param gpu_content: the contents of the gpu page.
        :return: the gpu name. If it does not find the field of the gpu name, it returns an empty string.
        """
        try:
            gpu_name_element = gpu_content.select(self.gpu_name_element)[0]
            gpu_name = get_fixed_text(gpu_name_element)
            gpu_name = gpu_name.split(' (')[0]
            gpu_name = gpu_name.split(' [')[0]
            gpu_name_list = [word for word in gpu_name.split() if word.isascii()]
            gpu_name = ' '.join(gpu_name_list)
            return gpu_name
        except Exception as e:
            print("Error while finding the GPU's name:", e)
            return ''

    def get_gpu_price(self, gpu_content: BeautifulSoup) -> str:
        """
        A method to get the gpu price given the gpu page content. It selects the price element and finds the price. If
        it does not find the field of the gpu price, it returns an empty string.
        :param gpu_content: the contents of the gpu page.
        :return: the gpu price. If it does not find the field of the gpu price, it returns an empty string.
        """
        try:
            gpu_price_element = gpu_content.select(self.gpu_price_element)[0]
            gpu_price = get_fixed_text(gpu_price_element)
            gpu_price = gpu_price.replace(' ', '')
            while not gpu_price[-1].isdigit():
                gpu_price = gpu_price[:-1]
            assert int(gpu_price)
            return gpu_price
        except Exception as e:
            print("Error while finding the GPU's price:", e)
            return ''

    def get_in_stock(self, gpu_content: BeautifulSoup) -> bool:
        """
        A method to get if the gpu price is available in the stock given the gpu page content. It selects the in-stock
        element and finds if it is in stock. If it does not find the field of the gpu in-stock, it assumes it is not
        available in stock.
        :param gpu_content: the contents of the gpu page.
        :return: a boolean indicating whether the gpu is available in stock. If it does not find the field of the gpu
        in-stock, it assumes it is not available in stock (returns False).
        """
        try:
            in_stock_element = gpu_content.select(self.in_stock_element)[0]
            in_stock = get_fixed_text(in_stock_element)
            if in_stock != '= 0 шт.':
                return True
            return False
        except Exception as e:
            print("Error while finding if the GPU's is in-stock (assuming it is not):", e)
            return False

    def handle_gpu_item(self, gpu_content: BeautifulSoup) -> dict:
        """
        a method for finding a gpu item following information: its model, its name, its price, and if it is available in
        stock. It stores these information in a dictionary, and returns this dictionary.
        :param gpu_content: the contents of the gpu page.
        :return: a dictionary containing the gpu info: its model, its name, its price, and if it is available in stock.
        """
        gpu_data = {'gpu_model': self.get_gpu_model(gpu_content).strip(),
                    'gpu_name': self.get_gpu_name(gpu_content).strip(),
                    'gpu_price': self.get_gpu_price(gpu_content),
                    'in_stock': self.get_in_stock(gpu_content)
                    }
        return gpu_data

    def is_last_page(self, page_content: BeautifulSoup, page_num: int) -> bool:
        """
        a method to find if a gpu list page (given its content) is the last page. It does this by finding the last page
        iterator in the page and compares its value with the page number.
        :param page_content: the contents of the gpus list page.
        :param page_num: the page number of the given page.
        :return: a boolean indicating whether the given page is the last page.
        """
        page_iterator_elements = page_content.select(self.page_iterator_element)
        for page_iterator_element in page_iterator_elements[::-1]:
            element_text = get_fixed_text(page_iterator_element)
            element_text = element_text.replace(' ', '')
            if element_text.isdigit():
                last_page_iterator = int(element_text)
                break
        else:
            return False
        return last_page_iterator <= page_num

    def append_data(self, new_data: dict) -> None:
        """
        a method to append the data of a new gpu to the data stored in the object.
        :param new_data: a dictionary containing the new gpu's data.
        :return: None.
        """
        self.data.append(new_data)

    def handle_page(self, page_content: BeautifulSoup):
        """
        A method to handle a gpus list page given its content. It goes through each gpu in the list, enters its link,
        find the necessary information, and finally stores the output in the object's data.
        :param page_content: the contents of the gpus list page.
        :return: None.
        """
        gpu_links = page_content.select(self.gpu_link_element)
        for gpu_link_item in gpu_links:
            gpu_link = self.base_link + gpu_link_item['href']
            gpu_content = read_link(gpu_link)
            now = time.time()
            self.last_scrape = now
            gpu_data = self.handle_gpu_item(gpu_content)
            self.append_data({**gpu_data, 'store_name': self.store_name, 'fetch_ts': int(now), 'url': gpu_link})

    def get_data(self) -> Tuple[List[dict], float]:
        """
        A method to get the data lastly scraped in the object along with the timestamp of the last fetch process.
        :return: a list of dictionaries representing the data scraped, and the timestamp of the last fetch process.
        """
        return self.data, self.last_scrape
