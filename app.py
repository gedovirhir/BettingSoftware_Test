from fastapi import FastAPI
from line_provider.models import Event

from typing import Dict

app = FastAPI()
events_storage: Dict[str, Event] = {
    
}