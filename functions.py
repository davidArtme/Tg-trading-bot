import hashlib
import hmac
import json
import time
import requests
from api_data.api_data import binance_testnet_api_secret, binance_testnet_api_keys, url_place_order, bybit_api_keys, bybit_api_secret
import decimal

recv_window = 5000
params_balance = {
    "accountType": "UNIFIED"
}

def get_timestamp():
    return str(int(time.time()*1000))

# get price ----------------------------------------
def get_price(symbol):
    url_get_price = "https://api.bybit.com/v5/market/tickers"
    params_get_price = {
        'category': 'spot',
        "symbol": symbol,
        "limit": 10
    }
    return requests.get(url=url_get_price, params=params_get_price).json()['result']['list'][0]['lastPrice']
#------------------------------------------------
# signature binance
def gen_signature_binance(params):
    param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature = hmac.new(bytes(binance_testnet_api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature

header_binance = {
    "X-MBX-APIKEY": binance_testnet_api_keys
}
#-----------
# wallet balance
def get_signature_wallet1(method, data, timestamp):
    param_str = f"{timestamp}{bybit_api_keys}{recv_window}"
    param_str += ujson.dumps(data) if method != 'get' else '&'.join([f'{k}={v}' for k, v in data.items()])
    return hmac.new(bytes(bybit_api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
def get_wallet_balance():
    url_wallet = "https://api.bybit.com/v5/account/wallet-balance"
    data1 = {"accountType": "UNIFIED"}
    timestamp = get_timestamp()
    header_get_balance_bybit = {
        "X-BAPI-API-KEY": bybit_api_keys,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": str(recv_window)
    }
    header_get_balance_bybit["X-BAPI-SIGN"] = get_signature_wallet1('get', data1, timestamp)
    wallet = requests.get(url=url_wallet, params=data1, headers=header_get_balance_bybit).json()
    dict_balance = {}
    numberOfCoins = len(wallet['result']['list'][0]['coin'])
    for i in range(numberOfCoins):
        dict_balance[wallet['result']['list'][0]['coin'][i]['coin']] = wallet['result']['list'][0]['coin'][i]['usdValue']
    return dict_balance
# market order ---------------------------------------
def get_private_market_order_binance(symbol, side, quantity):
    params_market = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
    }
    params_market['signature'] = gen_signature_binance(params_market)
    new_market_order_binance = requests.post(url=url_place_order, params=params_market, headers=header_binance).json()  # размещение новой заявки
    return new_market_order_binance
# ------------------------------------------------------
# limit order -------------------------------------------
def get_private_limit_order_binance(symbol, side, quantity, price):
    params_limit = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": round(float(quantity),2),
        "price": int(price),
        "timestamp": int(time.time()*1000)
    }
    params_limit['signature'] = gen_signature_binance(params_limit)
    new_limit_order_binance = requests.post(url=url_place_order, params=params_limit, headers=header_binance).json()  # размещение новой заявки
    return new_limit_order_binance
#-------------------------------------------------------
# рыночный ордер на bybit
def get_market_order_bybit(category, symbol, side, quantity):
    timestamp = str(int(time.time() * 1000))  # отпечаток времени
    url_order = "https://api.bybit.com/v5/order/create"
    def gen_signature(params, timestamp):
        param_str = timestamp + bybit_api_keys + '5000' + json.dumps(params)
        signature = hmac.new(bytes(bybit_api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
        return signature

    header = {
        "X-BAPI-API-KEY": bybit_api_keys,
        "X-BAPI-TIMESTAMP": str(int(time.time() * 1000)),
        "X-BAPI-RECV-WINDOW": "5000"
    }

    params = {
        "category": category,
        "symbol": symbol,
        "side": side.capitalize(),
        "orderType": "MARKET".capitalize(),
        "qty": str(quantity),
    }

    header["X-BAPI-SIGN"] = gen_signature(params, timestamp)
    new_order = requests.post(url=url_order, headers=header, data=json.dumps(params)).json()
    return new_order

# лимитный ордер на bybit
def get_limit_order_bybit(category, symbol, side, price, quantity):
    timestamp = str(int(time.time() * 1000))  # отпечаток времени
    url_order = "https://api.bybit.com/v5/order/create"

    def gen_signature(params, timestamp):
        param_str = timestamp + bybit_api_keys + '5000' + json.dumps(params)
        signature = hmac.new(bytes(bybit_api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
        return signature

    header = {
        "X-BAPI-API-KEY": bybit_api_keys,
        "X-BAPI-TIMESTAMP": str(int(time.time() * 1000)),
        "X-BAPI-RECV-WINDOW": "5000"
    }
    params = {
        "category": category,
        "symbol": symbol,
        "side": side.capitalize(),
        "orderType": "LIMIT".capitalize(),
        "qty": str(quantity),
        "price": str(price),
    }

    header["X-BAPI-SIGN"] = gen_signature(params, timestamp)
    new_order = requests.post(url=url_order, headers=header, data=json.dumps(params)).json()
    return new_order

# newOrder = get_limit_order_bybit('spot', 'TONUSDT', 'BUY', 5, 1)
# print(newOrder)
# print(newOrder['result']['orderId'])