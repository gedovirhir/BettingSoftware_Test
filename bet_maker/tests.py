import httpx
import pytest
import pytest_asyncio
import time
import copy
from datetime import datetime

from typing import List, Union

from main import app
from config import LINE_PROVIDER_HOST

@pytest_asyncio.fixture()
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app, base_url=f"http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_get_events(client: httpx.AsyncClient):
    resp = await client.get('/events')
    
    assert resp.is_success
    assert resp.json()

@pytest_asyncio.fixture()
async def bets_scripts(client: httpx.AsyncClient):
    resp = await client.get('/events')
    events_ids = [(e['id'], True) for e in resp.json()] + [('kekshrek', False), (32123, False)]
    amounts = [('kekshrek', False), (12321, True), (232.123, True)]
    
    scripts = []
    for ev_id in events_ids:
        for amount in amounts:
            body = {
                'event_id': ev_id[0],
                'amount': amount[0]
            }
            pred_response = bool(ev_id[1] * amount[1])
            
            scripts.append((body, pred_response))
    
    return scripts
 
@pytest.mark.asyncio
async def test_post_bet(client: httpx.AsyncClient, bets_scripts):
    for bet_input, expected in bets_scripts:
        resp = await client.post('/bet', json=bet_input)
        
        assert resp.is_success == expected

@pytest.mark.asyncio
async def test_get_bets(client: httpx.AsyncClient):
    resp = await client.get('/events')
    events = resp.json()
    
    bets = [
        {
            'event_id': e['id'],
            'amount': 123
        } for e in events
    ]
    
    for b in bets:
        await client.post('/bet', json=b)
    
    resp = await client.get('/bets')
    bets = resp.json()
    
    for b in bets:
        assert b in bets
