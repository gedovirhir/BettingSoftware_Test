from fastapi import HTTPException

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
    
    return events.json()

@app.post('/bet')
async def api_post_bet(bet: Bet):
    resp = await get_event(bet.event_id)
    event = resp.json()
    
    if not resp.is_success:
        raise HTTPException(resp.status_code, detail=event.get('detail'))
    
    await redis_add_bet(bet)
    
    return bet

@app.get('/bets')
async def api_get_bets():
    bets = await redis_get_all_bets()
    
    await update_bets_states(bets)
        
    return bets
    
    
    
        