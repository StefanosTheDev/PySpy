class InvalidParamError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class UsernameError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class PasswordError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class EmailInvalidError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class NoAccountsFoundError(Exception):
    pass
