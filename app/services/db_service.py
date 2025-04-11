from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import os
import json
from typing import Dict, List, Optional, Any, Union
import uuid

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

class DatabaseService:
    """Database service using TinyDB."""
    
    def __init__(self):
        # Initialize TinyDB with caching for better performance
        try:
            self.db = TinyDB('data/db.json', storage=CachingMiddleware(JSONStorage))
            print(f"Database initialized at {os.path.abspath('data/db.json')}")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise
        
        # Create tables
        self.users = self.db.table('users')
        self.items = self.db.table('items')
        
        # Query constructor
        self.query = Query()
        
        # Print tables info
        print(f"Database tables: {self.db.tables()}")
        print(f"Users count: {len(self.users)}")
        print(f"Items count: {len(self.items)}")
    
    def find_one(self, table_name: str, query: Dict[str, Any]) -> Optional[Dict]:
        """Find a single document in the specified table."""
        try:
            print(f"Finding one in {table_name} with query: {query}")
            table = getattr(self, table_name)
            q = self.query
            
            # Build the query dynamically
            query_conditions = None
            for key, value in query.items():
                condition = (q[key] == value)
                if query_conditions is None:
                    query_conditions = condition
                else:
                    query_conditions = query_conditions & condition
            
            if query_conditions is None:
                return None
                
            result = table.get(query_conditions)
            print(f"Found result: {result}")
            return result
        except Exception as e:
            print(f"Error in find_one: {str(e)}")
            return None
    
    def find_all(self, table_name: str, query: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Find all documents in the specified table that match the query."""
        try:
            print(f"Finding all in {table_name} with query: {query}")
            table = getattr(self, table_name)
            
            if query is None:
                results = table.all()
                print(f"Found {len(results)} results")
                return results
            
            q = self.query
            
            # Build the query dynamically
            query_conditions = None
            for key, value in query.items():
                condition = (q[key] == value)
                if query_conditions is None:
                    query_conditions = condition
                else:
                    query_conditions = query_conditions & condition
            
            if query_conditions is None:
                results = table.all()
                print(f"Found {len(results)} results")
                return results
                
            results = table.search(query_conditions)
            print(f"Found {len(results)} results")
            return results
        except Exception as e:
            print(f"Error in find_all: {str(e)}")
            return []
    
    def insert(self, table_name: str, document: Dict) -> int:
        """Insert a document into the specified table."""
        try:
            print(f"Inserting into {table_name}: {document}")
            table = getattr(self, table_name)
            
            # Ensure document has an ID
            if 'id' not in document:
                document['id'] = str(uuid.uuid4())
                
            doc_id = table.insert(document)
            # Flush database to disk
            self.db.storage.flush()
            print(f"Inserted document with ID: {doc_id}")
            
            # Verify the document was inserted
            table_contents = table.all()
            print(f"Table {table_name} now has {len(table_contents)} documents")
            
            return doc_id
        except Exception as e:
            print(f"Error in insert: {str(e)}")
            return -1
    
    def update(self, table_name: str, query: Dict[str, Any], update_data: Dict) -> List[int]:
        """Update documents in the specified table that match the query."""
        try:
            print(f"Updating in {table_name} with query {query}: {update_data}")
            table = getattr(self, table_name)
            q = self.query
            
            # Build the query dynamically
            query_conditions = None
            for key, value in query.items():
                condition = (q[key] == value)
                if query_conditions is None:
                    query_conditions = condition
                else:
                    query_conditions = query_conditions & condition
            
            if query_conditions is None:
                print("No query conditions provided")
                return []
                
            updated_ids = table.update(update_data, query_conditions)
            # Flush database to disk
            self.db.storage.flush()
            print(f"Updated document IDs: {updated_ids}")
            return updated_ids
        except Exception as e:
            print(f"Error in update: {str(e)}")
            return []
    
    def delete(self, table_name: str, query: Dict[str, Any]) -> List[int]:
        """Delete documents in the specified table that match the query."""
        try:
            print(f"Deleting from {table_name} with query: {query}")
            table = getattr(self, table_name)
            q = self.query
            
            # Build the query dynamically
            query_conditions = None
            for key, value in query.items():
                condition = (q[key] == value)
                if query_conditions is None:
                    query_conditions = condition
                else:
                    query_conditions = query_conditions & condition
            
            if query_conditions is None:
                print("No query conditions provided")
                return []
                
            deleted_ids = table.remove(query_conditions)
            # Flush database to disk
            self.db.storage.flush()
            print(f"Deleted document IDs: {deleted_ids}")
            return deleted_ids
        except Exception as e:
            print(f"Error in delete: {str(e)}")
            return []
    
    def close(self):
        """Close the database connection."""
        try:
            self.db.storage.flush()
            self.db.close()
            print("Database connection closed")
        except Exception as e:
            print(f"Error closing database: {str(e)}") 