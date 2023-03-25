import httpx
import redis
import asyncio

from typing import List

from config import LINE_PROVIDER_HOST
from config import R_HOST, R_PORT, R_PASSWORD

from models import Bet

redis_c_pool = redis.ConnectionPool(
    host=R_HOST,
    port=R_PORT,
    password=R_PASSWORD,
    decode_responses=True
)

async def actual_events() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        events = await client.get(f"{LINE_PROVIDER_HOST}/actual_events")
        
        return events

async def get_event(event_id: str):
    async with httpx.AsyncClient() as client:
        event = await client.get(f"{LINE_PROVIDER_HOST}/event/{event_id}")
        
        return event

async def update_bets_states(bets: List[dict]) -> List[dict]:
    sem = asyncio.Semaphore(10)
    
    async def __get_info(bet: dict, sem: asyncio.Semaphore):
        async with sem:
            event = await get_event(bet['event_id'])
            event = event.json()
            
            bet.update({'state': event['state']})
    
    await asyncio.gather(*[__get_info(bet, sem) for bet in bets])
        

def redis_conn() -> redis.Redis:
    return redis.Redis(connection_pool=redis_c_pool)

async def redis_add_bet(bet: Bet):
    rs = redis_conn()
    
    id_ = str(bet.id)
    cont = bet.dict()
    
    add_to_set = rs.sadd('bet:bets_keys', id_)
    add_to_hash = rs.hset(f"bet:{id_}", mapping=cont)
    return add_to_set * add_to_hash

async def redis_get_all_bets() -> List[dict]:
    rs = redis_conn()
    
    bets_keys = rs.smembers('bet:bets_keys')
    bets = [rs.hgetall(f"bet:{key}") for key in bets_keys]
    
    return bets