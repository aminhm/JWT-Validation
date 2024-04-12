from utils import getJwtToken, getJwtHeader, checkJwtHeader, getPemCertificate, verifyJwtSignature, checkTime
from flask import jsonify
import jwt

def validateJwtController():
    # Get the JWT from Authorization header
    jwtToken = getJwtToken()
    
    try:
        # get Jwt header
        decodedTokenHeader = getJwtHeader(jwtToken)
        
        # check the x5u and alg parameter inside the header
        headerChecking = checkJwtHeader(decodedTokenHeader)
        if(headerChecking[1]!=200):
            return headerChecking
        
        # get the PEM-encoded certificate
        pemCertificate = getPemCertificate(decodedTokenHeader)
        
        # Verify the JWT signature
        decodedTokenPayload = verifyJwtSignature(jwtToken,pemCertificate)
        
        # check the expiration time
        timeChecing = checkTime(decodedTokenPayload)
        if(timeChecing[1]!=200):
            return timeChecing
        
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
