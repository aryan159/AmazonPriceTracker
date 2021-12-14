from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

import re

from AmazonPriceTracker.url_checker import URLChecker
from .models import Products

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

#Main Page
#Handles the entering of product URLs
def index(request):

    #handle url form
    if request.method == 'POST':
        #retrieve form data
        form = ProductURLForm(request.POST)
        #server-side validation
        if form.is_valid():
            url = form.cleaned_data["product_url"]
        else:
            #return the form with error messages
            return render(request, "AmazonPriceTracker/new_index.html", {
                "form" : form,
            })

        #check that the user entered URL is valid and get price & name
        valid, price, name = URLChecker(url)

        #extract the 10 digits after /dp/ in the url which will give us the ASIN
        position = url.find('/dp/')
        ASIN_user = url[position + 4 : position + 14]
        
        #if the url is valid
        if ASIN_user.isalnum() and valid:
            #if product does not exist in the db, add it to the db along with its price and name
            if not Products.objects.filter(ASIN=ASIN_user).exists():
                new_product = Products(ASIN=ASIN_user)
                new_product.name = name
                new_product.save()
                new_product.prices_set.create(price=price)
            #redirect to the product page
            return HttpResponseRedirect(f"/product/{ASIN_user}")
        else:
            #return error message
            return render(request, "AmazonPriceTracker/new_index.html", {
                "form" : ProductURLForm(),
                "error" : "Invalid URL! Make sure you are on the product page and not on the search page"
            })
    #handle get request
    else:
        return render(request, "AmazonPriceTracker/new_index.html", {
            "form" : ProductURLForm()
        })

#Product Page
#Displays product price history & notifies user via email when the price drops
def product(request, ASIN):

    #get current product info
    current_product = Products.objects.get(ASIN=ASIN)
    prices = current_product.prices_set.all()
    name = current_product.name

    #handle email form
    if request.method == 'POST':
        form = EmailForm(request.POST)
        #server-side validation
        if form.is_valid():
            email = form.cleaned_data["email"]
        else:
            return render(request, f"AmazonPriceTracker/new_product.html", {
                "ASIN": ASIN,
                "prices": prices,
                "form" : form,
                "name": name,
            })

        #check email via regex
        if re.fullmatch(email_re, email):
            #add email to db
            current_product = Products.objects.get(ASIN=ASIN)
            current_product.emails_set.create(email=email)
            #return success message
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

    #handle get request
    return render(request, "AmazonPriceTracker/new_product.html", {
        "ASIN": ASIN,
        "prices": prices,
        "name": name,
        "form": EmailForm()
    })

