import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_sqlalchemy import query
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
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Delete Store is not implementing Yet")

    @blp.arguments(StoreUpdateSchema)
    def put(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Updating a Store is not implementing Yet")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

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
