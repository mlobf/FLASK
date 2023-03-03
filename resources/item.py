import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema

""" 
A Blueprint is used to divided bussiness logic in
multiple segments.
"""

blp = Blueprint("items", __name__, description="Operations on items")


# --------------------------------------------------------------------------
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return items.values()
        except KeyError:
            abort(404, message="Items not found.")

    # Item Create Item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        try:
            for item in items.values():
                if (
                    item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]
                ):
                    abort(
                        404,
                        message="Item already exist",
                    )

            item_id = uuid.uuid4().hex
            new_item = {**item_data, "id": item_id}
            items[item_id] = new_item

            return new_item, 201
        except Exception as e:
            abort(404, "Bad request.")

    # Item Put Item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_data):
        try:
            items[item_data["id"]] |= item_data
            return items
        except Exception as e:
            print("erro ", e)
            abort(404, message=f"item has a problem {e}")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        item_id = request.get_json()
        try:
            return items[item_id["id"]]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        item_id = request.get_json()
        try:
            del items[item_id["id"]]
            return items, 201
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        try:
            if item_data["id"] in items:
                items[item_data["id"]] |= item_data
                return items
        except Exception as e:
            print("erro ", e)
            abort(404, message=f"item has a problem {e}")
