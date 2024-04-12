from flask import Flask
from controller import validateJwtController

app = Flask(__name__)


@app.route('/auth', methods=['GET'])
def validateJWT():
    return validateJwtController()


if __name__ == '__main__':
    app.run(debug=True)
