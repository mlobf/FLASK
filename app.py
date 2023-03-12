import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager


from db import db
from blocklist import BLOCKLIST

import models
from resources import item, store
from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint

app = Flask(__name__)


app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Store REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https:cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)

app.config[
    "JWT_SECRET_KEY"
] = "my-Super+Secret@goFlash.com"  # Change this S@#th before make deployment process.

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_heather, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_heather, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked", "error": "token revoked"}
        ),
        401,
    )



@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # Change this ...... for something like = Look to database and see whether if user is a admin
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback(jwt_heather, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "autorization required",
            }
        ),
        401,
    )


@app.before_first_request
def create_tables():
    print("Tables are Created!!!")
    db.create_all()


api.register_blueprint(ItemBluePrint)
api.register_blueprint(StoreBluePrint)
api.register_blueprint(TagBluePrint)
api.register_blueprint(UserBluePrint)


if __name__ == "__main__":
    app.run(debug=True)
