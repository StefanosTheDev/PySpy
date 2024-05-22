from flask import request, jsonify, Flask, Blueprint
from GlobalErrorHandling.ServiceException import InvalidParamError, UsernameError, PasswordError, EmailInvalidError
from Service.AccountService import AccountService
from sqlalchemy.exc import IntegrityError


accounts_api = Blueprint('accounts', __name__)

@accounts_api.post('/accounts/create_account')
def create_account():
    try: 
        # Retrieve Data 
        data = request.get_json()

        if data is None: 
            raise InvalidParamError("No JSON payload found")
        
        expected_param_set = {'email', 'username', 'password'}
        key_list = [value for value in data.keys()]  # Return a list
        key_list_set = set(key_list)  # Convert to set

        if key_list_set == expected_param_set:  # Compare sets and this is approved.
            email = AccountService.check_email(data['email'])
            username = AccountService.check_username(data['username'])
            password = AccountService.check_password(data['password'])
            account = AccountService.register_account(email, username, password)
            return jsonify({"account": account.json()}), 201
        else:
            raise InvalidParamError('Incoming request has invalid parameters')
    except (InvalidParamError, UsernameError, PasswordError, EmailInvalidError, IntegrityError, ValueError) as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(error)
        return jsonify({"error": "An unexpected error occurred"}), 500

@accounts_api.get('/accounts/getAllAccounts')
def getAccounts():
    pass

@accounts_api.post('/accounts/login')
def login():
    pass

@accounts_api.put('/accounts/update_account')
def update_account_by_id():
    pass

@accounts_api.get('/accounts/getAccountById')
def get_account_by_id():
    pass

@accounts_api.delete('/accounts/deleteAccountById')
def delete_account_by_id():
    pass
