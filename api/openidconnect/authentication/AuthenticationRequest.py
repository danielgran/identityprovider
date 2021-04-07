import json, uuid, urllib.parse
import api.RedisCache as RedisCache


class AuthenticationRequest(RedisCache.CacheBlueprint):
    # request is a flask object
    def __init__(self, client_id="", state="", nonce="", scope="", redirect_uri="", code_challenge="",
                 code_challenge_method="", autostore=False, guid=None):
        self.client_id = client_id
        self.state = state
        self.nonce = nonce
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method
        self.authenticated = False

        # conditional checks
        if guid is not None:
            self.guid = guid

        if autostore:
            self.store()

        self.login_uri = urllib.parse.urlparse(
            self.redirect_uri + "/?guid=" + self.guid + "&dest=http://localhost:5000/authorize").geturl()

    def is_valid(self):

        if (
                self.client_id and
                self.state and
                self.nonce and
                self.scope and
                self.redirect_uri and
                self.code_challenge and
                self.code_challenge_method):
            return True

        return False

    def to_json(self):
        iam = {
            "guid": self.guid,
            "client_id": self.client_id,
            "state": self.state,
            "nonce": self.nonce,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method,
            "authenticated": self.authenticated
        }

        return json.dumps(iam)

    def load_from_cache(self):
        jsonstr = RedisCache.redisbase.get(self.guid)
        obj = json.loads(jsonstr)

        self.client_id = obj['client_id']
        self.state = obj['state']
        self.nonce = obj['nonce']
        self.scope = obj['scope']
        self.redirect_uri = obj['redirect_uri']
        self.code_challenge = obj['code_challenge']
        self.code_challenge_method = obj['code_challenge_method']
        self.authenticated = obj['authenticated']


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
