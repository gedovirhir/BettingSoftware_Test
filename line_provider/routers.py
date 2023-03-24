from fastapi import HTTPException
from fastapi.responses import JSONResponse

from typing import Optional

from app import app
from .models import Event
from .utils import update_event_storage, get_event

@app.post('/event')
async def post_event(event: Event):
    if get_event(event.id):
        return HTTPException(status_code=400, detail="Event already exists")
    try:
        update_event_storage(event)
        return JSONResponse(status_code=200, content={'message': 'Event added'})
    except Exception as ex:
        return HTTPException(status_code=400, detail=str(ex))

@app.get('/event/{event_id}')
async def get_event(event_id: str):
    ev = get_event(event_id)
    if not ev:
        return HTTPException(status_code=400, detail='Event not found')

    return ev
    
@app.put('/event/{event_id}')
async def put_event(event_id: str, event: Event):
    ev = get_event(event_id)
    if not ev:
        return HTTPException(status_code=400, detail='Event not found')

    update_content = event.dict(exclude_unset=True)
    update_content['id'] = event_id
    
    for p_name, p_value in update_content.items():
        setattr(ev, p_name, p_value)
    
    return JSONResponse(status_code=200, content={'message': 'Event updated'})
    
    
    


