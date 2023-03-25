import time
from datetime import datetime

from fastapi import HTTPException

from typing import Optional, List

from app import app
from models import Event
from utils import update_event_storage, get_event, get_events

@app.post('/event', status_code=201)
async def api_post_event(event: Event):
    if await get_event(event.id):
        raise HTTPException(status_code=400, detail="Event already exists")
    try:
        await update_event_storage(event)
        return event
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@app.get('/event/{event_id}')
async def api_get_event(event_id: str):
    ev = await get_event(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail='Event not found')

    return ev
    
@app.put('/event/{event_id}')
async def api_put_event(event_id: str, event: Event):
    ev = await get_event(event_id)
    if not ev:
        raise HTTPException(status_code=400, detail='Event not found')

    update_content = event.dict(exclude_unset=True)
    update_content['id'] = event_id
    
    for p_name, p_value in update_content.items():
        setattr(ev, p_name, p_value)
    
    return ev
    
@app.get('/actual_events', response_model=List[Event])
async def api_get_actual_events(cur_time: Optional[datetime] = None):
    cur_time = (cur_time and cur_time.timestamp()) or time.time()
    events = await get_events(filter=lambda e: e.deadline and e.deadline > cur_time)
    return events


