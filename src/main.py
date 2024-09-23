from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os
import pytz
from scripts.grafic_generator_script import create_pdf_report
from scripts.data_extract_functions import get_position_history_manual, convert_order_to_register, extract_kpi
from datetime import datetime, timedelta
import time
def create_bybit_client(Api_key:str = None, Api_secret:str = None):
    client = HTTP(testnet=False, api_key=Api_key, api_secret=Api_secret)
    return client

def cmd_interactive_menu():
    print("Bienvenido al sistema de reportes de S&S Investments")
    file_name = input("Ingrese el nombre del archivo a crear, terminado con la extensión .pdf: ")
    user_name = input("Ingrese el nombre del titlar de la cuenta a la cual se le realiza el reporte: ")
    account_number = input("Ingrese los ultimos 3 digitos del número de cuenta a la cual se le realiza el reporte: ")
    strategy = input("Ingrese la estrategia de trading utilizada en el periodo reportado: ")
    option = input("¿Desea especificar el periodo del reporte o seguir con la opción de un mes (s/n): ")
    initial_value = input("Ingrese el saldo inicial de la cuenta: ")
    if option.lower() == "s":
        start_date = input("Ingrese la fecha de inicio del reporte en formato dd/mm/yyyy: ")
        end_date = input("Ingrese la fecha de fin del reporte en formato dd/mm/yyyy: ")
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y")
        return file_name, user_name, account_number, strategy, start_date, end_date, initial_value
    else:
        timezone = pytz.timezone("Etc/GMT+5")
        start_date = datetime.now(tz=timezone) - timedelta(days=31)
        end_date = datetime.now(tz=timezone)
    
    

    return file_name, user_name, account_number, strategy, start_date, end_date, initial_value




if __name__ == '__main__':
    file_name, user_name, account_number, strategy, start_date, end_date, initial_value = cmd_interactive_menu() # Llamado a la función que solicita los datos al usuario
    load_dotenv()
    client = create_bybit_client(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    result = get_position_history_manual(client,  start_date, end_date)
    kpis = extract_kpi(result, float(initial_value))
    registers = convert_order_to_register(result, float(kpis[1].split(" ")[0]))
    create_pdf_report(file_name, user_name, account_number,strategy, start_date, end_date, kpis, registers)
