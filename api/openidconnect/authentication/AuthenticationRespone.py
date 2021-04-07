import json, uuid, urllib.parse, time
from api.RedisCache import CacheBlueprint
import api.RedisCache as RedisCache


class AuthenticationResponse(CacheBlueprint):

    def __init__(self, guid=None, redirect_uri="", authentication_request_id="", state="", user_id="", released=False):
        self.state = state
        self.authentication_request_id = authentication_id
        self.user_id = user_id
        self.redeemed = False  # exchanged by client
        self.time_redeemed = 0
        self.released = released  # sent to client
        self.time_released = 0

        self.redirect_uri = urllib.parse.urlparse(redirect_uri + "?code=" + self.guid + "&state=" + self.state).geturl()

        if guid is not None:
            self.guid = guid

        self.store()

    def redeem_token(self):
        self.redeemed = True
        self.time_redeemed = int(time.time())
        self.store()

    def release_token(self):
        self.released = True
        self.time_released = int(time.time())
        self.store()

    def to_json(self):
        iam = {
            "guid": self.guid,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "authentication_request_id": self.authentication_id,
            "user_id": self.user_id,
            "time_created": self.time_created,
            "released": self.released,
            "time_released": self.time_released
        }
        return json.dumps(iam)

    def load_from_cache(self):
        jsonstr = RedisCache.redisbase.get(self.guid)
        obj = json.loads(jsonstr)

        self.guid = obj['guid']
        self.redirect_uri = obj['redirect_uri']
        self.state = obj['state']
        self.authentication_request_id = obj['authentication_request_id']
        self.user_id = obj['user_id']
        self.time_created = obj['time_created']
        self.released = obj['released']
        self.time_released = obj['time_released']
        self.redeemed = obj['redeemed']
        self.time_redeemed = obj['time_redeemed']



