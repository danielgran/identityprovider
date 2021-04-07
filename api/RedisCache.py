import hashlib, random, base64, json, uuid, jsonpickle, time

from api.base import redis_cache as redisbase

from collections import UserDict

class CacheUserSession():

    def __init__(self, address, authorization_level):
        self.address = address
        self.authorization_level = authorization_level

        # Session ID creation

        sha256_hash = hashlib.sha256(str(random.randint(100, 2000)).encode('utf-8')).hexdigest()

        self.id = sha256_hash

    def register(self):
        if redisbase.set(self.id, self.__repr__()):
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


class CacheBlueprint(UserDict):

    guid = str(uuid.uuid4())
    stored = False
    time_created = int(time.time())


    def __init__(self):
        self.guid = str(uuid.uuid4())
        self.stored = False
        self.time_created = int(time.time())


    def store(self):
        assert (isinstance(self.to_json(), str))
        redisbase.set(self.guid, self.to_json(), ex=1200)  # ex=600 delete cache object after 10 minutes
        self.stored = True

    def to_json(self):
        json = jsonpickle.encode(self)
        return json

    def load_from_cache(self):
        self.__dict__.update(jsonpickle.decode(redisbase.get(self.guid)).__dict__)
