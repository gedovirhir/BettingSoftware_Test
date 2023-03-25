import httpx
import pytest
import pytest_asyncio
import time
import copy
from datetime import datetime

from typing import List, Union

from main import app

def to_datetime(d_object: Union[str, float]):
    return datetime.fromtimestamp(d_object)\
           if isinstance(d_object, float)\
           else datetime.fromisoformat(d_object)

@pytest_asyncio.fixture()
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app, base_url=f"http://testserver") as client:
        yield client

@pytest_asyncio.fixture()
async def default_events(client: httpx.AsyncClient) -> List[dict]:
    events = [
        {'coef': 1.1, 'deadline': '2022-03-03', 'state': 1},
        {'coef': 11.1, 'deadline': time.time() + 6000, 'state': 2},
        {'coef': 0.8, 'deadline': '2021-06-12', 'state': 3},
        {'deadline': '2022-06-12', 'state': 3},
        {'state': 3},
        {}
    ]
    
    for e in events:
        resp = await client.post('/event', json=e)
        e.update(resp.json())
        
    return events

@pytest_asyncio.fixture()
async def default_event(client: httpx.AsyncClient) -> List[dict]:
    event = {'coef': 1.1, 'deadline': '2023-03-03', 'state': 1}
    
    resp = await client.post('/event', json=event)
    event.update(resp.json())
    
    return event

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'name, value, success',
    [   
        ("coef", 1.32, True),
        ("coef", -1, False),
        ("coef", 0, False),
        ("coef", '1.32', True),
        ("coef", 1.3232, False),
     
        ("deadline", "2023-04-04 23:20:20", True),
        ("deadline", "2023-04-04", True),
        ("deadline", "04-04-2023 23:20:20", False),
        ("deadline", time.time() + 6000, True),
        ("deadline", int(time.time()) + 6000, True),
        ("deadline", -int(time.time()), False),

        ("state", 1, True),
        ("state", 2, True),
        ("state", 3, True),
        ("state", 4, False),
        ("state", -1, False),
    ]
)
async def test_post_event(client: httpx.AsyncClient, name, value, success):
    resp = await client.post('/event', json={name: value})
    assert resp.is_success == success
    
    if success:
        assert resp.status_code == 201
        
@pytest.mark.asyncio
async def test_get_event(client: httpx.AsyncClient, default_events):
    for e in default_events:
        resp = await client.get(f"/event/{e['id']}")
        e_get = resp.json()
        assert e_get == e

@pytest.mark.asyncio
async def test_get_actual_events(client: httpx.AsyncClient, default_events):
    cur_time = time.time()
    resp = await client.get(f'/actual_events?cur_time={cur_time}')
    
    assert resp.is_success
    
    resp_events = resp.json()
    
    for e in default_events:
        e_deadline = e.get('deadline')
        if e_deadline:
            e_deadline = to_datetime(e_deadline).timestamp()
        
        if e_deadline and e_deadline > cur_time:
            assert e in resp_events
        else:
            assert e not in resp_events

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'new_event, success',
    [
        ({'coef': 1.1, 'deadline': '2022-03-03', 'state': 1}, True),
        ({'coef': None, 'deadline': None, 'state': None}, True),
        ({'coef': -1.1}, False),
        ({}, True),
    ]
)
async def test_put_event(client: httpx.AsyncClient, default_event, new_event, success):
    updated_event = copy.copy(default_event)
    updated_event.update(new_event)
    
    if updated_event.get('deadline'):
        updated_event['deadline'] = to_datetime(updated_event['deadline']).timestamp()
    
    resp = await client.put(f"/event/{default_event['id']}", json=new_event)
    
    assert resp.is_success == success
    if success:
        assert updated_event == resp.json()
        
    