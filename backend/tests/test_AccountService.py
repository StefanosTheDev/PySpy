import unittest
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Service.AccountService import AccountService
from GlobalErrorHandling.ServiceException import EmailInvalidError, PasswordError, UsernameError

class test_email(unittest.TestCase):
    
    def test_valid_email(self):
        email = 'stefanos26sophocleous@gmail.com'
        foo = AccountService.check_email(email)
        self.assertEqual(foo, email)

    def test_invalid_email(self):
        email = '123'
        with self.assertRaises(EmailInvalidError) as error:
            AccountService.check_email(email)
        
        self.assertEqual(str(error.exception), "Email Does Not Exist")

class test_check_password(unittest.TestCase):
    
    def test_paswd_invalid_length(self):
        foo = 'afs'
        bar = 'asdfasdfasdfasdfasdfasdf'
        with self.assertRaises(PasswordError) as error:
            AccountService.check_password(foo)

        with self.assertRaises(PasswordError) as error:
            AccountService.check_password(bar)
        
        self.assertEqual(str(error.exception), 'Password does not meet length reqs')
    
    def test_paswd_missing_up_low(self):
        foo = 'STEFANOS'
        bar = 'stefanos'
        with self.assertRaises(PasswordError) as error:
            print(error)
            AccountService.check_password(foo)
        
        with self.assertRaises(PasswordError) as error:
            AccountService.check_password(bar)
        
        self.assertEqual(str(error.exception), "Upper and Lower Characters Missing"
                                    " In Password")

    def test_paswd_missing_digit(self):
        foo = 'Stefanos'
    
        with self.assertRaises(PasswordError) as error:
            print(error)
            AccountService.check_password(foo)

        self.assertEqual(str(error.exception), "Password does not contain a num value")
                                    
    def test_paswd_missing_special_char(self):
        foo = 'Stefanos3'
        
        with self.assertRaises(PasswordError) as error:
            print(error)
            AccountService.check_password(foo)

        self.assertEqual(str(error.exception), "Password does not contain a"
                                    "special character")
                                    
    def test_paswd_isvalid(self):
        foo = 'Stefanos3!!!'
        bar = AccountService.check_password(foo)
        self.assertEqual(foo, bar)

class test_check_username(unittest.TestCase):
    
    def test_username_invalid_min_length(self):
        foo = ''
        with self.assertRaises(UsernameError) as error:
            AccountService.check_username(foo)

        self.assertEqual(str(error.exception), "Error with length of username")

    def test_username_invalid_max_length(self):
        
        bar = 'fooobarasdfl;kjdsf;lkjasdflkjasdf'

        with self.assertRaises(UsernameError) as error:
            AccountService.check_username(bar)
        
        self.assertEqual(str(error.exception), "Error with length of username")

    def test_username_missing_upper(self):
        foo = 'stefanos'
        
        with self.assertRaises(UsernameError) as error:
            AccountService.check_username(foo)
        
        self.assertEqual(str(error.exception), "Upper and Lower Characters Missing "
                                    "In Username")

    def test_username_missing_lower(self):
        foo = 'STEFANOS'
        with self.assertRaises(UsernameError) as error: 
            AccountService.check_username(foo)
        
        self.assertEqual(str(error.exception), "Upper and Lower Characters Missing "
                                    "In Username")
        
    def test_username_isvalid(self):
        foo = 'Stefanos'
        result = AccountService.check_username(foo)
        self.assertEqual(foo, result)

class test_register_account(unittest.TestCase):
    
    def test_register_account_isvalid(self):
        pass

    def test_register_account_integrity_error(self):
        pass

    def test_register_account_username_error(self):
        pass

    def test_register_account_pass_error(self):
        pass

    def test_email_invalid_error(self):
        pass

    def test_register_account_exception(self):
        pass






class test_delete_account_by_id(unittest.TestCase):

    def test_account_id_not_found(self):
        pass
    def test_delete_account_isvalid(self):
        pass
    def test_delete_error_rollback(self):
        pass

class test_get_account_by_id(unittest.TestCase):

    def test_get_account_isvalid(self):
        pass

    def test_get_account_not_found(self):
        pass

    def test_get_account_exception_error(self):
        pass


if __name__ == '__main__':
    unittest.main()