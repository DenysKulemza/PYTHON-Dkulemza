import datetime
import jwt
from flask import request, Response

from json import dumps

from db.user_db import User
from db.animal_db import Animal
from db.access_request import AccessToken
from db.specie_db import Specie

from settings import app

from validation.valid import valid_user, valid_animals, valid_species
from validation.valid import center_exists, check_center_before_delete
from validation.valid import valid_token, valid_login_password

from validation.getters import get_access, get_specie

from error_variables.error_msg import exists_center_error_msg
from error_variables.error_msg import exists_animal_in_center_error_msg
from error_variables.error_msg import invalid_sign_in_error_msg
from error_variables.error_msg import invalid_token_error_msg
from error_variables.error_msg import invalid_id_error_msg
from error_variables.error_msg import invalid_animal_error_msg
from error_variables.error_msg import invalid_species_error_msg
from error_variables.error_msg import invalid_user_error_msg


app.config['SECRET_KEY'] = 'secret key'


@app.route('/login')
def get_token():
    """Getting token by user sign in

    :return: token or response
    """
    request_data = request.get_json()
    center_id = User.query.filter_by(login=request_data['Login']).first()
    login = str(request_data['Login'])
    password = str(request_data['Password'])
    condition = valid_login_password(login,
                                     password)

    if condition:
        expiration_data = datetime.datetime.utcnow() \
                          + datetime.timedelta(seconds=100)
        AccessToken.add_request(center_id.id, str(expiration_data))
        token = jwt.encode({'exp': expiration_data},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response(invalid_sign_in_error_msg,
                        400, mimetype='application/json')


@app.route('/register', methods=['POST'])
def register():
    """Register center in database

    :return: response
    """
    request_data = request.get_json()
    if center_exists(request_data['Login']):
        return Response(exists_center_error_msg,
                        status=401, mimetype='application/json')
    if valid_user(request_data):
        User.add_user(request, request_data['Login'],
                      request_data['Password'],
                      request_data['Address'])
        return Response("", status=201, mimetype='application/json')
    else:
        return Response(dumps(invalid_user_error_msg),
                        status=400, mimetype='application/json')


@app.route('/centers')
def get_centers():
    """Getting all centers from database

    :return: all centers form database
    """
    return str(User.get_all_centers())


@app.route('/animals', methods=['POST'])
def register_animal():
    """Register animal in database

    :return: response
    """
    token = request.args.get('token')
    if valid_token(token, app.config['SECRET_KEY']):
        return Response(invalid_token_error_msg,
                        status=401, mimetype='application/json')
    request_data = request.get_json()
    if valid_animals(request_data):
        Animal.add_animal(request, get_access().center_id,
                          request_data['Name'],
                          get_specie(request_data['Species']).description,
                          request_data['Age'],
                          request_data['Species'],
                          get_specie(request_data['Species']).price)
        return Response("", status=201, mimetype='application/json')
    else:
        return Response(dumps(invalid_animal_error_msg),
                        status=400, mimetype='application/json')


@app.route('/animals')
def get_all_animals():
    """Getting all name of animals

    :return: all animals by name
    """
    return str(Animal.get_all_animal())


@app.route('/animals/<int:animal_id>')
def get_animal(animal_id):
    """Getting detailed information about animal by id

    :param animal_id: id of some animal
    :return: detailed information about animal by id
    """
    return str(Animal.display_current_animal(animal_id))


@app.route('/centers/<int:center_id>')
def get_center(center_id):
    """Getting information about some center by id

    :param center_id: id of some center
    :return: detailed information about center by id
    """
    return str(Animal.get_centers_animals(center_id))


@app.route('/species', methods=['POST'])
def register_specie():
    """Register specie in database

    :return: response
    """
    token = request.args.get('token')
    if valid_token(token, app.config['SECRET_KEY']):
        return Response(invalid_token_error_msg,
                        status=401, mimetype='application/json')
    request_data = request.get_json()
    if valid_species(request_data):
        Specie.add_specie(request, request_data['Name'],
                          request_data['Description'],
                          request_data['Price'])
        return Response("", status=201, mimetype='application/json')
    else:
        return Response(dumps(invalid_species_error_msg),
                        status=400, mimetype='application/json')


@app.route('/species')
def get_all_specie():
    """Get all species from database

    :return: species and amounts of them
    """
    return str([Specie.json(specie,
                            len(list(Animal.query.
                                     filter_by(species=specie.name).all())))
                for specie in Specie.query.all()])


@app.route('/species/<int:specie_id>')
def get_current_specie(specie_id):
    """Get some specie by id

    :param specie_id: id of some specie
    :return: return detailed view of Specie
    """
    return str(Specie.get_specie_animals(specie_id))


@app.route('/animals/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    """Update some animal

    :param animal_id: id of updating animal
    :return: nothing or response
    """
    request_data = request.get_json()
    if 'Name' in request_data and 'Age' in request_data:
        Animal.update_animal(request, animal_id,
                             request_data['Name'], request_data['Age'])
    elif 'Name' not in request_data and 'Age' in request_data:
        Animal.update_animal(request, animal_id, None, request_data['Age'])
    else:
        Animal.update_animal(request, animal_id, request_data['Name'], None)
    return Response('', status=204)


@app.route('/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    """Delete animal by id

    :param animal_id: id of deleting animal
    :return: response
    """
    token = request.args.get('token')
    if valid_token(token, app.config['SECRET_KEY']):
        return Response(invalid_token_error_msg,
                        status=401, mimetype='application/json')

    if Animal.check_animal_before_delete(animal_id):
        return Response(dumps(invalid_id_error_msg),
                        status=401, mimetype='application/json')
    else:
        if check_center_before_delete(get_access().center_id, animal_id):
            Animal.delete_animal(request, animal_id)
            return Response('', status=200, mimetype='application/json')
        else:
            return Response(exists_animal_in_center_error_msg,
                            status=200, mimetype='application/json')


app.run(port=5001)
