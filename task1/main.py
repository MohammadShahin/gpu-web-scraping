
from task1.gpu_scraper import *

OUTPUT_FILE = './output.csv'

stores = [
        {
            'store_name': 'OnlineTrade',
            'base_link': 'https://www.onlinetrade.ru/',
            'gpu_page_link': 'https://www.onlinetrade.ru/catalogue/videokarty-c338/?page=',
            'gpu_features_element': 'li.featureList__item',
            'gpu_name_element': 'div.productPage__card  h1',
            'gpu_price_element': 'span.js__actualPrice',
            'in_stock_element': 'span.catalog__displayedItem__availabilityCount label',
            'gpu_link_element': 'div.indexGoods__item__flexCover > div > a[href]',
            'page_iterator_element': 'div.paginator > div.paginator__links > a',
            'gpu_model_key': 'Серия процессора',
            'feature_separator': ':',
            'page_start_from_zero': True
        },
        {
            'store_name': 'Regard',
            'base_link': 'https://regard.ru',
            'gpu_page_link': 'https://www.regard.ru/catalog/group4000.htm/page',
            'gpu_features_element': '#tabs-1 > table tr',
            'gpu_name_element': '#goods_head',
            'gpu_price_element': '#hits-long > div.content > div.block.bblock-long.lot > div.bcontent.lot > div.goods_price > div.price_block > span.price.lot > span',
            'in_stock_element': '#hits-long > div.content > div.block.bblock-long.lot > div.bcontent.lot > div.goods_price > div.action_block.left > div > div',
            'gpu_link_element': '#hits > div.content > div.block > div.bcontent > div.aheader > a',
            'page_iterator_element': '#hits > div.content > div.pagination > a',
            'gpu_model_key': 'Серия',
            'feature_separator': '  ',
            'page_start_from_zero': False
        }
]


if __name__ == '__main__':
    all_data = pd.DataFrame(columns=COLUMNS)
    pd.set_option('display.max_columns', None)
    for store in stores:
        gpu_scraper = GpuScraper(**store)
        store_data, last_scrape = gpu_scraper.scrape()
        print(store_data.head(20))
        all_data = all_data.append(store_data)
    all_data.to_csv(OUTPUT_FILE, index=False)
    print(all_data.head(20))
