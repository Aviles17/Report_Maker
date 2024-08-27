import time
import pytz
from datetime import datetime

'''
###################################################################################
[Proposito]: Funcion para limpiar la entrada de la informacion del cliente y proveer la informacion de cuenta
[Parametros]: symbol(Stock por la cual se quiere filtrar, Ejemplo : USDT), cliente (Informacion del cliente de bybit)
[Retorna]: Retorna valor 'float' del balance de la moneda asignada por parametro en la cuenta
###################################################################################
'''
def Get_Balance(client,symbol: str = "USDT"):
    filt_Balance = 0
    while(filt_Balance == 0):
        balance = client.get_coin_balance(accountType="CONTRACT", coin=symbol)
        if balance is not None:
            filt_Balance = balance["result"]["balance"]["walletBalance"]
        else:
            filt_Balance = 0
            
    return filt_Balance



def get_position_history(client,defined_interval: str = "m"): # 'm' for montly, 'a' for all time
    # Convert both to Unix time
    if defined_interval == "m":
        start_time = int(time.time() *1000) - (31 * 24 * 60 * 60 * 1000)
    if defined_interval == "a":
        timezone = pytz.timezone("Etc/GMT+5")
        date_origin = datetime(2024,7,20,0,0,0, tzinfo=timezone) # July 20 of 2024
        utc_date_origin = (date_origin.astimezone(pytz.utc).timestamp())*1000
        date = int(time.time() *1000) - (365 * 24 * 60 * 60 * 1000)
        if utc_date_origin < date:
            start_time = date
        else:
            start_time = utc_date_origin

    concat_list = []
    #Get the first hsitory of 7 days
    res = client.get_closed_pnl(category="linear", limit=100)
    concat_list.extend(res["result"]["list"])
    endtime = int(res["result"]["list"][-1]["createdTime"])
    try:
        while start_time <= endtime:
            res = client.get_closed_pnl(category="linear",endTime = endtime, limit=100)
            endtime = int(res["result"]["list"][-1]["createdTime"])
            concat_list.extend(res["result"]["list"])
        return concat_list
    except Exception as e:
        print(f"An exception occurred connecting to Bybit 'get_closed_pnl' endpoint: {e}")
        return []


def extract_kpi(orders:list):
    pass # TO DO
















if __name__ == '__main__':
    print('This script is not meant to be run directly. Exiting...')