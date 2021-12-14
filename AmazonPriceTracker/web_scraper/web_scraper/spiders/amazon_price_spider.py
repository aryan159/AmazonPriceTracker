import scrapy
import re
import csv

class AmazonPriceSpider(scrapy.Spider):
    name = "amazon_price"

    def start_requests(self):
        file = open('AmazonPriceTracker/AmazonPriceTracker/crawler/input.csv')
        csvreader = csv.reader(file)
        ASINs = next(csvreader)
        #ASINs = ['B081V6W99V', 'B01LWC5IMC']
        for ASIN in ASINs:
            url = 'https://www.amazon.sg/dp/' + ASIN
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("/")[-2]
        #filename = f'quotes-{page}.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log(f'Saved file {filename}')

        price = response.css("span.apexPriceToPay *::text").get()
        if not price:
            price = response.css("span.priceBlockBuyingPriceString *::text").get()
        if not price:
            price = response.css("span#price *::text").get()
        if not price:
            price = response.css("span#priceblock_ourprice *::text").get()
        price = re.sub("[^0-9.]", "", price)
        #price = float(price)
        yield {
            response.request.url.split('/')[-1]: price
        }

        #with open('output.txt', 'w') as f:
        #   f.write(price)

        #self.logger.info("OUTPUTINGGGGGGGG " + price)

#process = CrawlerProcess(settings={
#    "FEEDS": {
#        "items.json": {"format": "json"},
#    },
#})

