from cryptography import fernet
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

def encrypt(file):
    try:
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        encrypted = cipher_suite.encrypt(file)
        # encode to urlsafe base64 format
        # encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        return encrypted
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(encrypted):
    try:
        # base64 decode
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded = cipher_suite.decrypt(encrypted)
        return decoded
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None