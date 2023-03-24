from line_provider.models import Event

from typing import Callable, Optional, List

from app import events_storage

def get_events(filter: Callable = lambda _: True) -> List[Event]:
    return [val for val in events_storage.values() if filter(val)]

def update_event_storage(event: Event):
    events_storage.update(
        {event.id: event}
    )

def get_event(event_id: str) -> Optional[Event]:
    return events_storage.get(event_id)