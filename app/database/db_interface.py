import os

import pyrebase
import xxhash
import yaml
from flask import g

from ..models import User
from ..tools import keys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_NAME = "../config.yml"
CONFIG_DATA = yaml.safe_load(open(os.path.join(BASE_DIR, CONFIG_NAME)))

fbconf = {
    "apiKey": CONFIG_DATA["firebase"]["API_KEY"],
    "authDomain": CONFIG_DATA["firebase"]["AUTH_DOMAIN"],
    "databaseURL": CONFIG_DATA["firebase"]["DATABASE_URL"],
    "projectId": CONFIG_DATA["firebase"]["PROJECT_ID"],
    "storageBucket": CONFIG_DATA["firebase"]["STORAGE_BUCKET"],
    "messagingSenderId": CONFIG_DATA["firebase"]["SENDER_ID"],
    "serviceAccount": CONFIG_DATA["firebase"]["SERVICE_ACCOUNT"],
}

firebase = pyrebase.initialize_app(fbconf)
auth = firebase.auth()
db = firebase.database()


class DBInterface:
    @classmethod
    def create_user(self, data):
        """Creates new user from form request data"""
        if data["password"] != data["confirm_password"]:
            return {"error": "Passwords do not match"}

        try:
            user = auth.create_user_with_email_and_password(
                data["email"], data["password"]
            )
        except Exception as e:
            if "EMAIL_EXISTS" in str(e):
                return {"error": "Account with that email address already exists"}
            elif "WEAK_PASSWORD" in str(e):
                return {"error": "Password must be at least 6 characters long"}
            else:
                return {"error": "An unknown error occured"}

        auth.send_email_verification(user["idToken"])

        key = keys.generate_key()
        while self.valid_key(key):
            key = keys.generate_key()

        data = {
            "uid": user["localId"],
            "first-name": data["first_name"],
            "last-name": data["last_name"],
            "email": data["email"],
            "api-key": key,
            "account-type": 0,
        }

        hash_id = xxhash.xxh64(user["localId"], seed=g.hash_seed).hexdigest()
        db.child("users").child(hash_id).set(data)
        db.child("keys").child(hash_id).set({"key": data["api-key"]})

        user_obj = User(data, hash_id)

        return {"user": user_obj}

    @classmethod
    def authenticate_user(self, data):
        """Attempts to authenticate existing user"""

        try:
            user = auth.sign_in_with_email_and_password(data["email"], data["password"])
        except Exception as e:
            if "EMAIL_NOT_FOUND" in str(e):
                return {"error": "Account with that email does not exist"}
            else:
                return {"error": "Email or password are incorrect"}
        else:
            info = auth.get_account_info(user["idToken"])

        if info["users"][0]["emailVerified"] is False:
            return {"error": "Account is not yet verified"}

        hash_id = xxhash.xxh64(user["localId"], seed=g.hash_seed).hexdigest()
        data = db.child("users").child(hash_id).get()
        data = dict(data.val())

        user_obj = User(data, hash_id)

        return {"user": user_obj}

    @classmethod
    def get_user(self, id):
        """Returns user object from database"""
        try:
            data = db.child("users").child(id).get()
        except Exception:
            return None

        if data is None:
            return None

        try:
            data = dict(data.val())
        except Exception:
            return None

        user_obj = User(data, id)

        return user_obj

    @classmethod
    def reset_user(self, data):
        """Sends password reset email for authenticated users"""
        try:
            auth.send_password_reset_email(data["email"])
        except Exception:
            return {"error": "Email does not exist"}
        return {}

    @classmethod
    def valid_key(self, key):
        """Determines if key already exists within database"""
        query_data = db.child("keys").get()

        try:
            for data in query_data.each():
                if data.val()["key"] == key:
                    return True
                continue
        except Exception:
            return False
        return False
