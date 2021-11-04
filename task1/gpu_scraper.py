import time
import requests
from bs4 import BeautifulSoup
from utils import * 
import pandas as pd


base_link = 'https://www.onlinetrade.ru/'
gpu_page_link = base_link + 'catalogue/videokarty-c338/?page='
COLUMNS = ['store_name', 'gpu_model', 'gpu_name', 'fetch_ts', 'gpu_price', 'in_stock', 'url']
num_pages = 1


class GpuScraper:

    def __init__(self, gpu_page_link, store_name):
        self.gpu_page_link = gpu_page_link
        self.store_name = store_name
        pass

    def scrape(self):
        page_num = 0
        while True:
            page_content = read_link(self.gpu_page_link + str(page_num))
            page_num += 1
            page_data = self.handle_page(page_content, )
            if self.is_last_page(page_content):
                break

    def get_gpu_model(self, gpu_content: BeautifulSoup) -> str:
        """
        A method to get the gpu model given
        :param gpu_content:
        :return:
        """
        try:
            features = gpu_content.select("li.featureList__item")
            value = ''
            for feature in features:
                feature_text = feature.get_text()
                key, value = feature_text.split(':')
                if key == 'Серия процессора':
                    break
            return value
        except:
            return ''

    def get_gpu_name(self, gpu_content):
        try:
            gpu_name_element = gpu_content.select('div.productPage__card  h1')[0]
            gpu_name = self.get_fixed_text(gpu_name_element)
            gpu_name = gpu_name.split(' (')[0].split(' ', 1)[-1]
            return gpu_name
        except:
            return ''

    def get_gpu_price(self, gpu_content):
        try:
            gpu_price_element = gpu_content.select('span.js__actualPrice')[0]
            gpu_price = self.get_fixed_text(gpu_price_element, '')[:-1]
            gpu_price = int(gpu_price)
            return gpu_price
        except:
            return ''

    def get_in_stock(self, gpu_content):
        try:
            in_stock_element = gpu_content.select('span.catalog__displayedItem__availabilityCount label')[0]
            in_stock = self.get_fixed_text(in_stock_element)
            if in_stock != '= 0 шт.':
                return True
            return False
        except:
            return False

    def handle_gpu_item(self, gpu_content):
        gpu_data = {'gpu_model': self.get_gpu_model(gpu_content),
                    'gpu_name': self.get_gpu_name(gpu_content),
                    'fetch_ts': int(time.time()),
                    'gpu_price': self.get_gpu_price(gpu_content),
                    'in_stock': self.get_in_stock(gpu_content)
                    }
        return gpu_data

    def is_last_page(self, page_content):
        gpus_shown_element = page_content.select('div.paginator__count')[0]
        gpus_shown = self.get_fixed_text(gpus_shown_element).split(':')[-1]
        gpus_shown = gpus_shown.strip()
        gpus_shown_list = gpus_shown.split()
        last_gpu_in_page = gpus_shown_list[0].split('-')[-1]
        gpus_total = gpus_shown_list[-1]
        return gpus_total == last_gpu_in_page
    
    def handle_page(self, page_content):
        gpu_item_class = 'indexGoods__item'
        gpu_items = list(page_content.find_all(class_=gpu_item_class))
        data = {column: [] for column in COLUMNS}
        description_class = 'indexGoods__item__descriptionCover'
        for gpu_item in gpu_items:
            gpu_description = gpu_item.find(class_=description_class)
            gpu_link_item = gpu_description.find('a')
            if gpu_link_item.has_attr('href'):
                gpu_link = base_link + gpu_link_item['href']
                gpu_content = read_link(gpu_link)
                gpu_data = self.handle_gpu_item(gpu_content)
                data['store_name'].append(self.store_name)
                for column in COLUMNS:
                    data[column].append(gpu_data[column])
                data['url'].append(gpu_link)
            break
        print(data)
        return []
