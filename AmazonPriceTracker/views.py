from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import re

from AmazonPriceTracker.url_checker import URLChecker, URLCheckerStarter
from .models import Products, Prices, Emails
from .daily_web_scraper import DailyWebScraper

email_re = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class ProductURLForm (forms.Form):
    product_url = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "URLForm", 
        "placeholder": "Enter your Amazon.sg link here",
        "autocomplete": "off",
    }))

class EmailForm(forms.Form):
    email = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Your Email Address"
    }))

def activate(request):
    DailyWebScraper()


def index(request):
    if request.method == 'POST':
        form = ProductURLForm(request.POST)
        url = ''
        if form.is_valid():
            url = form.cleaned_data["product_url"]
        else:
            print("[AAAAAAAAAAAAAA] Invalid in the first loop")
            return HttpResponseRedirect(reverse("AmazonPriceTracker:index"))
        #extract the 10 digits after /dp/
        position = url.find('/dp/')
        ASIN_user = url[position + 4 : position + 14]
        valid, price, name = URLChecker(url)
        if ASIN_user.isalnum() and valid:
            if not Products.objects.filter(ASIN=ASIN_user).exists():
                new_product = Products(ASIN=ASIN_user)
                new_product.name = name
                new_product.save()
                new_product.prices_set.create(price=price)
            print("[AAAAAAAAAAAAAA] Valid!")
            return HttpResponseRedirect(f"/product/{ASIN_user}")
        else:
            print("[AAAAAAAAAAAAAA] Invalid!")
            return render(request, "AmazonPriceTracker/new_index.html", {
                "form" : ProductURLForm(),
                "error" : "Invalid URL! Make sure you are on the product page and not on the search page"
            })
    return render(request, "AmazonPriceTracker/new_index.html", {
        "form" : ProductURLForm()
    })

def product(request, ASIN):
    current_product = Products.objects.get(ASIN=ASIN)
    prices = current_product.prices_set.all()
    name = current_product.name
    if request.method == 'POST':
        form = EmailForm(request.POST)
        email = ''
        if form.is_valid():
            email = form.cleaned_data["email"]
        else:
            return render(request, f"AmazonPriceTracker/new_product.html", {
                "ASIN": ASIN,
                "prices": prices,
                "form" : EmailForm(),
                "error" : "Invalid Email",
                "name": name,
            })
        if re.fullmatch(email_re, email):
            #add to db
            current_product = Products.objects.get(ASIN=ASIN)
            current_product.emails_set.create(email=email)
            return render(request, "AmazonPriceTracker/new_product.html", {
                "ASIN": ASIN,
                "prices": prices,
                "form" : EmailForm(),
                "name": name,
                "success": "Successfully added your email. We will inform you of any price drops on this product"
            })
        else:
            return render(request, "AmazonPriceTracker/new_product.html", {
                "ASIN": ASIN,
                "prices": prices,
                "form" : EmailForm(),
                "name": name,
                "error" : "Invalid Email"
            })

    return render(request, "AmazonPriceTracker/new_product.html", {
        "ASIN": ASIN,
        "prices": prices,
        "name": name,
        "form": EmailForm()
    })

