from flask import Flask, request, jsonify
from keycloak.keycloak_openid import KeycloakOpenID
import jwt
import requests


KEYCLOAK_OPENID_CLIENT = KeycloakOpenID(server_url='http://keycloak:8080/',
                                                client_id='mqtt_broker',
                                                client_secret_key='R1TppwB4HbAvdpYYDScNPQ1fbXzTyHk1',
                                                realm_name='master'
                                                )
app = Flask(__name__)

def verify_jwt(token):
    try:
        KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + KEYCLOAK_OPENID_CLIENT.public_key() + "\n-----END PUBLIC KEY-----"
        options = {"verify_signature": True,"verify_aud": True, "verify_exp": True}
        # Decode and verify the JWT
        decoded = KEYCLOAK_OPENID_CLIENT.decode_token(token)
        return True, decoded
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError as e:
        return False, str(e)
    except:
        return False, "Unknown error"

@app.route('/auth', methods=['POST'])
def authenticate():
    auth_data = request.get_json()
    print(auth_data)
    token = auth_data['username']
    is_valid, decoded_or_error = verify_jwt(token)
    if is_valid:
        # Implement additional checks if necessary (e.g., roles, permissions)
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False, 'error': decoded_or_error}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
