from utils import *
from flask import jsonify
import jwt

def validate_jwt_controller():
    """
    Validate the JWT token provided in the request.

    Parameters:
    - request (Request): Flask request object.

    Returns:
    - tuple: A tuple containing JSON response and HTTP status code.
    """
    jwt_token = get_jwt_token()
    
    try:
        # get Jwt header
        decoded_token_header = get_jwt_header(jwt_token)
        
        # check the x5u and alg parameter inside the header
        header_checking = check_jwt_header(decoded_token_header)
        if(header_checking[1]!=200):
            return header_checking
        
        # get the PEM-encoded certificate
        pem_certificate = get_pem_certificate(decoded_token_header)
        
        # Verify the JWT signature
        decoded_token_payload = verify_jwt_signature(jwt_token,pem_certificate)
        
        # check the expiration time
        time_checking = check_time(decoded_token_payload)
        if(time_checking[1]!=200):
            return time_checking
        
        # JWT is valid
        return jsonify({'valid': True}), 200
        
    # JWT Expired Signature Error
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'error': 'JWT expired'}), 400
    # JWT Invalid Token Error
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'error': 'Invalid JWT format'}), 400
    # Other exceptions
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500
