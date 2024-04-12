from flask import Flask
from controller import *

app = Flask(__name__)

@app.route('/auth', methods=['GET'])
def validate_jwt_api():
    return validate_jwt_controller()

if __name__ == '__main__':
    app.run(debug=True)
