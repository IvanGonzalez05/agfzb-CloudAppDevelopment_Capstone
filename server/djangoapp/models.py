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


# <HINT> Create a plain Python class `DealerReview` to hold review data
