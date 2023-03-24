from uuid import uuid4
from pydantic import BaseModel, validator, Field
import enum
from decimal import Decimal

from typing import Optional, Union
from datetime import datetime

class EventState(enum.Enum):
    NEW = 1
    FIN_WIN = 2
    FIN_LOSE = 3

class Event(BaseModel):
    id: Optional[str] = None
    coef: Optional[Decimal] = Field(decimal_places=2, gt=0)
    deadline: Optional[Union[float, datetime]] = None
    state: Optional[EventState] = None
    
    @validator('id', pre=True, always=True)
    def create_id(cls, v):
        return v or str(uuid4())
    
    @validator('deadline', pre=True)
    def convert_datetime(cls, v):
        if isinstance(v, str):
            try:
                date_ = datetime.fromisoformat(v)
                return date_.timestamp()
            except:
                pass
        
        return v
    
    
