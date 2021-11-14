# Web Scraping with Provectus

All the tasks in this repository were done as part of Provectus internship. 

## Table of contents
- [Task 1](#task1)
    - [Task description](#task1-description)
    - [Solution logic](#task1-solution-logic)
    - [Running the solution](#task1-run-solution)

<a name="task1"></a>
## Task 1

<a name="task1"></a>
### Task description
Fetch the data about gpu prices/OOS status from local retailer store websites.

Store the gathered data into single CSV file in the following format:
```
store_name,gpu_model,gpu_name,fetch_ts,gpu_price,in_stock,url
OnlineTrade,RTX 3060,ASUS ROG Strix RTX 3060 OC12GB,1635846081,75999,true,https://onlinetrade.ru/url_to_gpu/
```
Details:
- `fetch_ts` - unix timestamp in seconds
- `in_stock` - availability status `true/false`

Please choose at least 3 local retailers from the list:

- https://www.onlinetrade.ru
- https://www.citilink.ru
- https://www.dns-shop.ru
- https://xcom-shop.ru
- https://pleer.ru
- https://regard.ru
- https://oldi.ru

<a name="task1"></a>
### Solution logic
The sites used for this task were https://www.onlinetrade.ru and https://regard.ru. 

The `GpuScraper` class in 'gpu_scraper.py' is the main part of the project. When it is needed
to scrape a store site, a new object of the class is created with the new site details such as the site's 
link, and the css selectors of the necessary items, etc. When a new object is successfully
created of the class, the `scrape` method can be used to start scraping the site. The workflow
of the scraping is described in the following steps:
  1. It goes through each page of the GPUs pages in the given site. 
  2. It starts iterating over each GPU in the list, and visit their site individually.
  3. It collects the necessary information as shown the task description, stores them 
  into a Pandas dataframe, and finally returns the dataframe.

In the 'main.py' you can check the sites' used for scraping. The two sites are scraped, and their outputs are 
merged into one dataframe, which is finally written to an output csv file. 

<a name="task1-run-solution"></a>
### Run the solution
To run the solution you need first to install the necessary modules in 'requirements.txt'. To do that, run the 
following command in the terminal:
```shell
$ pip install -r ./task1/requirements.txt
```

Now you can run the 'main.py' file using the command:
```shell
$ python ./task1/main.py
```
