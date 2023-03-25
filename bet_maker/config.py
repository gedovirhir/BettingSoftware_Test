
import os

LINE_PROVIDER_HOST=f"http://{os.getenv('LINE_PROVIDER_HOST')}"

R_HOST = os.getenv('REDIS_HOST')
R_PORT = os.getenv('REDIS_PORT')
R_PASSWORD = ''

WEB_PORT = os.getenv('BET_MAKER_PORT')
WEB_HOST = '0.0.0.0'