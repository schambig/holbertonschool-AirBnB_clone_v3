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
    # retrieve the object based on the class and its ID, or None if not found
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def return_place_id(place_id):
    ''' Retrieve a Place object using its id, use GET http method '''
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                strict_slashes=False)
def delete_place_id(place_id):
    ''' Delete a Place object using its id, ise DELETE http method '''
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)
