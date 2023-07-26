from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
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
            return redirect('djangoapp/')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    # logout user in request. Its simple.
    logout(request)
    # return redirect(request, 'djangoapp:index', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # if http method is GET, render the form
    print('Registration')
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    # if http method is POST, create user
    elif request.method == "POST":
        print('is a post method')
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
            print('creating user')
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            print('login user')
            login(request, user=user)
            print('befor redirect')
            return redirect('djangoapp/')
        else:
            return render(request, 'djangoapp/registration.html', context)
        

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

