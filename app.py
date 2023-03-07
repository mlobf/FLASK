import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager


from db import db
import models
from resources import item, store
from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagBluePrint


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


@app.before_first_request
def create_tables():
    print("Tables are Created!!!")
    db.create_all()


api.register_blueprint(ItemBluePrint)
api.register_blueprint(StoreBluePrint)
api.register_blueprint(TagBluePrint)


if __name__ == "__main__":
    app.run(debug=True)
