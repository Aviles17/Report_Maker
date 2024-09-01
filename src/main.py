from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os
import pytz
from scripts.grafic_generator_script import create_pdf_report
from scripts.data_extract_functions import get_position_history_manual, convert_order_to_register, extract_kpi
from datetime import datetime

def create_bybit_client(Api_key:str = None, Api_secret:str = None):
    client = HTTP(testnet=False, api_key=Api_key, api_secret=Api_secret)
    return client




if __name__ == '__main__':
    load_dotenv()
    client = create_bybit_client(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    timezone = pytz.timezone("Etc/GMT+5")
    start_date = datetime(2024, 7, 25, 0, 0, tzinfo=timezone)
    end_date = datetime(2024, 8, 25, 0, 0, tzinfo=timezone)
    result = get_position_history_manual(client, start_date, end_date)
    kpis = extract_kpi(result, 8.36)
    registers = convert_order_to_register(result, float(kpis[1].split(" ")[0]))
    create_pdf_report("Prototipo_Reporte_Jul-Ago.pdf", "Administración", "229","Basic Supertrend", start_date, end_date, kpis, registers)
