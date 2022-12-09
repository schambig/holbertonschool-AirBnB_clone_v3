#!/usr/bin/python3
'''
Create a new view for Place objects that handles all default HTTP methods
'''
from models.user import User
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def return_places(city_id):
    '''
    Retrieves the list of all Place objects of a City, use GET http method
    '''
    # Return the object based on the class and its ID, or None if not found
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)
