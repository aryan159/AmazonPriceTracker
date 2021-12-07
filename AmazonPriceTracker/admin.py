from django.contrib import admin

from .models import Products, Prices, Emails

# Register your models here.
admin.site.register(Products)
admin.site.register(Prices)
admin.site.register(Emails)
