from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor
from twisted.internet.task import deferLater

from multiprocessing import Process, Queue

import csv, json

from .web_scraper.web_scraper.spiders.urlchecker_spider import URLCheckerSpider

filenameOutput = "AmazonPriceTracker/AmazonPriceTracker/crawler/urlcheckeroutput.json"
filenameInput = "AmazonPriceTracker/AmazonPriceTracker/crawler/urlcheckerinput.csv"

def f(q):
        try:
            runner = CrawlerRunner(settings={
                "FEEDS": {
                filenameOutput : {"format": "json"},
                },
            })
            deferred = runner.crawl(URLCheckerSpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

def URLChecker(url):
    '''
    Scrapes the provided url and checks if price can be extracted

    Input
    url (string): the url we want to check

    Output
    valid (boolean): Is the URL valid?
    price (float): Price of product (-1.0 if invalid)
    name (string): Name of product (-1.0 if invalid)
    '''

    with open(filenameInput, "w") as file:
        writer = csv.writer(file)
        url = [url]
        writer.writerow(url)


    file = open(filenameOutput, 'w')
    file.close()

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

    try:
        file = open('AmazonPriceTracker/AmazonPriceTracker/crawler/urlcheckeroutput.json')
        output = json.load(file)
        return output[0]["valid"], float(output[0]["price"]), output[0]["name"]
    except:
        return False, -1.0, -1.0
