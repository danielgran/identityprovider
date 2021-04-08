import urllib.parse, time, uuid
from api.RedisCache import CacheBlueprint


class AuthenticationResponse(CacheBlueprint):
    def __init__(self,
                 guid=None,
                 time_issued=int(time.time()),
                 user_id="",
                 expires_after=600,
                 redirect_uri="",

                 access_token="",
                 token_type="",
                 id_token="",
                 state="",
                 expires_in=0,
                 ):
        super(AuthenticationResponse, self).__init__()

        if guid is not None:
            self.guid = guid

        # Variable assignment
        self.time_issued = time_issued
        self.expires_after = expires_after
        self.redirect_uri = redirect_uri
        self.user_id = user_id

        self.access_token = guid  # Accesstoken is guid
        self.token_type = token_type
        self.id_token = id_token
        self.state = state
        self.expires_in = time_issued + expires_in



        self.store()

    @property
    def redirect_uri_with_params(self):
        return urllib.parse.urlparse(self.redirect_uri + "?code=" + self.guid + "&state=" + self.state).geturl()
