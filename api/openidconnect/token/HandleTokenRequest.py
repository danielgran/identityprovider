from api.openidconnect.token.TokenRequest import TokenRequest
from api.openidconnect.token.TokenResponse import TokenResponse
from api.openidconnect.ErrorResponse import ErrorResponse

from api.openidconnect.authentication.AuthenticationRespone import AuthenticationResponse


# post
def handle_token_request(request):
    # 1. verify access token against stored one
    grant_type = request.args.get("grant_type")
    code = request.args.get("code")
    redirect_uri = request.args.get("redirect_uri")
    code_verifier = request.args.get("code_verifier")

    tknreq = TokenRequest(grant_type=grant_type, code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)

    # verify valid
    if not tknreq.is_valid():
        return ErrorResponse("Invalid request" + tknreq.__repr__())

    # verify if accesstoken is legit

    auth_resp = AuthenticationResponse(guid=tknreq.code)
    auth_resp.load_from_cache()



    # 2. generate response and store in the redis database

    if auth_resp.guid and (auth_resp.guid == tknreq.code):
        # legit request now generate Response
        tkn_resp = TokenResponse(user_id=auth_resp.user_id)
        tkn_resp.generate()



    # 3. return response

    return tkn_resp
