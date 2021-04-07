import json, uuid, urllib.parse, time
from api.RedisCache import CacheBlueprint
import api.RedisCache as RedisCache


class AuthenticationResponse(CacheBlueprint):

    def __init__(self, guid=None, redirect_uri="", authentication_request_id="", state="", user_id="", released=False):
        self.state = state
        self.authentication_request_id = authentication_request_id
        self.user_id = user_id
        self.redeemed = False  # exchanged by client
        self.time_redeemed = 0
        self.released = released  # sent to client
        self.time_released = 0
        self.redirect_uri = redirect_uri

        if guid is not None:
            self.guid = guid

        self.store()

    def get_full_redirect_uri(self):
        return urllib.parse.urlparse(self.redirect_uri + "?code=" + self.guid + "&state=" + self.state).geturl()

    def redeem_token(self):
        self.redeemed = True
        self.time_redeemed = int(time.time())
        self.store()

    def release_token(self):
        self.released = True
        self.time_released = int(time.time())
        self.store()
