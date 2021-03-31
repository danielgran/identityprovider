from ariadne.constants import PLAYGROUND_HTML
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType

from flask import Flask, request, jsonify

import redis, json

from api.base import db, redis_cache
from api.authorization.level1.authorization import level1_authorization

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
query.set_field("authorize", level1_authorization)


mutation = ObjectType("Mutation")
mutation.set_field("register", register_user)

schema = make_executable_schema(
    load_schema_from_path("schema.graphql"), query, mutation, snake_case_fallback_resolvers
)


if ENABLE_PLAYGROUND:
    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200


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


def transform_header_to_tuple(header):
    array = str(request.headers).replace("\r", "").replace(" ", "").split("\n")

    tuple = {}

    for i in array:

        if len(i) > 1:
            tuple[i.split(':')[0]] = i.split(":")[1]

    return tuple
