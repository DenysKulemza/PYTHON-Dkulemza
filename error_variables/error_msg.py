""" Variables of error messages for response
"""
invalid_token_error_msg = 'Invalid token'

invalid_id_error_msg = 'Animal with this id doesn\'t exists'

invalid_species_error_msg = {
    "error": "Invalid specie object passed in request or specie is already exists. Price should be positive",
    "helpString": "Data passed in similar to this {'Name': name, 'Description': description, 'Price': price}"
}

invalid_animal_error_msg = {
    "error": "Invalid animal object passed in request or animal is already exists."
             " Age should be positive or Species doesn\'t exists",
    "helpString": "Data passed in similar to this {'Name': name, 'Age': age , 'Species': specie}"
}
invalid_user_error_msg = {
            "error": "Invalid user object passed in request",
            "helpString": "Data passed in similar to this {'Login': login, 'Password': password, ''Address': address}"
        }

invalid_sign_in_error_msg = 'Invalid login or password'


exists_center_error_msg = 'Center is already exists'


exists_animal_in_center_error_msg = 'This center could not delete this animal,' \
                                    ' because this animal is not in this center'
