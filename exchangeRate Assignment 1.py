# exchange.py
# FINE3300 - Assignment 1 (Part 2)
# Author: Marek Satov

from pathlib import Path
#Bring in the ExchangeRates class from exchangeRate.py

# Execution starts here
if __name__ == "__main__": #
    # Full path to your CSV file
    CSV_PATH = Path(__file__).with_name("BankOfCanadaExchangeRates.csv")
#    Builds path that sits next to exchnange rates and finds the CVS file

# file: exchangeRate.py
import csv
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation #round to nearest cent


def _load_usd_cad_rate(path: Path = CSV_PATH) -> Decimal:
    """Read the last numeric value from the 'USD/CAD' column (CAD per 1 USD)."""
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)  # assumes a header row exists
        try:
            col = header.index("USD/CAD")  # update if your header differs
        except ValueError:
            raise ValueError("CSV must have a 'USD/CAD' column.") #if no USD/CAD column, raise error   
        last = None #initialize last to None
        for row in reader: #iterate through each row in the CSV
            if col < len(row): #check if the column index is within the row length
                cell = row[col].strip().replace(",", "") #remove whitespace and commas
                if cell: #if cell is not empty
                    try: #try to convert cell to Decimal
                        last = Decimal(cell) #update last with the current cell value
                    except InvalidOperation: #if conversion fails, ignore and continue
                        pass 
        if last is None: #if no numeric value was found, raise error
            raise ValueError("No numeric USD/CAD values found.") 
        return last #return the last found value

def convert_usd_to_cad(amount) -> Decimal: #define function to convert USD to CAD
    """USD -> CAD using latest USD/CAD; rounds to cents.""" 
    rate = _load_usd_cad_rate() #load the latest USD/CAD rate
    return (Decimal(str(amount)) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #convert amount to Decimal, multiply by rate, round to nearest cent

def convert_cad_to_usd(amount) -> Decimal: #define function to convert CAD to USD
    """CAD -> USD using latest USD/CAD; rounds to cents.""" 
    rate = _load_usd_cad_rate() #load the latest USD/CAD rate
    if rate == 0: 
        raise ZeroDivisionError("USD/CAD rate is zero.") #prevent division by zero
    return (Decimal(str(amount)) / rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) #convert amount to Decimal, divide by rate, round to nearest cent

if __name__ == "__main__": 
    print("Using CSV:", CSV_PATH.resolve()) #print the full path to the CSV file
    amt = input("Amount: ").strip().replace("$", "").replace(",", "") #get user input for amount, remove $ and commas
    frm = input("From (USD/CAD): ").strip().upper() #get user input for currency type, convert to uppercase
    if frm == "USD": #if currency type is USD
        print(f"CAD {convert_usd_to_cad(amt):,.2f}") #print converted amount in CAD format
    elif frm == "CAD": #if currency type is CAD
        print(f"USD {convert_cad_to_usd(amt):,.2f}") #print converted amount in USD format
    else:
        print("Use USD or CAD.") #print error message for invalid currency type









