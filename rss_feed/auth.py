import jwt
from functools import wraps
from flask import jsonify, request
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("C:/Users/Israh/PycharmProjects/RSS_REST_API/firebase-admin-sdk/firebase-sdk.json")
firebase_admin.initialize_app(cred)

SK = "randomsupersecretkey123"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://localhost:5000/route?token=xxx

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, SK)
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)

    return decorated


def verify_firebase_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise Exception('Invalid Firebase token')
