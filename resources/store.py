import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, StoreUpdateSchema

""" 
A Blueprint is used to divided bussiness logic in
multiple segments.
"""

blp = Blueprint("stores", __name__, description="Operations in Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
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
    def get(self):
        try:
            return stores, 201
        except KeyError:
            abort(404, message="Store not found.")

    @blp.arguments(StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="This store already exists")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
