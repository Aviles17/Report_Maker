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



def get_position_history_auto(client,defined_interval: str = "m"): # 'm' for montly, 'a' for all time
    # Convert both to Unix time
    if defined_interval == "m":
        start_time = int(int(time.time() *1000) - (30.4 * 24 * 60 * 60 * 1000))
    elif defined_interval == "a":
        timezone = pytz.timezone("Etc/GMT+5")
        date_origin = datetime(2024,7,20,0,0,0, tzinfo=timezone) # July 20 of 2024
        utc_date_origin = (date_origin.astimezone(pytz.utc).timestamp())*1000
        date = int(time.time() *1000) - (365 * 24 * 60 * 60 * 1000)
        if date < utc_date_origin: #If the requested date is before the products launch
            start_time = utc_date_origin 
        else:
            start_time = date  - (365 * 24 * 60 * 60 * 1000)

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

def get_position_history_manual(client,start_date: datetime, end_date: datetime):
    start_time = int(start_date.timestamp())*1000
    end_time = int(end_date.timestamp())*1000

    #Check if the start date is before the products launch
    date_origin = datetime(2024,7,20,0,0,0, tzinfo=pytz.timezone("Etc/GMT+5")) # July 20 of 2024
    utc_date_origin = (date_origin.astimezone(pytz.utc).timestamp())*1000
    if start_time < utc_date_origin:
        start_time = utc_date_origin
    
    concat_list = []
    #Get the first hsitory of 7 days
    try:
        while start_time <= end_time:
            res = client.get_closed_pnl(category="linear",endTime = end_time, limit=100)
            end_time = int(res["result"]["list"][-1]["createdTime"])
            concat_list.extend(res["result"]["list"])
        return concat_list
    except Exception as e:
        print(f"An exception occurred connecting to Bybit 'get_closed_pnl' endpoint: {e}")
        return []

def convert_order_to_register(orders:list, final_balance:float):
    ret = []
    for order in orders:
        ret.append({
            "Id": order["orderId"],
            "Fecha": datetime.fromtimestamp(int(order["createdTime"])/1000).strftime("%m/%d/%Y %H:%M:%S"),
            "Cantidad": order["qty"],
            "Profit": str(round(float(order["closedPnl"]),4)),
            "Aporte": str(round((float(order["closedPnl"])/final_balance)*100,4))
        })
    return ret


def extract_kpi(orders:list, initial_balance:float):
    ret = [initial_balance]
    profit = 0

    for order in orders:
        profit += float(order["closedPnl"])
    
    ret.append(profit + initial_balance)

    ret.append(profit)

    ret.append((profit/initial_balance)*100)

    #Convert all registers to formatted strings
    for i in range(len(ret)):
        if i != 3 and i != 2:
            ret[i] = f"{ret[i]:.2f} USDT"
        elif i == 3:
            ret[i] = f"{ret[i]:.2f}%"
        elif i == 2:
            if ret[i] < 0:
                ret[i] = f"- {ret[i]:.2f} USDT"
            else:
                ret[i] = f"+ {ret[i]:.2f} USDT"

    return ret

















if __name__ == '__main__':
    print('This script is not meant to be run directly. Exiting...')