# Web Scraping with Provectus Task 2: Using Scrapy

## Table of contents
- [Task description](#task2-description)
- [Solution logic](#task2-solution-logic)
- [Running the solution](#task2-run-solution)


<a name="task2-description"></a>
## Task description
All the same as part 1, but using [Scrapy](https://scrapy.org/) framework. 
Also, you will need to add one more website to parse (on your choice) 
and use XPath selectors to locate elements on the web page.

##### Required tech stack
Try to implement your solution using following python packages: `Scrapy`

Revisit/explore following topics:
- Scrapy official doc
- HTTP request/response structure
- XPath query language

##### Expected deadline: 15.11.21 (~1 week)

<a name="task2-solution-logic"></a>
## Solution logic

The `GpuScraper` class in 'scrapy_scraper/scrapy_scraper/spider/gpu_scraper.py' is the main part of the project. 
This class inherits the class `scrapy.Spider` to achieve fast processing (scraping) of the sites.

The stores which need to be scraped along with their necessary information are stored in a list of dictionaries. The info
include the name of the stores, the Xpath selectors of the necessary items, etc. 

The workflow of the scraping is described in the following steps:
  1. It goes through each page of the GPUs pages in the given site. 
  2. It starts iterating over each GPU in the list, and visit their site individually.
  3. It collects the necessary information as shown the task description, stores them in the output file.

<a name="task2-run-solution"></a>
### Run the solution
To run the solution you need first to install the necessary modules in 'requirements.txt'. To do that, run the 
following command in the terminal:
```shell
$ pip install -r ./task2/requirements.txt
```

Now you can run the scraper file using the command:
```shell
scrapy crawl gpu_scraper -o output.csv
```
