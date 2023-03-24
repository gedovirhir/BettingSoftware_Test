import httpx

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app import app

from models import Bet
from utils import (actual_events, 
                   get_event,
                   update_bets_states, 
                   redis_add_bet, 
                   redis_get_all_bets)

@app.get('/events')
async def api_get_events():
    events = await actual_events()
    
    return JSONResponse(status_code=200, content=events.json())

@app.post('/bet')
async def api_post_bet(bet: Bet):
    event = await get_event(bet.event_id)
    content = event.json()
    
    if not event.is_success:
        raise HTTPException(event.status_code, detail=content.get('detail'))
    
    await redis_add_bet(bet)
    
    return bet

@app.get('/bets')
async def api_get_bets():
    bets = await redis_get_all_bets()
    
    await update_bets_states(bets)
        
    return bets
    
    
    
        