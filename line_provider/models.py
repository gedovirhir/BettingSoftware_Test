from uuid import uuid4
from pydantic import BaseModel, validator, Field
import enum
from decimal import Decimal
from datetime import datetime

from typing import Optional, Union

class EventState(enum.Enum):
    NEW = 1
    FIN_WIN = 2
    FIN_LOSE = 3

class Event(BaseModel):
    id: Optional[str] = None
    coef: Optional[Decimal] = Field(decimal_places=2, gt=0)
    deadline: Optional[Union[float, str]] = None
    state: Optional[EventState] = None
    
    @validator('id', pre=True, always=True)
    def create_id(cls, v):
        return v or str(uuid4())
    
    @validator('deadline')
    def convert_datetime(cls, v):
        try:
            if isinstance(v, str):
                v = datetime.fromisoformat(v).timestamp()
            elif isinstance(v, float):
                v = datetime.fromtimestamp(v).timestamp()
            
            return v
        except Exception as ex:
            raise ValueError('Not in timestamp or datetime format')
    
    
