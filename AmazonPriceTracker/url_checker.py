from scrapy.crawler import CrawlerProcess, CrawlerRunner
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

from .web_scraper.web_scraper.spiders.urlchecker_spider import URLCheckerSpider
from .models import Prices, Products

filenameOutput = 'AmazonPriceTracker/crawler/urlcheckeroutput.json'

def URLCheckerStarter():
    process = CrawlerProcess(settings={
            "FEEDS": {
            filenameOutput : {"format": "json"},
            },
        })

    process.start()
    return process


def URLChecker(url, process):
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

    process.crawl(URLCheckerSpider)
    #process.start()

    try:
        file = open('AmazonPriceTracker/crawler/urlcheckeroutput.json')
        output = json.load(file)
        return [output[0]["valid"], float(output[0]["price"])]
    except:
        return [False, -1.0]
