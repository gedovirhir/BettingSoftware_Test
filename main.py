import uvicorn

from app import *
from line_provider.routers import *

if __name__ == "__main__":
    uvicorn.run(
        app,
        host='localhost',
        port=8080
    )