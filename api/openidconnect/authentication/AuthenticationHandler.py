from argon2 import PasswordHasher

from api.openidconnect.authentication.AuthenticationRequest import AuthenticationRequest
from api.openidconnect.authentication.AuthenticationRespone import AuthenticationResponse
from api.openidconnect.ErrorResponse import ErrorResponse

from api.model.User import User


# GET via redirect from client
def handle_authentication_request(request):
    scope = request.args.get("scope")
    response_type = request.args.get("response_type")
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state")
    response_mode = request.args.get("response_mode")
    nonce = request.args.get("nonce")
    display = request.args.get("display")
    prompt = request.args.get("prompt")
    max_age = request.args.get("max_age")
    ui_locales = request.args.get("ui_locales")
    id_token_hint = request.args.get("id_token_hint")
    login_hint = request.args.get("login_hint")
    acr_values = request.args.get("acr_values")
    code_challenge = request.args.get("code_challenge")
    code_challenge_method = request.args.get("code_challenge_method")

    authentication_request = AuthenticationRequest(
                                                    scope=scope,
                                                    response_type=response_type,
                                                    client_id=client_id,
                                                    redirect_uri=redirect_uri,
                                                    state=state,
                                                    response_mode=response_mode,
                                                    nonce=nonce,
                                                    display=display,
                                                    prompt=prompt,
                                                    max_age=max_age,
                                                    ui_locales=ui_locales,
                                                    id_token_hint=id_token_hint,
                                                    login_hint=login_hint,
                                                    acr_values=acr_values,
                                                    code_challenge=code_challenge,
                                                    code_challenge_method=code_challenge_method,
                                                    auto_store=True)

    # Check integrity of the request
    if not authentication_request.is_valid():
        return ErrorResponse("Error in supplied arguments")


    return authentication_request


def handle_user_authentication(request):

    guid = request.form.get("guid")
    email = request.form.get("email")
    password = request.form.get("password")

    user_id = ""


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
        user_id = email
        # authentication response can be created

    #todo other providers like facebook or google



    # If the client has successfully authenticated

    if authobj.authenticated:
        auth_resp = AuthenticationResponse(authentication_request_id=authobj.guid, redirect_uri=authobj.get_, state=authobj.state)
        auth_resp.release_token()
        auth_resp.user_id = user_id
        return auth_resp




