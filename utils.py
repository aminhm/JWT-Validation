import time
from flask import request, jsonify
import jwt
import requests

def get_jwt_header(token: str) -> dict:
    """
    Decode JWT header without verifying the signature.

    Parameters:
    - token (str): JWT token string.

    Returns:
    - dict: Decoded JWT header.
    """
    return jwt.get_unverified_header(token)

def get_jwt_token() -> str:
    """
    Get JWT token from the Authorization header in the request.

    Returns:
    - str: JWT token string.
    """
    return request.headers.get('Authorization', '').split('Bearer ')[-1]

def check_jwt_header(jwt_header : dict) -> tuple:
    """
    Check if the required parameters are present in the JWT header.

    Parameters:
    - jwt_header (dict): Decoded JWT header.

    Returns:
    - tuple: A tuple containing JSON response and HTTP status code.
    """
    if 'x5u' not in jwt_header:
        return jsonify({'valid': False, 'error': 'x5u parameter missing in JWT header'}), 400
    if 'alg' not in jwt_header:
        return jsonify({'valid': False, 'error': 'alg parameter missing in JWT header'}), 400
    if  jwt_header['alg'] != 'RS256':
        return jsonify({'valid': False, 'error': 'Invalid signature algorithm. RS256 is expected.'}), 400
    return jsonify({'valid': True}), 200

def get_pem_certificate(jwt_header: dict) -> str:
    """
    Fetch PEM-encoded certificate from the URL specified in the JWT header inside 'x5u' parameter.

    Parameters:
    - jwt_header (dict): Decoded JWT header.

    Returns:
    - str: PEM-encoded certificate string.
    """
    pemCertificate = requests.get(jwt_header['x5u']).text
    return pemCertificate


def verify_jwt_signature(jwt_token: str, pem_certificate: str) -> dict:
    """
    Verify JWT signature using the fetched certificate.

    Parameters:
    - jwt_token (str): JWT token string.
    - pem_certificate (str): PEM-encoded certificate string.

    Returns:
    - dict: Decoded JWT payload.
    """
    return jwt.decode(jwt_token, pem_certificate, algorithms=['RS256'])

def check_time(jwt_payload: dict) -> tuple:
    """
    Check if the JWT token's issue time and expiration are valid.

    Parameters:
    - jwt_payload (dict): Decoded JWT payload.

    Returns:
    - tuple: A tuple containing JSON response and HTTP status code.
    """
    current_time = int(time.time())
    if 'iat' in jwt_payload and jwt_payload['iat'] > current_time:
        return jsonify({'valid': False, 'error': 'JWT issued in the future'}), 400
    if 'exp' in jwt_payload and jwt_payload['exp'] < current_time:
        return jsonify({'valid': False, 'error': 'JWT expired'}), 400
    return jsonify({'valid': True}), 200