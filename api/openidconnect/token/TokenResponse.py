import json, uuid

from api.RedisCache import CacheBlueprint

import api.RedisCache as RedisCache



class TokenResponse(CacheBlueprint):

    def __init__(self, guid=None, id_token="", access_token="", refresh_token="", token_type="", expires_in="", user_id=""):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in

        # Identify User
        self.user_id = user_id

        if guid is not None:
            self.guid = guid


    def generate(self, gen_refr_tkn=False):
        self.access_token = str(uuid.uuid4())
        if gen_refr_tkn:
            self.refresh_token = str(uuid.uuid4())
        self.store()


    def to_json(self):
        iam = {
            "guid": self.guid,
            "id_token": self.id_token,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in
        }
        return json.dumps(iam)

    def load_from_cache(self):
        jsonstr = RedisCache.redisbase.get(self.guid)
        obj = json.loads(jsonstr)

        self.guid = obj["obj"]
        self.id_token = obj["id_token"]
        self.access_token = obj["access_token"]
        self.refresh_token = obj["refresh_token"]
        self.token_type = obj["token_type"]
        self.expires_in = obj["expires_in"]