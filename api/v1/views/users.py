#!/usr/bin/python3
'''
Create a new view for User objects that handles all default HTTP methods
'''
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def return_users():
    ''' Retrieves the list of all User objects, use GET http method '''
    # save all the objects in State class from database
    users = storage.all(User)
    users_list = []
    for key, value in users.items():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def return_users_id(user_id):
    ''' Retrieve a User object using a specific id, use GET http method '''
    # save all the objects in State class from database
    users = storage.all(User)
    for key, value in users.items():
        # check if id passed is linked to User object
        # if so, return the User object
        if users[key].id == user_id:
            return value.to_dict()
    # raise error 404 if id is not liked to User object
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users_id(user_id):
    ''' Delete a State object using a specific id, use DELETE http method '''
    # save the object with the specific id from database
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    ''' Create a user object, use POST http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # create a new instance of User and pass body dict as **kwargs
    obj = User(**body)

    if 'email' not in body:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in body:
        return (jsonify({'error': 'Missing password'}), 400)
    else:
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_users_id(user_id):
    ''' Update a State object, use PUT http method '''
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        ignore_key = ['id', 'email', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(user, key, value)
            else:
                pass
        storage.save()
        return (jsonify(user.to_dict()), 200)
