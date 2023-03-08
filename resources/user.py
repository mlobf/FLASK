import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from flask_sqlalchemy import query
from passlib.hash import pbkdf2_sha256

from db import db
from schemas import UserSchema
from models import UserModel

""" 
A Blueprint is used to divided bussiness logic in
multiple segments.
"""

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "User created sucessfully."}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    @blp.response(200, UserSchema)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted."}
