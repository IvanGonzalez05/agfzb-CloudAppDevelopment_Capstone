from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    inlines= [CarModelInline]

# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake)
