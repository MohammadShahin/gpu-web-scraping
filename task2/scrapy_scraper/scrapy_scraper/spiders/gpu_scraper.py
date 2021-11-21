
import scrapy
import time

stores = [
    {
        'store_name': 'OnlineTrade',
        'base_link': 'https://www.onlinetrade.ru',
        'gpu_page_link': 'https://www.onlinetrade.ru/catalogue/videokarty-c338/?page=',
        'gpu_model_element': '//li[@class="featureList__item"]/*[contains(text(), "Графический процессор")]/../text()',
        'gpu_price_element': '//span[@class="js__actualPrice"]/span/text()',
        'gpu_in_stock_element': '//span[@class="catalog__displayedItem__availabilityCount"]/label/text()',
        'gpu_link_element': '//div[@class="indexGoods__item__flexCover"]/div[@class="indexGoods__item__descriptionCover"]/a/@href',
        'gpu_name_element': '//div[@class="indexGoods__item__flexCover"]/div[@class="indexGoods__item__descriptionCover"]/a/text()',
        'page_iterator_element': '//div[@class="paginator"]/div[@class="paginator__links"]/a/text()',
        'page_start_from_zero': True
    },
    {
        'store_name': 'Regard',
        'base_link': 'https://regard.ru',
        'gpu_page_link': 'https://www.regard.ru/catalog/group4000.htm/page',
        'gpu_model_element': '//tr/td[contains(text(), "Серия")]/../td[last()]/text()',
        'gpu_price_element': '//div[@class="price_block"]/span/span/text()',
        'gpu_in_stock_element': '//div[@class="goodCard_inStock_button inStock_available"]/text()',
        'gpu_link_element': '//div[@class="bcontent"]/div[@class="aheader"]/a/@href',
        'gpu_name_element': '//div[@class="bcontent"]/div[@class="aheader"]/a/text()',
        'page_iterator_element': '//div[@class="pagination"]/a/text()',
        'page_start_from_zero': False
    }
]

MAX_PAGES = 20
unblocking_space = '\xa0'


class GpuScraper(scrapy.Spider):
    name = "gpu_scraper"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3'

    def start_requests(self):
        """
        A method to start the scraping. It goes through the stores and start scraping the first page of each store.
        :return:
        """
        for store in stores:
            store_page_link = store['gpu_page_link']
            page_num = 0 if store['page_start_from_zero'] else 1
            page_link = store_page_link + str(page_num)
            yield scrapy.Request(url=page_link, callback=self.parse, meta={**store, 'page_num': page_num})

    def parse(self, response):
        """
        A method to handle a gpu page list given the response. It consists mainly of two parts. The first part is it
        goes through each gpu in the list and scrapes them individually. The second is that it checks if the current
        page is the last page (by checking the page iterators at the bottom). If it's not the last page, it starts
        scraping the next page.
        """
        gpu_links = response.selector.xpath(response.meta['gpu_link_element']).getall()
        gpu_names = response.selector.xpath(response.meta['gpu_name_element']).getall()
        assert len(gpu_links) == len(gpu_names)
        for gpu_link, gpu_name in zip(gpu_links, gpu_names):
            gpu_link = response.meta['base_link'] + gpu_link
            gpu_name_fixed = self.fix_gpu_name(gpu_name)
            yield scrapy.Request(url=gpu_link, callback=self.parse_gpu, meta={**response.meta, 'gpu_link': gpu_link,
                                                                              'gpu_name': gpu_name_fixed})

        page_num = response.meta['page_num']
        page_iterators = response.selector.xpath(response.meta['page_iterator_element']).getall()
        if not self.is_last_page(page_iterators, page_num):
            store_page_link = response.meta['gpu_page_link']
            page_link = store_page_link + str(page_num + 1)
            yield scrapy.Request(url=page_link, callback=self.parse,
                                 meta={**response.meta, 'page_num': page_num + 1})

    def is_last_page(self, page_iterators, page_num) -> bool:
        """
        a method to find if a gpu list page (given page iterators) is the last page. It does this by finding the last
        page iterator in the page and compares its value with the page number.
        :param page_iterators: the page iterators elements at the bottom of the page.
        :param page_num: the page number of the given page.
        :return: a boolean indicating whether the given page is the last page.
        """
        for page_iterator in page_iterators[::-1]:
            if page_iterator.isdigit():
                last_page_iterator = int(page_iterator)
                break
        else:
            return False
        return last_page_iterator <= page_num

    def fix_gpu_name(self, gpu_name: str) -> str:
        """
        A method to fix the gpu name. It replaces the unblocking space with a normal space and takes rid of the parts
        that are inside parenthesis.
        :param gpu_name: the original gpu name.
        :return: a modified version of the gpu name.
        """
        gpu_name = gpu_name.replace(unblocking_space, ' ')
        gpu_name = gpu_name.split(' (')[0]
        gpu_name = gpu_name.split(' [')[0]
        return gpu_name

    def parse_gpu(self, response):
        """
        A method to deliver an object to write to the output file. It combines all required information about the gpu
        in one dictionary to write it.
        """
        ts = round(time.time())
        gpu_model = response.selector.xpath(response.meta['gpu_model_element']).get()
        yield {
            'store_name': response.meta['store_name'],
            'gpu_model': None if gpu_model is None else gpu_model.replace(unblocking_space, ' '),
            'gpu_name': response.meta['gpu_name'],
            'fetch_ts': ts,
            'gpu_price': self.fix_price(response.selector.xpath(response.meta['gpu_price_element']).get()),
            'in_stock': self.is_in_stock(response.selector.xpath(response.meta['gpu_in_stock_element']).get()),
            'url': response.meta['gpu_link']
        }

    def fix_price(self, price: str) -> str:
        """
        A method to fix the price by eliminating the spaces and the currency.
        :param price: a price string which needs to be fixed.
        :return: a modified version of the price.
        """
        try:
            price = price.replace(unblocking_space, ' ')
            price = price.replace(' ', '')
            while not price[-1].isdigit():
                price = price[:-1]
            assert int(price)
            return price
        except Exception as e:
            print("Error while finding the GPU's price:", e)
            return ''

    def is_in_stock(self, in_stock: str) -> bool:
        """
        A method to find if the gpu is available in stock given the availability string.
        :param in_stock: the availability string.
        :return: a boolean for the gpu's availability in stock.
        """
        try:
            in_stock = in_stock.replace(unblocking_space, ' ')
            if in_stock != '= 0 шт.':
                return True
            return False
        except Exception as e:
            print("Error while finding if the GPU's is in-stock (assuming it is not):", e)
            return False

