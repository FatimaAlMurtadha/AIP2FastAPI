from fastapi import FastAPI
"""
item_router = APIRoutes(prefix="api/v1/items", tags=["items"])

# Mock data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

# Check the program for the first time
@item_router.get("/health") # decorator
def health_check():
    return {"Status": "OK"}

# Get all items
@item_router.get("/items")
def get_items():
    for item in items:
        item["name"] = item["name"].upper()
    return items

# Get item by ID
@item_router.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item finns inte"}

# Get items with query parameters
@item_router.get("/items")
def get_items_query(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Create a new item
@item_router.post("/items")
def create_item(item: dict):
    items.append(item)
    return item

# Update an item
@item_router.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    for i in range(len(items)): # loop through the items list using index
        if items[i]["id"] == item_id:
            items[i] = item
            return item
    return {"error": "Item finns inte"}

# Delete an item
@item_router.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i in range(len(items)):
        if items[i]["id"] == item_id:
            del items[i]
            return {"message": "Item deleted"}
    return {"error": "Item finns inte"}

"""