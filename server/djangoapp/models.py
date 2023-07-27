from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=50, null=False, primary_key=True)
    description = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=50, null=False, primary_key=True)
    dealer_id = models.IntegerField(null=False)
    type = models.CharField(max_length=50)
    year = models.DateField(null=True)
    # many to many relationship with car make
    carmakes = models.ManyToManyField(CarMake)

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # dealer address
        self.address = address
        # dealer city
        self.city = city
        # dealer full name
        self.full_name = full_name
        # dealer id
        self.id = id
        # location lat
        self.lat = lat
        # location long
        self.long = long
        # dealer short name
        self.short_name = short_name
        # dealer state
        self.st = st
        # dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealership
        self.dealership = dealership
        # Dealer name
        self.name = name
        # Dealer purchase
        self.purchase = purchase
        # Dealer review
        self.review = review
        # purchase_date
        self.purchase_date = purchase_date
        # car_make
        self.car_make = car_make
        # car_model
        self.car_model = car_model
        # car_year
        self.car_year = car_year
        # sentiment
        self.sentiment = sentiment
        # id
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.full_name