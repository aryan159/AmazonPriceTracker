from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
import time, datetime
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings     
from twisted.internet import reactor
from twisted.internet.task import deferLater
import csv
import json
from multiprocessing import Process, Queue

from .web_scraper.web_scraper.spiders.urlchecker_spider import URLCheckerSpider
#from .models import Prices, Products

filenameOutput = 'AmazonPriceTracker/crawler/urlcheckeroutput.json'

def URLCheckerStarter():
    process = CrawlerProcess(settings={
            "FEEDS": {
            filenameOutput : {"format": "json"},
            },
        })

    process.start()
    return process

def f(q):
        try:
            #configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
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
    (list) [valid(Boolean), price(int)]
    '''

    with open("AmazonPriceTracker/crawler/urlcheckerinput.csv", "w") as file:
        writer = csv.writer(file)
        url = [url]
        writer.writerow(url)

    
    file = open(filenameOutput, 'w')
    file.close()
    """ process = CrawlerProcess(settings={
            "FEEDS": {
            filenameOutput : {"format": "json"},
            },
        }) """

    

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

    #process.crawl(URLCheckerSpider)
    #process.start()

    try:
        file = open('AmazonPriceTracker/crawler/urlcheckeroutput.json')
        output = json.load(file)
        return output[0]["valid"], float(output[0]["price"]), output[0]["name"]
    except:
        return False, -1.0, -1.0
