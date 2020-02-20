from flask import request, Response
from db.animal_db import *
from db.settings import *
import json
from validation.valid import valid_animals, check_center_id


@app.route('/animals', methods=['POST'])
def register_animal():
    request_data = request.get_json()
    if valid_animals(request_data):
        if check_center_id(request_data):
            Animal.add_animal(request_data['Center id'], request_data['Name'], request_data['Description'], request_data['Age'], request_data['Species'], request_data['Price'])
            response = Response("", status=201, mimetype='application/json')
            return response
    else:
        invalid_user_error_msg = {
            "error": "Invalid user object passed in request",
            "helpString": "Data passed in similar to this {'name': name, 'description': description, 'age': age, "
                          "'species': species, 'price': price "
        }
        response = Response(json.dumps(invalid_user_error_msg), status=400, mimetype='application/json')
        return response


app.run(port=5000)