# JWT Validation API

This project implements a simple API endpoint for validating JSON Web Tokens (JWT) passed in the Authorization header. It checks if the JWT is valid, and if not, provides information about why the validation failed.

## Installation

1. Clone this repository:

```
git clone https://github.com/aminhm/JWT-Validation.git
```

2. Install the required dependencies:

```
pip install flask PyJWT requests
```

3. For MacOS also:

```
pip install cryptography
```

4. For Windows also:

```
pip install pyjwt[crypto]
```

## Usage

1. Start the Flask application:

```
python api.py
```

2. Make a GET request to the `/auth` endpoint with the JWT included in the Authorization header.

Example request:

```
GET http://localhost:5000/auth HTTP/1.1
Host: localhost:5000
Accept: application/json
Authorization: Bearer <your_jwt_token>
```

3. Example response:

```json
{
  "valid": true
}
```

If the JWT is invalid, the response will contain an error message explaining why.

## Endpoint

The endpoint URL for validating JWTs is:

```
http://localhost:5000/auth
```

## Dependencies

- Flask: Web framework for building the API.
- PyJWT: Library for decoding and verifying JWTs.
- Requests: Library for making HTTP requests.
