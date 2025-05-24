from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # Helps to structure your data and also provide additional validation

app = FastAPI()


class Item(BaseModel):
    text: str = None
    is_done: bool = False


items = []

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items/")
def create_item(item: Item):
    items.append(item)
    return items


@app.get("/items/{item_id}", response_model=list[Item])
def list_item(limit: int = 10):
    return items[0: limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.put("/Items/{item_id}")
def update_item(item_id: int, item: Item):
    if 0 <= item_id < len(items):
        items[item_id] = item
        return {"message": f"{item_id} successfully updated"}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if 0 <= item_id < len(items):
        deleted = items.pop(item_id)
        return {"message": f"item {item_id} successfully deleted"}
    raise HTTPException(status_code=404, detail=f"Items {item_id} not found")
