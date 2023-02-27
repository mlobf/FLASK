from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)


# Store Get All Stores
@app.get("/store")
def get_stores():
    return stores, 201


# Store Get Store by Id
@app.get("/store/<string:store_id>")
def get_store(store_id):
    store_id = request.get_json()
    try:
        return stores[store_id["id"]], 201
    except KeyError:
        abort(404, message="Store not found.")


# Store Put Store by Id
@app.put("/store/<string:store_id>")
def put_store(store_id):
    store_id = request.get_json()
    store = stores[store_id["id"]]
    return null
    """ 
    try:
        return stores[store_id["id"]], 201
    except KeyError:
        abort(404, message="Store not found.")
    """


# Store Delete Store by Id
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    store_id = request.get_json()
    try:
        del stores[store_id["id"]]
        return stores, 201
    except KeyError:
        abort(404, message="Store not found.")


# Store Create Store
@app.post("/store")
def create_store():
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


# Item get All Items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


# Item get Item by ID
@app.get("/item/<string:item_id>")
def get_item(item_id):
    item_id = request.get_json()
    try:
        return items[item_id["id"]]
    except KeyError:
        abort(404, message="Item not found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    item_id = request.get_json()
    try:
        del items[item_id["id"]]
        return items, 201
    except KeyError:
        abort(404, message="Item not found.")


# Item Create Item
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            404,
            message="Bad request. Ensure 'price','store_id','name' are included in the JSON payload",
        )

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


if __name__ == "__main__":
    app.run(debug=True)
