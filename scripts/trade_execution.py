from binance.client import Client
from binance.enums import *

def execute_trade(signal, quantity):
    client = Client(api_key, api_secret)
    
    if signal == "Buy":
        order = client.create_order(
            symbol='BTCUSDT',
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
    elif signal == "Sell":
        order = client.create_order(
            symbol='BTCUSDT',
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
    return order 