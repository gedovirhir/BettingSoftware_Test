import uvicorn
from config import WEB_PORT, WEB_HOST

from app import *
from routers import *
from swagger import *

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=WEB_HOST,
        port=int(WEB_PORT)
    )