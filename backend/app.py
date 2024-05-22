from flask import Flask
from Database.db import db
from API.AccountsAPI import accounts_api

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./account.db'

# Suppress a warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_super_secret_key'

app.register_blueprint(accounts_api)

# Initialize the database
db.init_app(app)

# Create tables before the first request using an alternative approach
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
