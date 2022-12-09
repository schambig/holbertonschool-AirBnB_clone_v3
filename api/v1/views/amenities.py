#!/usr/bin/python3
'''
Create a new view for Amenity objects that handles all default HTTP methods
'''
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def return_amenities():
    ''' Retrieves the list of all Amenity objects, use GET http method '''
    # save all the objects in Amenity class from database
    amenities = storage.all(Amenity)
    amenities_list = []
    for key, value in amenities.items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def return_amenities_id(amenity_id):
    ''' Retrieve an Amenity object using its id, use GET http method '''
    # save all the objects in Amenity class from database
    amenities = storage.all(Amenity)
    for key, value in amenities.items():
        # check if id passed is linked to Amenity object
        # if so, return the Amenity object
        if amenities[key].id == amenity_id:
            return value.to_dict()
    # raise error 404 if id is not liked to Amenity object
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities_id(amenity_id):
    ''' Delete an Amenity object using its id, use DELETE http method '''
    # save the object with the specific id from database
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    ''' Create an Amenity object, use POST http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # create a new instance of Amenity and pass body dict as **kwargs
    obj = Amenity(**body)

    if 'name' not in body:
        return (jsonify({'error': 'Missing name'}), 400)
    else:
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_id(amenity_id):
    ''' Update an Amenity object, use PUT http method '''
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        ignore_key = ['id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(amenity, key, value)
            else:
                pass
        storage.save()
        return (jsonify(amenity.to_dict()), 200)
