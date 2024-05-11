from flask import Flask

app = Flask(__name__) # This correct?


if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
