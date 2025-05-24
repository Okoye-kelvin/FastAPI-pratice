from fastapi import FastAPI

app = FastAPI()


@app.post("/items/")  # create or add item
def create_item(name: str, price: float):
    return {"name": name, "price": price}


@app.put("/items/{item_id}")  # update a table of items
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}


@app.delete("/items/{item_id}")  # delete an item from the table
def delete_item(item_id: int):
    return {"message": f"item {item_id} successfully deleted"}


@app.get("/item/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
