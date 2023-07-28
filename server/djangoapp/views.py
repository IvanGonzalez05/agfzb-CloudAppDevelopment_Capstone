from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

fake_dealerships = [
    {
        "_id":"b4fd620059e3126b951c144b7c16b2bb",
        "_rev":"1-34e7ebd07643af43db578a46ee1d6365",
        "id":1,
        "city":"El Paso",
        "state":"Texas",
        "st":"TX",
        "address":"3 Nova Court",
        "zip":"88563",
        "lat":31.6948,
        "long":-106.3,
        "short_name":"Holdlamis",
        "full_name":"Holdlamis Car Dealership"
    },
    {
        "_id":"b4fd620059e3126b951c144b7c16ba98",
        "_rev":"1-d1778a396ca8cb0ef2966a9854eb93ee",
        "id":2,
        "city":"Minneapolis",
        "state":"Minnesota",
        "st":"MN",
        "address":"6337 Butternut Crossing",
        "zip":"55402",
        "lat":44.9762,
        "long":-93.2759,
        "short_name":"Temp",
        "full_name":"Temp Car Dealership"
      },
    {
            "_id":"b4fd620059e3126b951c144b7c16c1d6",
            "_rev":"1-cc5d5c13aa879d1cef8253dfa1dce77d",
            "id":3,
            "city":"Birmingham",
            "state":"Alabama",
            "st":"AL",
            "address":"9477 Twin Pines Center",
            "zip":"35285",
            "lat":33.5446,
            "long":-86.9292,
            "short_name":"Sub-Ex",
            "full_name":"Sub-Ex Car Dealership"
         }
   ]

fake_reviews = [
      {
            "_id":"2f776d69d096c0262460927edb846e31",
            "_rev":"1-6d3a316e140863cdb147048888d26051",
            "id":1,
            "name":"Berkly Shepley",
            "dealership":15,
            "review":"Total grid-enabled service-desk",
            "purchase":True,
            "purchase_date":"07/11/2020",
            "car_make":"Audi",
            "car_model":"A6",
            "car_year":2010
      },
      {
            "_id":"2f776d69d096c0262460927edb847625",
            "_rev":"1-0cbc084ce570374a1d0c2653ceb254ad",
            "id":2,
            "name":"Gwenora Zettoi",
            "dealership":23,
            "review":"Future-proofed foreground capability",
            "purchase":True,
            "purchase_date":"09/17/2020",
            "car_make":"Pontiac",
            "car_model":"Firebird",
            "car_year":1995
         }
   ]

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact_us.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            context["user"] = user
            return render(request, 'djangoapp/index.html', context)

    return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
@login_required
def logout_request(request):
    context = {}
    # logout user in request. Its simple.
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # if http method is GET, render the form
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    # if http method is POST, create user
    elif request.method == "POST":
        # get user data from post request
        username = request.POST["username"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        password = request.POST["password"]

        user_exists = False
        try:
            # Check if user already exists
            User.objects.get(username)
            user_exists = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        
        if not user_exists:
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user=user)
            context["user"] = user
            return render(request, 'djangoapp/index.html', context=context)
        else:
            return render(request, 'djangoapp/registration.html', context)
        

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/55b76625-6fe5-492e-8ba0-484277bf348c/dealership-package/get_dealerships"
        # dealerships = get_dealers_from_cf(url)
        # context["dealerships"] = dealerships
        context["dealerships"] = fake_dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/55b76625-6fe5-492e-8ba0-484277bf348c/dealership-package/get-review"
        # reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = fake_reviews
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context=context)

@login_required
def add_review(request, dealer_id):
    # to validate if user is authenticated (changed for decorator)
    # if request.user.is_authenticated:
    context = {}
    if request.method == "GET":
        context["dealer_id"] = dealer_id
        context["cars"] = CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context=context)
    if request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/55b76625-6fe5-492e-8ba0-484277bf348c/dealership-package/post-review"
        review = {
            "time": datetime.utcnow().isoformat(),
            "dealership": 11,
            "review": "This is a great car dealer"
        }
        json_payload = { "review": review }
        response = post_request(url, json_payload, 11)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)