import scrapy
import re
import csv

class URLCheckerSpider(scrapy.Spider):
    name = "urlchecker"

    def start_requests(self):
        file = open('AmazonPriceTracker/AmazonPriceTracker/crawler/urlcheckerinput.csv')
        csvreader = csv.reader(file)
        url = next(csvreader)[0]

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        name = response.css("span#productTitle *::text").get()
        price = response.css("span.apexPriceToPay *::text").get()
        if not price:
            price = response.css("span.priceBlockBuyingPriceString *::text").get()
        if not price:
            price = response.css("span#price *::text").get()
        if not price:
            price = response.css("span#priceblock_ourprice *::text").get()
        price = re.sub("[^0-9.]", "", price)

        if not price:
            valid = False
        else:
            valid = True

        price = re.sub("[^0-9.]", "", price)
        #price = float(price)
        yield {
            "valid": valid,
            "price": price,
            "name": name,
        }

    
