import jwt
from functools import wraps
from flask import jsonify, request
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("C:/Users/Israh/PycharmProjects/RSS_REST_API/firebase-admin-sdk/firebase-sdk.json")
firebase_admin.initialize_app(cred)

SK = "randomsupersecretkey123"


# uid = '7UZTBh8Dghg7F5Kp7pwRsl7qMF52'
# custom_token = auth.create_custom_token(uid)
# print(custom_token.decode())

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get token from headers
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        if token.startswith('Bearer '):
            token = token[7:]  # Strip "Bearer " from the token

        try:
            # Assuming you are using Firebase to verify the token
            verify_firebase_token(token)
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)

    return decorated


def verify_firebase_token(token):
    try:
        print(f'verifying token... {token}')
        decoded_token = auth.verify_id_token(token)
        print("Token verified!")
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}")
        raise Exception('Invalid Firebase token')
