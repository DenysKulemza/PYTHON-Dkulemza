import datetime
import jwt
from flask import request, Response

from validation.valid import *
from validation.getters import *
from logger.warning_log import error_response

app.config['SECRET_KEY'] = 'secret key'


@app.route('/login')
def get_token():
    """Getting token by user sign in

    :return: token or response
    """
    request_data = request.get_json()
    if not valid_user_login(request_data):
        return Response(error_response(), 400, mimetype='application/json')

    center_id = User.query.filter_by(login=request_data['Login']).first()
    login = str(request_data['Login'])
    password = str(request_data['Password'])

    condition = valid_login_password(login, password)

    if condition:
        expiration_data = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        AccessToken.add_request(center_id.id, str(expiration_data))
        token = jwt.encode({'exp': expiration_data}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response(error_response(), 400, mimetype='application/json')


@app.route('/register', methods=['POST'])
def register():
    """Register center in database

    :return: response
    """
    request_data = request.get_json()
    if center_exists(request_data['Login']):
        return Response('Invalid token', status=401, mimetype='application/json')
    if valid_user(request_data):
        User.add_user(request, request_data['Login'], request_data['Password'], request_data['Address'])
        return Response("", status=201, mimetype='application/json')
    else:
        return Response(error_response(), status=400, mimetype='application/json')


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
        return Response('Invalid token', status=401, mimetype='application/json')
    request_data = request.get_json()
    if valid_animal_form(request_data) and valid_animals(request_data):
        Animal.add_animal(request, get_access().center_id, request_data['Name'], get_specie(request_data['Species']).description,
                          request_data['Age'],
                          request_data['Species'], get_specie(request_data['Species']).price)
        return Response("", status=201, mimetype='application/json')
    else:
        return Response(error_response(), status=400, mimetype='application/json')


@app.route('/animals')
def get_all_animals():
    """Getting all name of animals

    :return: all animals by name
    """
    return str(Animal.get_all_animal())


@app.route('/animals/<int:id>')
def get_animal(id):
    """Getting detailed information about animal by id

    :param id: id of some animal
    :return: detailed information about animal by id
    """
    return str(Animal.display_current_animal(id))


@app.route('/centers/<int:id>')
def get_center(id):
    """Getting information about some center by id

    :param id: id of some center
    :return: detailed information about center by id
    """
    return str(Animal.get_centers_animals(id))


@app.route('/species', methods=['POST'])
def register_specie():
    """Register specie in database

    :return: response
    """
    token = request.args.get('token')
    if valid_token(token, app.config['SECRET_KEY']):
        return Response('Invalid token', status=401, mimetype='application/json')
    request_data = request.get_json()
    if valid_specie_form(request_data) and valid_species(request_data):
        Specie.add_specie(request, request_data['Name'], request_data['Description'], request_data['Price'])
        return Response("", status=201, mimetype='application/json')
    else:
        return Response(error_response(), status=400, mimetype='application/json')


@app.route('/species')
def get_all_specie():
    """Get all species from database

    :return: species and amounts of them
    """
    return str([Specie.json(specie, len(list(Animal.query.filter_by(species=specie.name).all())))
                for specie in Specie.query.all()])


@app.route('/species/<int:id>')
def get_current_specie(id):
    """Get some specie by id

    :param id: id of some specie
    :return: return detailed view of Specie
    """
    return str(Specie.get_specie_animals(id))


@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    """Update some animal

    :param id: id of updating animal
    :return: nothing or response
    """
    request_data = request.get_json()
    if 'Name' in request_data and 'Age' in request_data:
        Animal.update_animal(request, id, request_data['Name'], request_data['Age'])
    elif 'Name' not in request_data and 'Age' in request_data:
        Animal.update_animal(request, id, None, request_data['Age'])
    else:
        Animal.update_animal(request, id, request_data['Name'], None)
    return Response('', status=204)


@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    """Delete animal by id

    :param id: id of deleting animal
    :return: response
    """
    token = request.args.get('token')
    if valid_token(token, app.config['SECRET_KEY']):
        return Response('Invalid token', status=401, mimetype='application/json')

    if Animal.check_animal_before_delete(id):
        return Response(error_response(), status=401, mimetype='application/json')
    else:
        if check_center_before_delete(get_access().center_id, id):
            Animal.delete_animal(request, id)
            return Response('', status=200, mimetype='application/json')
        else:
            return Response(error_response(), status=200, mimetype='application/json')


app.run(port=5001)
