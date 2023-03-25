import uvicorn
from config import WEB_HOST, WEB_PORT

from app import *
from routers import *
from swagger import *

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=WEB_HOST,
        port=int(WEB_PORT)
    )