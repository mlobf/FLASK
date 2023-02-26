from flask import Flask, request
from db import stores, items
import uuid

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores.append(new_store)
    stores[store_id] = new_store
    return new_store, 201


# Este aqui
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


# get item in store
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
