from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)
        # return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/55b76625-6fe5-492e-8ba0-484277bf348c/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        return HttpResponse(reviews)

@login_required
def add_review(request, dealer_id):
    # to validate if user is authenticated (changed for decorator)
    # if request.user.is_authenticated:
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/55b76625-6fe5-492e-8ba0-484277bf348c/dealership-package/post-review"
    review = {
        "time": datetime.utcnow().isoformat(),
        "dealership": 11,
        "review": "This is a great car dealer"
    }
    json_payload = { "review": review }
    response = post_request(url, json_payload, 11)
    return HttpResponse(response)