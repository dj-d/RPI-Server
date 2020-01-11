from models.user_models import UserModel
from services.EmailSender import send_reset_password, send_otp

import hashlib
from random import randint


class LoginService:
    """
    TODO doc
    """

    def __init__(self, otp_digits=4):
        self.otp_digits = otp_digits
        self.user_model = UserModel()

    def create_user(self, name, surname, email, password):
        if name and surname and email and password:
            api_key = self.encrypt_string(email, password)
            return self.user_model.create(name, surname, email, api_key)

    def user_exist(self, email, api_key):
        return self.user_model.get_user(email, api_key)

    def set_otp_code(self, email, api_key):
        otp_code = self.generate_otp()
        self.user_model.create_otp(api_key, otp_code)
        if send_otp(email, otp_code):
            return True
        return False

    def clear_otp(self, api_key, otp):
        return self.user_model.delete_otp(api_key, otp)

    def user_login(self, email, api_key, otp):
        return self.user_model.get_user_with_otp(email, api_key, otp)

    def send_reset_pw(self, email, password):
        if self.user_model.get_user(email, self.encrypt_string(email, password)):
            return send_reset_password(email)
        return True

    # SHA256 - ENCRYPT
    def encrypt_string(self, email, password):
        hash_string = email + password + email.split('@')[0]
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def generate_otp(self):
        return randint(1000, 9999)

    def check_api_key(self, key):
        return self.user_model.check_api_key(key)
