import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema, StoreUpdateSchema
from db import db
from models import StoreModel


""" 
A Blueprint is used to divided bussiness logic in
multiple segments.
"""

blp = Blueprint("stores", __name__, description="Operations in Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store_id = request.get_json()
        try:
            return stores[store_id["id"]], 201
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        store_id = request.get_json()
        try:
            del stores[store_id["id"]]
            return stores, 201
        except KeyError:
            abort(404, message="Store not found.")

    @blp.arguments(StoreUpdateSchema)
    def put(self, store_id):
        try:
            _id = store_id["id"]
            stores[store_id["id"]] = store_id
            return stores, 201

        except:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        try:
            return stores.values()
        except KeyError:
            abort(404, message="Store not found.")

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreUpdateSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()

        except IntegrityError:
            abort(400, "A store with that name already exist.")

        except SQLAlchemyError:
            abort(500, "A error has occurred while add a store")

            return store, 201
