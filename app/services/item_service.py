from typing import List, Optional, Dict
from app.models.item import Item
from app.services.db_service import DatabaseService

class ItemService:
    """Service for handling item-related business logic."""
    
    def __init__(self):
        # Initialize database service
        self.db_service = DatabaseService()
        
        # Seed some initial items if none exist
        if not self.db_service.find_all('items'):
            self._seed_initial_items()
    
    def _seed_initial_items(self):
        """Seed some initial items for demonstration."""
        initial_items = [
            {"id": "1", "name": "Item 1", "description": "This is item 1"},
            {"id": "2", "name": "Item 2", "description": "This is item 2"},
        ]
        
        for item in initial_items:
            self.db_service.insert('items', item)
    
    def get_all_items(self) -> List[Item]:
        """Get all items."""
        items = self.db_service.find_all('items')
        return [Item(**item) for item in items]
    
    def get_item_by_id(self, item_id: str) -> Optional[Item]:
        """Get an item by its ID."""
        item = self.db_service.find_one('items', {'id': item_id})
        if item:
            return Item(**item)
        return None
    
    def create_item(self, item: Item) -> Item:
        """Create a new item."""
        # Convert Item model to dict
        item_dict = item.dict()
        
        # Insert into database
        self.db_service.insert('items', item_dict)
        
        return item
    
    def update_item(self, item_id: str, updated_item: Item) -> Optional[Item]:
        """Update an existing item."""
        # Check if item exists
        existing_item = self.db_service.find_one('items', {'id': item_id})
        if not existing_item:
            return None
            
        # Convert Item model to dict and update
        updated_item_dict = updated_item.dict()
        self.db_service.update('items', {'id': item_id}, updated_item_dict)
        
        return updated_item
    
    def delete_item(self, item_id: str) -> bool:
        """Delete an item by its ID."""
        result = self.db_service.delete('items', {'id': item_id})
        return len(result) > 0 