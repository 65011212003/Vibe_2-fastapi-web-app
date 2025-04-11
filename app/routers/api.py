from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.item import Item, ItemCreate
from app.services.item_service import ItemService
from app.models.auth import UserResponse
from app.routers.auth import get_current_user_from_token

router = APIRouter(tags=["api"])
item_service = ItemService()

@router.get("/items", response_model=List[Item])
async def get_items():
    """Get all items."""
    return item_service.get_all_items()

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    """Get a specific item by ID."""
    item = item_service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=Item, status_code=201)
async def create_item(
    item: ItemCreate, 
    current_user: UserResponse = Depends(get_current_user_from_token)
):
    """Create a new item. Requires authentication."""
    # Convert ItemCreate to Item with a dummy ID (will be replaced by the service)
    new_item = Item(id="temp", **item.dict())
    return item_service.create_item(new_item)

@router.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: str, 
    item: ItemCreate,
    current_user: UserResponse = Depends(get_current_user_from_token)
):
    """Update an existing item. Requires authentication."""
    # Convert ItemCreate to Item with the existing ID
    updated_item = Item(id=item_id, **item.dict())
    result = item_service.update_item(item_id, updated_item)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@router.delete("/items/{item_id}", response_model=Dict[str, bool])
async def delete_item(
    item_id: str,
    current_user: UserResponse = Depends(get_current_user_from_token)
):
    """Delete an item. Requires authentication."""
    success = item_service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True}

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 