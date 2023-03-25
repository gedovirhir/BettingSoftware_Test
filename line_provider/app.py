from fastapi import FastAPI
import time

from typing import Dict

from models import Event, EventState

app = FastAPI()
events_storage: Dict[str, Event] = {
    '1': Event(
        id='1',
        coef=1.32,
        deadline="2023-03-28",
        state=EventState.NEW
    ),
    '2': Event(
        id='2',
        coef=1.8,
        deadline=time.time() + 6000,
        state=EventState.NEW
    ),
    '3': Event(
        id='3',
        coef=1.83,
        deadline=time.time() + 6000,
        state=EventState.NEW
    ),
}