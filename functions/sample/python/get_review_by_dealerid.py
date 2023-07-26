"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
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
        selector = { "dealership": { "$eq": param_dict["DEALERSHIP_ID"]}}
        reviews_result = reviews_database.get_query_result(selector)
        reviews = []
        for review in reviews_result:
            reviews.append(review)
        print({ "reviews": reviews })
        return { "reviews": reviews }
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
