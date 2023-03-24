from pydantic import BaseModel, Field
import enum
from uuid import UUID, uuid4

from typing import Optional, Union

class BetState(enum.Enum):
    NEW = 1
    FIN_WIN = 2
    FIN_LOSE = 3

class Bet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    event_id: str
    amount: Union[int, float]