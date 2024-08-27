from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

def create_bybit_client(Api_key:str = None, Api_secret:str = None):
    client = HTTP(testnet=False, api_key=Api_key, api_secret=Api_secret)
    return client




if __name__ == '__main__':
    load_dotenv()
    client = create_bybit_client(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    