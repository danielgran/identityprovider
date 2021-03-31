import hashlib, random, base64, json

from api.base import redis_cache


class CacheUserSession():

    def __init__(self, address, authorization_level):
        self.address = address
        self.authorization_level = authorization_level

        # Session ID creation

        sha256_hash = hashlib.sha256(str(random.randint(100, 2000)).encode('utf-8')).hexdigest()

        self.id = sha256_hash

    def register(self):
        if redis_cache.set(self.id, self.__repr__()):
            return True
        else:
            return False


    def __repr__(self):
        iam = {
            "id": self.id,
            "address": self.address,
            "authorization_level": self.authorization_level
        }

        return json.dumps(iam)


class CacheBlueprint:
    import time

    stored = False
    created = int(time.time())

    def store(self, uid):
        assert (isinstance(self.to_json(), str))
        assert (uid is not None)
        redis_cache.set(uid, self.to_json(), ex=600)  # ex=600 delete cache object after 10 minutes
        self.stored = True

    def to_json(self):
        pass
