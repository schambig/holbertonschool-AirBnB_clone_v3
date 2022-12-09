#!/usr/bin/python3
'''
Create a new view for Review object that handles all default HTTP methods
'''
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def return_reviews(place_id):
    '''
    Retrieves the list of all Review objects of a Place, use GET http method
    '''
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def return_review_id(review_id):
    ''' Retrieve a Review object using its id, use GET http method '''
    # retrieve the object based on the class and its ID, or None if not found
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())
