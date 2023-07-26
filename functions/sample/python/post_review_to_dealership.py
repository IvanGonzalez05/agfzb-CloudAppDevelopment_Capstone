"""IBM Cloud Function that post a review to a dealership

Returns:
    Posted review
"""

import requests
from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(param_dict):
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        reviews_database = client["reviews"]
        new_review = reviews_database.create_document(param_dict["REVIEW"])
        if new_review.exists():
            print("document created successfully")
            return new_review
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


new_review = {
    "review": 
        {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }
}
params = {
    "COUCH_USERNAME": "c83e48b3-ddc6-4cb6-91d6-579a7eec5feb-bluemix",
    "IAM_API_KEY": "ydfmMHAr4bqft6IwjMSZBHMthGdNQt4z-RCpyo6Boj9z",
    "REVIEW": new_review
}

main(params)