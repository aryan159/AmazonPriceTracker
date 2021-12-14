from django.core.mail import send_mail
from django.conf import settings

from scrapy.crawler import CrawlerProcess

from twisted.internet import reactor
from twisted.internet.task import deferLater

import datetime, csv, json

from .web_scraper.web_scraper.spiders.amazon_price_spider import AmazonPriceSpider
from .models import Products


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    updateDB()
    return deferLater(reactor, seconds, lambda: None)

def updateDB():
    file = open('AmazonPriceTracker/crawler/output.json')
    output = json.load(file)
    print(output)
    for price in output:
        ASIN = list(price.keys())[0]
        current_product = Products.objects.get(ASIN=ASIN)
        print('[AAAAAAAAAAAAAAAA] tryna get previosu_price')
        #print(current_product)
        #print(current_product.prices_set.all())
        #print(current_product.prices_set.all()[0])
        #print(current_product.prices_set.all()[0].price)
        previous_price = None
        try: 
            previous_price = current_product.prices_set.all()[0].price
        except:
            previous_price = None
        current_price = float(list(price.values())[0])
        current_product.prices_set.create(price=current_price)
        if previous_price and current_price < previous_price:
            emails = list(current_product.emails_set.all())
            send_mail('Price Drop', 'Price has dropped',
                      settings.DEFAULT_FROM_EMAIL, emails)
            print('[AAAAAAAAAAAAAAA] sent email')
            print(emails)
    print('[AAAAAAAAAAAAA] Finished updating DB')

def postASINs():
    ASINs = []
    for product in Products.objects.all():
        ASINs.append(product.ASIN)
    filenameInput = 'AmazonPriceTracker/crawler/input.csv'
    with open(filenameInput, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(ASINs)
    print("Just Posted to crawler/input.csv")


def DailyWebScraper():
    now = datetime.datetime.now()
    filenameOutput = 'AmazonPriceTracker/crawler/output.json'
    file = open(filenameOutput, 'w')
    file.close()
    process = CrawlerProcess(settings={
            "FEEDS": {
            filenameOutput : {"format": "json"},
            },
        })

    def _crawl(result, spider):
        file = open(filenameOutput, 'w')
        file.close()
        postASINs()

        deferred = process.crawl(spider)
        deferred.addCallback(lambda results: print('waiting 60 seconds before restart...'))
        deferred.addCallback(sleep, seconds=60)
        deferred.addCallback(_crawl, spider)
        return deferred

    _crawl(None, AmazonPriceSpider)

    process.start()

#mainFunction()

""" def crawl():
    now = datetime.datetime.now()
    filename = f"crawler_output/{re.sub('/', '', now.strftime('%x'))}.json"
    file = open(filename, 'w')
    file.close()
    process = CrawlerProcess(settings={
        "FEEDS": {
           filename : {"format": "json"},
        },
    })

    process.crawl(AmazonPriceSpider)
    process.start(stop_after_crawl=False)

def schedule_task(task, frequency):
    ''' 
    Schedule a regular task

    Parameters:
        task (function): The task that we want to schedule
        frequency (int): number of times per day (choose factors of 24)
    '''
    now = datetime.datetime.now()
    numOfHours = 24/frequency
    startingHour = now.hour
    startingMinute = now.minute + 1

    while True:
        now = datetime.datetime.now()
        if (now.hour - startingHour) % numOfHours == 0 and now.minute == startingMinute:
            task()
            time.sleep(numOfHours*60*60 - 120) #sleep almost 24h
        else:
            time.sleep(15) #check every X seconds, adjust as you need
    
    return

def schedule_task_testing(task):
    ''' 
    Schedule a regular task

    Parameters:
        task (function): The task that we want to schedule
        frequency (int): number of times per day (choose factors of 24)
    '''
    now = datetime.datetime.now()
    startingMinute = now.minute + 1
    print('STARTING MINUTE IS: ' + str(startingMinute))

    while True:
        now = datetime.datetime.now()
        if (now.minute - startingMinute) % 2 == 0:
            print('[' + now.strftime('%X') + '] TRUE')
            task()
            time.sleep(100) #sleep ~2min
        else:
            print('[' + now.strftime('%X') + '] FALSE')
            time.sleep(15) #check every X seconds, adjust as you need
    
    return
 """
