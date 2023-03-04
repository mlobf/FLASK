import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import query
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from models.item import ItemModel

""" 
A Blueprint is used to divided bussiness logic in
multiple segments.
"""

blp = Blueprint("items", __name__, description="Operations on items")


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
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()

            return new_item, 201
        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the item.")

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
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Delete Item is not implementing Yet")

    def put(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating a Item is not implementing Yet")
