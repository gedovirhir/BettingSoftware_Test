from typing import Callable, Optional, List, Union

from app import events_storage
from models import Event

async def get_events(filter: Callable[[Event], bool] = lambda _: True) -> List[Event]:
    return [val for val in events_storage.values() if filter(val)]

async def update_event_storage(event: Event):
    events_storage.update(
        {event.id: event}
    )

async def get_event(events_id: Union[str, List[str]]) -> Optional[Event]:
    if not isinstance(events_id, list):
        events_id = [events_id]
    
    return [events_storage.get(id_) for id_ in events_id]