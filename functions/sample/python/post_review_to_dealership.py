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
