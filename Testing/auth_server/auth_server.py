from flask import Flask, request, jsonify
from keycloak.keycloak_openid import KeycloakOpenID
import jwt
import requests
import os

client_id = os.environ['KEYCLOAK_CLIENT_ID']
client_secret_key = os.environ['KEYCLOAK_CLIENT_SECRET_KEY']
server_url = os.environ['SERVER_URL']

KEYCLOAK_OPENID_CLIENT = KeycloakOpenID(server_url=server_url,
                                                client_id=client_id,
                                                client_secret_key=client_secret_key,
                                                realm_name='master'
                                                )
app = Flask(__name__)

def verify_jwt(token):
    try:
        # Decode and verify the JWT
        decoded = KEYCLOAK_OPENID_CLIENT.decode_token(token)
        return True, decoded
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError as e:
        print("Invalid token")
        return False, str(e)
    except Exception as e:
        print("Nesto je otislo do kurca", e)
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
