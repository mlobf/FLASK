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
        items = ItemModel.query.all()
        return items

    # Item Create Item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the item.")

        return item, 201


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = StoreModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Store deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item
