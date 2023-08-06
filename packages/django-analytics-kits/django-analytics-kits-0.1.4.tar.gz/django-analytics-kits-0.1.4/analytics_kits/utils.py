import nacl.secret
import nacl.utils
import hashlib

from analytics_kits import settings


class KitCrypt(object):

    def __init__(self):
        secret_key = hashlib.sha224(settings.SECRET_KEY).hexdigest()[:32]
        self.secret_box = nacl.secret.SecretBox(secret_key)
        self.nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    def decrypt(self, encrypted):
        return self.secret_box.decrypt(encrypted.decode('string_escape'))

    def encrypt(self, plain):
        return self.secret_box.encrypt(
            plain, self.nonce).encode('string_escape')
