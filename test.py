import time
import hmac
import hashlib
import requests
from api_data.api_data import bybit_api_keys, bybit_api_secret

recv_window = 5000
timestamp = str(int(time.time()*1000)) #отпечаток времени
url_wallet = "https://api.bybit.com/v5/account/wallet-balance"
data1 = {"accountType": "UNIFIED"}
def get_signature_wallet1(method, data, timestamp):
    param_str = f"{timestamp}{bybit_api_keys}{recv_window}"
    param_str += ujson.dumps(data) if method != 'get' else '&'.join([f'{k}={v}' for k, v in data.items()])
    return hmac.new(bytes(bybit_api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()

header_get_balance_bybit = {
    "X-BAPI-API-KEY": bybit_api_keys,
    "X-BAPI-TIMESTAMP": timestamp,
    "X-BAPI-RECV-WINDOW": str(recv_window)
}
header_get_balance_bybit["X-BAPI-SIGN"] = get_signature_wallet1('get',data1, timestamp)
wallet = requests.get(url=url_wallet, params=data1, headers=header_get_balance_bybit).json()
total_balance = wallet['result']['list'][0]['totalEquity']
coin = wallet['result']['list'][0]['coin'][0]['coin']
usd_value = wallet['result']['list'][0]['coin'][0]['usdValue']
dict_balance = {}
print(len(wallet['result']['list'][0]))
for i in range(len(wallet['result']['list'][0])):
    dict_balance[wallet['result']['list'][0]['coin'][i]['coin']] = wallet['result']['list'][0]['coin'][i]['usdValue']
print(dict_balance)

print(wallet)



