#!/usr/bin/python3
'''
Create a new view for State objects that handles all default HTTP methods
'''
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def return_states():
    ''' Retrieves the list of all State objects, use GET method '''
    # save all the objects in State class from database
    states = storage.all(State)
    states_list = []
    for key, value in states.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def return_states_id(state_id):
    ''' Retrieve a State object using a specific id '''
    # save all the objects in State class from database
    states = storage.all(State)
    for key, values in states.items():
        # check if id passed is linked to State object
        # if so, return the State object
        if states[key].id == state_id:
            return value.to_dict()
    # raise error 404 if id is not liked to State object
    abort(404)
