from flask import request, Response
from db.user_db import *
from db.settings import *
from validation.valid import valid_user
import logging

logging.basicConfig(filename='demo.log', level=logging.INFO)


@app.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    if valid_user(request_data):
        logging.info(f'{request.method}, {request.url}')
        User.add_user(request_data['Login'], request_data['Password'], request_data['Address'])
        response = Response("", status=201, mimetype='application/json')
        return response
    else:
        invalid_user_error_msg = {
            "error": "Invalid user object passed in request",
            "helpString": "Data passed in similar to this {'login': login, 'password': password, ''address': address"
        }
        response = Response(json.dumps(invalid_user_error_msg), status=400, mimetype='application/json')
        return response


@app.route('/users')
def get_users():
    return User.get_all_users()


app.run(port=5000)
