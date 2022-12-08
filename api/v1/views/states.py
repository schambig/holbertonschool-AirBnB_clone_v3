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
