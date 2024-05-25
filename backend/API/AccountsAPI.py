from flask import request, jsonify, Flask, Blueprint, session
from GlobalErrorHandling.ServiceException import InvalidParamError, UsernameError, PasswordError, EmailInvalidError, NoAccountsFoundError, UserNotLoggedInError
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
    except (InvalidParamError, UsernameError, PasswordError, EmailInvalidError, IntegrityError, ValueError, Exception) as error:
        return jsonify({"error": str(error)}), 400

@accounts_api.post('/accounts/login')
def login():
    try: 
        data = request.get_json()
        if data is None:
            raise InvalidParamError("No JSON payload found")
        
        expected_param_set = {'username', 'password'}
        key_list = [value for value in data.keys()]
        key_list = set(key_list)

        if key_list == expected_param_set:
            username, password = data['username'], data['password']
            account = AccountService.login_account(username, password)
            if account: # if account exist whichmeans login worked
                print(session['logged_in'])
                print(session['account_id'])
                print(session['username'])
                return jsonify({"Login Successfull": account.json()}), 201 # THis the right thing to do? 
        else:
            raise InvalidParamError('Incomming request has invalid params')
    except (UsernameError, InvalidParamError, PasswordError, Exception) as error: 
        return jsonify({"error": str(error)}), 400

@accounts_api.get('/accounts/getAllAccounts')
def getAccounts():
    try:
        list_of_accounts = AccountService.get_all_accounts()
        return jsonify({"accounts_list": list_of_accounts})
    except (NoAccountsFoundError, Exception) as error:
        return jsonify({"error": error})

@accounts_api.put('/accounts/update_account')
def update_account_by_id():
    pass

@accounts_api.get('/accounts/getAccountById/<int:account_id>')
def get_account_by_id(account_id):
    try:
        account = AccountService.get_account_by_id(account_id)
        return jsonify({"account": account})
    except (NoAccountsFoundError, Exception) as error:
        return jsonify({"error": str(error)}), 404


@accounts_api.delete('/accounts/deleteAccountById')
def delete_account_by_id():
    pass

@accounts_api.post('/accounts/logout')
def logout():
    try:
        result = AccountService.logout_account()
        return jsonify(result), 200
    except UserNotLoggedInError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500
