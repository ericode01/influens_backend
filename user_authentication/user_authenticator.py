import json

import bcrypt

from database.database_controller import DatabaseController


class UserAuthenticator:
    def __init__(self):
        self.databaseController = DatabaseController()
        self.enable_hashing = False

    def authenticate_user_by_email(self, email, password):
        user, password_hash = self.databaseController.get_user_for_email(email)

        if not user or not password_hash:
            user = {"authenticated": False, "error": "User not found"}
            return json.dumps(user)

        if self.enable_hashing:
            if bcrypt.checkpw(password, password_hash):
                user["authenticated"] = True
                return json.dumps(user)
        else:
            if password == password_hash:
                user["authenticated"] = True
                return json.dumps(user)

        return json.dumps({"authenticated": False, "error": "Incorrect email or password"})
