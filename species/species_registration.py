from flask import request, Response
from db.settings import *
from db.specie_db import *
from json import dumps
from validation.valid import valid_species


@app.route('/species', methods=['POST'])
def register():
    request_data = request.get_json()
    if valid_species(request_data):
        Specie.add_specie(request_data['Name'], request_data['Description'], request_data['Price'])
        response = Response("", status=201, mimetype='application/json')
        return response
    else:
        invalid_species_error_msg = {
            "error": "Invalid user object passed in request",
            "helpString": "Data passed in similar to this {'Name': name, 'Description': description, 'Price': price"
        }
        response = Response(dumps(invalid_species_error_msg), status=400, mimetype='application/json')
        return response

