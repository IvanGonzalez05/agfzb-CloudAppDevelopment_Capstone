import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {}".format(url))
    api_key = "ydfmMHAr4bqft6IwjMSZBHMthGdNQt4z-RCpyo6Boj9z"
    try:
        # call get method of requests with url and params
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs,
            auth=HTTPBasicAuth('apikey', api_key)
        )
    except:
        print("Network exception occuredd")
    
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    print("POST to {}".format(url))
    print("body {}".format(json_payload))
    print("params {}".format(kwargs))
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        print("dealers")
        print(json_result)
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    print("dealer reviews")
    print(json_result)
    if json_result:
        reviews = json_result["rows"]
        for review in reviews:
            review_doc = review["doc"]
            review_obj = DealerReview(
                id=review_doc["id"],
                name=review_doc["name"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                dealership=review_doc["dealership"],
                review=review_doc["review"],
                purchase=review_doc["purchase"],
                purchase_date=review_doc["purchase_date"],
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
    return results

def analyze_review_sentiments(dealer_review):
    url = ""
    api_key = "ydfmMHAr4bqft6IwjMSZBHMthGdNQt4z-RCpyo6Boj9z"
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.get(
        url,
        params=params,
        headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth('apikey', api_key)
    )
