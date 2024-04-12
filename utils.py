import time
from flask import request, jsonify
import jwt
import requests

# Decode JWT without verifying header
def getJwtHeader(token):
    return jwt.get_unverified_header(token)

def getJwtToken():
    return request.headers.get('Authorization', '').split('Bearer ')[-1]

# Check if the required headers are present'
def checkJwtHeader(jwtHeader):
    if 'x5u' not in jwtHeader:
        return jsonify({'valid': False, 'error': 'x5u parameter missing in JWT header'}), 400
    if 'alg' not in jwtHeader:
        return jsonify({'valid': False, 'error': 'alg parameter missing in JWT header'}), 400
    if  jwtHeader['alg'] != 'RS256':
        return jsonify({'valid': False, 'error': 'Invalid signature algorithm. RS256 is expected.'}), 400
    return jsonify({'valid': True}), 200

# Fetch PEM-encoded certificate from the URL in x5u parameter
def getPemCertificate(jwtHeader):
    pemCertificate = requests.get(jwtHeader['x5u']).text
    return pemCertificate

# Verify JWT signature using the fetched certificate
def verifyJwtSignature(jwtToken,pemCertificate):
    return jwt.decode(jwtToken, pemCertificate, algorithms=['RS256'])

# Check issue time and expiration
def checkTime(JwtPayload):
    currentTime = int(time.time())
    if 'iat' in JwtPayload and JwtPayload['iat'] > currentTime:
        return jsonify({'valid': False, 'error': 'JWT issued in the future'}), 400
    if 'exp' in JwtPayload and JwtPayload['exp'] < currentTime:
        return jsonify({'valid': False, 'error': 'JWT expired'}), 400
    return jsonify({'valid': True}), 200