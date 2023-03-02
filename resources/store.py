import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

""" 
A Blueprint is used to divided bussiness logic in
multiple segments.
"""

blp = Blueprint("stores", __name__, description="Operations in Stores")


@blp.route("/stores/<string:store_id>")
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


# StoreList
# --------------------------------------------------------------------------
@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        try:
            return stores, 201
        except KeyError:
            abort(404, message="Store not found.")

    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(
                404,
                message="Bad request. Please ensure 'name' are inclued in the JSON payload",
            )
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="This store already exists")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
