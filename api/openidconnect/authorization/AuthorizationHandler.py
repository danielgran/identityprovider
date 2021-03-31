import json, time

import api.RedisCache as RedisCache


class AuthenticationRequest(RedisCache.CacheBlueprint):
    # request is a flask object
    def __init__(self, client_id, state, nonce, scope, redirect_uri, code_challenge, code_challenge_method,
                 autostore=False):
        self.client_id = client_id
        self.state = state
        self.nonce = nonce
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method

        if autostore:
            self.store()

    def to_json(self):
        iam = {
            "client_id": self.client_id,
            "state": self.state,
            "nonce": self.nonce,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method
        }

        return json.dumps(iam)


# here the authorization progess starts.
# the browser is redirected to this page from the application which asks for federated authentication
# step is to save all the user request params
def handle_authentication_request(request):
    req_params = request.args

    # check necassery parameters

    assert (isinstance(req_params.get("client_id"), str))
    assert (isinstance(req_params.get("state"), str))
    assert (isinstance(req_params.get("scope"), str))
    assert (isinstance(req_params.get("nonce"), str))
    assert (isinstance(req_params.get("redirect_uri"), str))
    assert (isinstance(req_params.get("code_challenge"), str))
    assert (isinstance(req_params.get("code_challenge_method"), str))

    obj = AuthenticationRequest(req_params.get("client_id"), req_params.get("state"), req_params.get("nonce"), req_params.get("scope"),
                                req_params.get("redirect_uri"), req_params.get("code_challenge"), req_params.get("code_challenge_method"))
    obj.store(req_params.get("nonce"))
