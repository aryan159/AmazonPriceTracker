from django.db import models

class Products(models.Model):
    ASIN = models.CharField(max_length=11)
    name = models.CharField(max_length=1000, default='Not Defined')

    def __str__(self):
        return self.name + ' (' +self.ASIN + ')'

class Prices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    price = models.FloatField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.price)

class Emails(models.Model):
    products = models.ManyToManyField(Products)
    email = models.CharField(max_length=70)

    def __str__(self):
        return self.email
