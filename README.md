# AmazonPriceTracker
A web app to alert users of future price drops. Check it out at www.prizotracker.com

This project is built using Django (the web framework), SQLite (the database), Scrapy (the web crawler) and Bootstrap (front-end toolkit) and is hosted on Python Anywhere

The main page. Enter the product url you would like to start tracking
<img width="1440" alt="Main Page" src="https://user-images.githubusercontent.com/33245117/146040494-a94a676c-96b0-44f5-a754-658f480dc4b7.png">

The product page. Shows relevant price history and gives you an option to enter your email to get alerted of price drops.
<img width="1440" alt="Product Page" src="https://user-images.githubusercontent.com/33245117/146040822-10cd5357-5954-41bd-b47f-f1c57af91cd6.png">

The script runs once every 24 hours in the background, scraping through all the products in the database and alerting any relevant users of price drops

## Future Improvements
The inspiration for this project was to generate an income by sending affiliate links to users when alerting them of price drops. To to that, I will have to be approved as an amazon affiliate and replace and replace the links in the emails I send accordingly.

## Reproduce the code locally

To run this project, you will need to install all the appropriate dependencies

### Step 1
Create and activate a virtual environment. If not sure how to do so, refer to https://realpython.com/python-virtual-environments-a-primer/

### Step 2
Install all the dependencies. Navigate to the outer ProjectFolder with the "requirements.txt" file and execute the following command
```
pip install -r requirements.txt
```
### Step 3
Configure ProjectFolder/settings.py to send emails. The easiest way is via a google account. You will have to enable your google account for this via [this setting](https://myaccount.google.com/lesssecureapps). Then fill in the settings shown before

```
DEFAULT_FROM_EMAIL = '' #The email you will be sending from

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '' #The email you will be sending from
EMAIL_HOST_PASSWORD = '' #Password for your email
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Step 4
Schedule the daily crawl. Using cron should be the easiest on unix systems. 
```
python manage.py crawl
```
This script will
1. Crawl all the products in the database daily and
2. Alert the appropriate users in case of any price drops

### Step 5
Launch the project
```
python manage.py runserver --noreload --nothreading
```

Now the project is fully functional. Visit the url generated by the above command to interact with the web app.

## Things to talk about
1. Multiprocessing
2. Twisted Reactors

## Post - Mortem
Apparently something went wrong and the app now flags all links as invalid. I suspect that this has to do with Amazon.sg changing the names/ids of their html tags.


