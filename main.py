from ariadne.constants import PLAYGROUND_HTML
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType

from flask import Flask, request, jsonify

from api.base import db
from api.authorization.level1.authorization import level1_authorization

from api.registration.registration import register_user

ENABLE_PLAYGROUND = True

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:penis@127.0.0.1/dbidentityprovider"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["pool_pre_ping"] = True

app.debug = True

db.init_app(app)


query_authorized = ObjectType("Query")


mutation_authorized = ObjectType("Mutation")
mutation_authorized.set_field("register", register_user)


schema_authorized = make_executable_schema(
    load_schema_from_path("schema.graphql"), query_authorized, mutation_authorized, snake_case_fallback_resolvers
)

query_unauthorized = ObjectType("Query")
query_unauthorized.set_field("authorize", level1_authorization)

mutation_unauthorized = ObjectType("Mutation")

schema_unauthorized = make_executable_schema(
    load_schema_from_path("schema_unauthorized.graphql"), query_unauthorized, mutation_unauthorized, snake_case_fallback_resolvers
)



if ENABLE_PLAYGROUND:
    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200


@app.route("/api", methods=["POST"])
def apiendpoint():

    data = request.get_json()
    header = transform_header_to_tuple(request.headers)

    if header.get("Authorization") is None:
        success, result = graphql_sync(
            schema_unauthorized,
            data,
            context_value=request,
            debug=app.debug
        )
    else:
        try:
            success, result = graphql_sync(
                schema_authorized,
                data,
                context_value=request,
                debug=app.debug
            )
        except:
            success = False;
            result = {
                "error": "Error"
            }

    status_code = 200 if success else 400
    return jsonify(result), status_code


def transform_header_to_tuple(header):
    array = str(request.headers).replace("\r", "").replace(" ", "").split("\n")

    print(array)

    tuple = {}

    for i in array:

        if len(i) > 1:
            tuple[i.split(':')[0]] = i.split(":")[1]

    return tuple

