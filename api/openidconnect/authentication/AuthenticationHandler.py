from api.openidconnect.authentication.AuthenticationRequest import AuthenticationRequest
from api.openidconnect.authentication.AuthenticationRespone import AuthenticationResponse
from api.openidconnect.authentication.ErrorResponse import ErrorResponse
from argon2 import PasswordHasher

from api.model.User import User

# here the authorization progess starts.
# the browser is redirected to this page from the application which asks for federated authentication
# step is to save all the user request params


# When user is redirected
def handle_authentication_request(request):
    req_params = request.args
    # check necassery parameters

    # the client either logs or is redirected

    client_id = req_params.get("client_id")
    state = req_params.get("state")
    scope = req_params.get("scope")
    nonce = req_params.get("nonce")
    redirect_uri = req_params.get("redirect_uri")
    code_challenge = req_params.get("code_challenge")
    code_challenge_method = req_params.get("code_challenge_method")

    obj = AuthenticationRequest(client_id=req_params.get("client_id"), state=req_params.get("state"), nonce=req_params.get("nonce"), scope=req_params.get("scope"),
                                redirect_uri=req_params.get("redirect_uri"), code_challenge=req_params.get("code_challenge"), code_challenge_method=req_params.get("code_challenge_method"), autostore=True)
    if not obj.is_valid():
        return ErrorResponse("Error in arguments")

    return obj


def handle_user_authentication(request):

    guid = request.form.get("guid")
    email = request.form.get("email")
    password = request.form.get("password")

    if not guid or not email or not password:
        return ErrorResponse("False arguments")

    authobj = AuthenticationRequest(guid=guid)
    authobj.load_from_cache()

    userobj = User.query.filter_by(email=email).first()


    # password and email login

    ph = PasswordHasher()
    if ph.verify(userobj.password, password):
        authobj.authenticated = True
        authobj.store()
        # authentication response can be created

    #todo other providers like facebook or google



    # If the client has successfully authenticated
    auth_resp = AuthenticationResponse(authentication_request_id=authobj.guid, redirect_uri=authobj.redirect_uri, state=authobj.state)
    if authobj.authenticated:
        auth_resp.release_token()

    return auth_resp




