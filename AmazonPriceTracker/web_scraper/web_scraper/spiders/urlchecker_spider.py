import scrapy
import re
import csv

class URLCheckerSpider(scrapy.Spider):
    name = "urlchecker"

    def start_requests(self):
        file = open('AmazonPriceTracker/crawler/urlcheckerinput.csv')
        csvreader = csv.reader(file)
        url = next(csvreader)[0]
        print('[AAAAAAAAAAAAAAAAA] In spider, url is ')
        print(url)

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        price = response.css("span.apexPriceToPay *::text").get()
        name = response.css("span#productTitle *::text").get()
        print('[AAAAAAAAAAAAAAAAA] In spider, price is ')
        print(price)
        if not price:
            price = response.css("span.priceBlockBuyingPriceString").get()
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

        #with open('output.txt', 'w') as f:
        #   f.write(price)

        #self.logger.info("OUTPUTINGGGGGGGG " + price)

#process = CrawlerProcess(settings={
#    "FEEDS": {
#        "items.json": {"format": "json"},
#    },
#})

