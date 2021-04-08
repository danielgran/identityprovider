import urllib.parse

import api.RedisCache as RedisCache
from api.model.Application import Application


class AuthenticationRequest(RedisCache.CacheBlueprint):
    def __init__(self,
                 guid=None,
                 auto_store=False,

                 scope="",
                 response_type="",
                 client_id="",
                 redirect_uri="",
                 state="",

                 response_mode="",
                 nonce="",
                 display="",
                 prompt="",
                 max_age=0,
                 ui_locales="",
                 id_token_hint="",
                 login_hint="",
                 acr_values="",
                 code_challenge="",
                 code_challenge_method=""
                 ):

        super(AuthenticationRequest, self).__init__()

        # Required
        self.scope = scope
        self.response_type = response_type
        self.client_id = client_id
        self.redirect_uri = redirect_uri

        self.state = state
        self.response_mode = response_mode
        self.nonce = nonce
        self.display = display
        self.prompt = prompt
        self.max_age = max_age,
        self.ui_locales = ui_locales
        self.id_token_hint = id_token_hint
        self.login_hint = login_hint
        self.acr_values = acr_values
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method
        self.auto_store = auto_store

        # conditional checks
        if guid is not None:
            self.guid = guid

        if auto_store:
            self.store()

    @property
    def authentication_uri_with_params(self):
        try:
            return urllib.parse.urlparse("http://localhost:8080/login" + "/?guid=" + self.guid + "&dest=http://localhost:5000/authorize").geturl()
        except:
            return ""

    def is_valid(self):
        # Check for mandatory parameters
        if not (self.guid and self.scope and self.response_type and self.redirect_uri and self.client_id):
            return False


        # Check if a proper client makes the request
        db_obj = Application.query.filter_by(client_id=self.client_id).first()
        if db_obj is None or not db_obj.uris:
            return False

        # Check if the supplied redirect_uri matches with one in the database
        for i in range(len(db_obj.uris)):
            if self.redirect_uri == db_obj.uris[i].redirect_uri:
                break
            if i+1 >= len(db_obj.uris):
                return False

        # Check if scope is present
        if not "openid" in self.scope:
            return False

        if self.response_type != "code":
            return False

        # Check for code challenge
        if self.code_challenge_method != "S256":
            return False

        return True



def handle_request(request):
    req_params = request.args
    # check necassery parameters

    # todo add a authentication model which can be filled different kind of information to handle the authentication from the user so he can possibly login with google, etc too

    assert (isinstance(req_params.get("email"), str))
    assert (isinstance(req_params.get("password"), str))

    obj = AuthenticationRequest(req_params.get("client_id"), req_params.get("state"), req_params.get("nonce"),
                                req_params.get("scope"),
                                req_params.get("redirect_uri"), req_params.get("code_challenge"),
                                req_params.get("code_challenge_method"))

    obj.store()
