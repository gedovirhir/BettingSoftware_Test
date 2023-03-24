from uuid import UUID, uuid4
from pydantic import BaseModel, validator
import enum

from typing import Optional, Union
from datetime import datetime
import time

class EventState(enum.Enum):
    NEW = 1
    FIN_WIN = 2
    FIN_LOSE = 3

class Event(BaseModel):
    id: Optional[UUID] = None
    coef: Optional[float] = None
    deadline: Union[float, datetime] = None
    state: Optional[EventState] = None
    
    @validator('id', pre=True, always=True)
    def create_id(cls, v):
        return v or uuid4()
    
    @validator('deadline', pre=True)
    def convert_datetime(cls, v):
        if isinstance(v, str):
            try:
                date_ = datetime.fromisoformat(v)
                return date_.timestamp()
            except:
                pass
        
        return v
    
    
