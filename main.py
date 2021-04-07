import redis

from ariadne.constants import PLAYGROUND_HTML
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType
from flask import Flask, request, jsonify, Response

from api.base import db
import api.openidconnect.authentication.AuthenticationHandler as oidcAuthorize
import api.openidconnect.token.HandleTokenRequest as oidcToken
from api.openidconnect.ErrorResponse import ErrorResponse
from api.registration.registration import register_user

ENABLE_PLAYGROUND = True

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:penis@127.0.0.1/dbidentityprovider"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["pool_pre_ping"] = True
app.debug = True

db.init_app(app)

redis_cache = redis.Redis(host="localhost", port=6379, db=0)
redis_cache.flushdb(asynchronous=False)

query = ObjectType("Query")

mutation = ObjectType("Mutation")
mutation.set_field("register", register_user)

schema = make_executable_schema(
    load_schema_from_path("schema.graphql"), query, mutation, snake_case_fallback_resolvers
)


# GraphQL Playground
if ENABLE_PLAYGROUND:
    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200


# GraphQL Endpoint
@app.route("/api", methods=["POST"])
def api_endpoint():

    data = request.get_json()

    header = transform_header_to_tuple(request.headers)
    print("New request from " + str(request.remote_addr))

    success, result = graphql_sync(
        data=data,
        schema=schema,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


# Called when the user gets redirected to the IdP to sign in
@app.route("/authorize", methods=["GET"])
def api_authorize_get():
    print(request)
    obj = oidcAuthorize.handle_authentication_request(request)

    if isinstance(obj, ErrorResponse):
        # Bad request
        # TODO Content type is still text/html
        return Response(response=str(obj), content_type="application/json", status=400)

    resp = Response()
    resp.headers["Location"] = obj.redirect_uri_with_params
    return resp, 301


# Called when the user has given credentials to authenticate
@app.route("/authorize", methods=["POST"])
def api_authorize_post():
    print(request)
    obj = oidcAuthorize.handle_user_authentication(request)
    # todo error handling
    resp = Response()
    resp.headers["Location"] = obj.get_full_redirect_uri()
    return resp, 301


# Called whenever a token was sent to the client and now exchanged for an api access token
@app.route("/token", methods=["POST"])
def api_token_request():
    print(request)
    obj = oidcToken.handle_token_request(request)
    if isinstance(obj, ErrorResponse):
        # Bad request
        # TODO Content type is still text/html
        return Response(response=str(obj), content_type="application/json", status=400)

    resp = Response()
    resp.headers["Location"] = obj.redirect_uri
    return str(obj), 301


def transform_header_to_tuple(header):
    array = str(request.headers).replace("\r", "").replace(" ", "").split("\n")

    tuple = {}

    for i in array:

        if len(i) > 1:
            tuple[i.split(':')[0]] = i.split(":")[1]

    return tuple
