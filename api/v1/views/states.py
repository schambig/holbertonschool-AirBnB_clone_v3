#!/usr/bin/python3
'''
Create a new view for State objects that handles all default HTTP methods
'''
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def return_states():
    ''' Retrieves the list of all State objects, use GET http method '''
    # save all the objects in State class from database
    states = storage.all(State)
    states_list = []
    for key, value in states.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def return_states_id(state_id):
    ''' Retrieve a State object using a specific id, use GET http method '''
    # save all the objects in State class from database
    states = storage.all(State)
    for key, value in states.items():
        # check if id passed is linked to State object
        # if so, return the State object
        if states[key].id == state_id:
            return value.to_dict()
    # raise error 404 if id is not liked to State object
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states_id(state_id):
    ''' Delete a State object using a specific id, use DELETE http method '''
    # save the object with the specific id from database
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    ''' Create a State object, use POST http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # create a new instance of State and pass body dict as **kwargs
    obj = State(**body)

    if 'name' not in body:
        return (jsonify({'error': 'Mising name'}), 400)
    else:
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states_id(state_id):
    ''' Update a State object, use PUT http method '''
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        ignore_key = ['id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(state, key, value)
            else:
                pass
        storage.save()
        return (jsonify(state.to_dict()), 200)
