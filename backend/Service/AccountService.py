from GlobalErrorHandling.ServiceException import (
    UsernameError, PasswordError, EmailInvalidError, NoAccountsFoundError, UserNotLoggedInError
)
from validate_email import validate_email
from Database.db import db
from Model.Models import AccountModel
from sqlalchemy.exc import IntegrityError
from flask import session

class AccountService:
    def register_account(email, username, password):
        try:
            AccountService.check_username(username)
            AccountService.check_password(password)
            AccountService.check_email(email)
            new_account = AccountModel(email=email, username=username, password=password)
            db.session.add(new_account)
            db.session.commit()
            return new_account
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email or Username already exists")
        except (UsernameError, PasswordError, EmailInvalidError) as error:
            db.session.rollback()
            raise error
        except Exception as error:
            db.session.rollback()
            raise error

    def delete_account_by_id(id):
        try: 
            user_account = AccountService.get_account_by_id(id)
            if user_account:
                db.session.delete(user_account)
                db.session.commit()
                return user_account
        except Exception as e:
            db.session.rollback()
            raise
    def update_account_by_id():
        pass

    def get_account_by_id(id):
        try:
            account = AccountModel.query.get(id)
            if not account:
                raise NoAccountsFoundError("Account ID does not exist")
            return account.json()
        except (Exception, NoAccountsFoundError) as error:
            raise error

    def get_all_accounts():
        try:
            accounts = AccountModel.query.all()
            if not accounts:
                raise NoAccountsFoundError('No accounts found in DB')
            accounts_json = [accounts.json() for accounts in accounts] ## create a list of the accounts
            return accounts_json
        except (Exception, NoAccountsFoundError) as error:
            raise error
        
    def login_account(username, password):
        try:
            account = AccountModel.query.filter_by(username=username).first()
            if not account:
                    raise UsernameError("User does not exist")
            if account.password == password:
                session['logged_in'] = True
                session['account_id'] = account.id
                session['username'] = account.username
                return account
            else:
                raise PasswordError('Password does not match this user')
        except (UsernameError, PasswordError, Exception) as error:
            raise error

    def check_username(username):
        try:
            if len(username) <= 5 or len(username) > 12:
                raise UsernameError("Error with length of username") 
            has_upper = any(letter.isupper() for letter in username)
            has_lower = any(letter.islower() for letter in username)
            if not (has_upper and has_lower):
                raise UsernameError("Upper and Lower Characters Missing "
                                    "In Username")
            return username
        except UsernameError as error:
            raise error
        except Exception as error:
            raise error

    def check_password(password):
        SPECIAL_CHARACTERS = "!@#$%^&*"
        try:
            if len(password) <= 5 or len(password) > 16:
                raise PasswordError('Password does not meet length reqs')

            has_upper = any(letter.isupper() for letter in password)
            has_lower = any(letter.islower() for letter in password)
            if not (has_upper and has_lower):
                raise PasswordError("Upper and Lower Characters Missing"
                                    " In Password")
            if not any(char.isdigit() for char in password):
                raise PasswordError("Password does not contain a num value")
            if not any(char in SPECIAL_CHARACTERS for char in password):
                raise PasswordError("Password does not contain a"
                                    "special character")

            return password  # Password is valid
        except PasswordError as error:
            print(f"Password validation failed: {error}")
            raise error
        except Exception as error:
            raise error

    def check_email(email):
        try:
            is_valid = validate_email(email)
            if is_valid:
                return email
            else:
                raise EmailInvalidError("Email Does Not Exist")
        except EmailInvalidError as error:
            raise error
        except Exception as error:
            raise error

    def logout_account():
        try:
        # Check if the user is logged in
            if 'logged_in' in session and session['logged_in']:
                # Clear the session data
                session.pop('logged_in', None)
                session.pop('account_id', None)
                session.pop('username', None)
                return {"message": "Successfully logged out"}
            else:
                raise UserNotLoggedInError("No user is currently logged in")
        except (UserNotLoggedInError, Exception) as error:
            raise error
 
