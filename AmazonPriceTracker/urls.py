from django.urls import path

from . import views

app_name = "AmazonPriceTracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<str:ASIN>/", views.product, name="product"),
    path("activate", views.activate, name="activate")
]