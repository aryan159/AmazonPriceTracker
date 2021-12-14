import scrapy
import re
import csv

class AmazonPriceSpider(scrapy.Spider):
    name = "amazon_price"

    def start_requests(self):
        file = open('AmazonPriceTracker/AmazonPriceTracker/crawler/input.csv')
        csvreader = csv.reader(file)
        ASINs = next(csvreader)
        for ASIN in ASINs:
            url = 'https://www.amazon.sg/dp/' + ASIN
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        price = response.css("span.apexPriceToPay *::text").get()
        if not price:
            price = response.css("span.priceBlockBuyingPriceString *::text").get()
        if not price:
            price = response.css("span#price *::text").get()
        if not price:
            price = response.css("span#priceblock_ourprice *::text").get()
        price = re.sub("[^0-9.]", "", price)
        yield {
            response.request.url.split('/')[-1]: price
        }

        
