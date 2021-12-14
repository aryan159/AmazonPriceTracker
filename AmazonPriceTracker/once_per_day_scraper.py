from django.core.mail import send_mail
from django.conf import settings

from scrapy.crawler import CrawlerProcess

import csv, json

from .web_scraper.web_scraper.spiders.amazon_price_spider import AmazonPriceSpider
from .models import Prices, Products, Emails


def updateDB():
    file = open('AmazonPriceTracker/AmazonPriceTracker/crawler/output.json')
    output = json.load(file)
    print(output)

    for price in output:
        ASIN = list(price.keys())[0]
        current_product = Products.objects.get(ASIN=ASIN)
        previous_price = None
        try:
            previous_price = current_product.prices_set.all()[0].price
        except:
            previous_price = None
        current_price = float(list(price.values())[0])
        current_product.prices_set.create(price=current_price)

        if previous_price and current_price < previous_price:
            ProductName = current_product.name
            ProductURL = "amazon.sg/dp/" + current_product.ASIN
            emails = list(current_product.emails_set.all())
            send_mail(
                f"{ProductName} has dropped in price",
                f"The price of {ProductName} has dropped from {previous_price} to {current_price}. Buy it now: {ProductURL}",
                settings.DEFAULT_FROM_EMAIL, emails)


def postASINs():
    ASINs = []
    for product in Products.objects.all():
        ASINs.append(product.ASIN)
    filenameInput = 'AmazonPriceTracker/AmazonPriceTracker/crawler/input.csv'
    with open(filenameInput, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(ASINs)


def OncePerDayScraper():
    filenameOutput = 'AmazonPriceTracker/AmazonPriceTracker/crawler/output.json'
    file = open(filenameOutput, 'w')
    file.close()
    process = CrawlerProcess(settings={
            "FEEDS": {
            filenameOutput : {"format": "json"},
            },
        })

    postASINs()
    process.crawl(AmazonPriceSpider)
    process.start()
    updateDB()

