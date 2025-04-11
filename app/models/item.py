from pydantic import BaseModel
from typing import Optional

# Item model
class Item(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

# Item creation model (without ID)
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None 