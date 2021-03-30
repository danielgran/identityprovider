import hashlib, random, base64, json

from api.base import redis_cache


class CacheUserSession():

    def __init__(self, address, authorization_level):
        self.address = address
        self.authorization_level = authorization_level

        # Session ID creation

        sha256_hash = hashlib.sha512(str(random.randint(1354684644,998478465))).hexdigest()
        self.id = base64.b64encode(sha256_hash)

    def register(self):
        if redis_cache.set(self.id, self.__repr__()):
            return True
        else:
            return False

    def __repr__(self):
        iam = {
            "id": self.id,
            "address": self.address,
            "authorization_level": self.authorizationlevel
        }

        return json.dumps(iam)
