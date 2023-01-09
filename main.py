import json
import requests
import colorama
import datetime
import time
import csv
import os
t = datetime.datetime.now()
today = t.strftime("%d_%m_%Y")

try: 
    if os.path.exists(f"{today}_data.csv"):
        with open(f"{today}_data.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                ("pair", "from", "to", "chang", "time")
            )
    else:
        with open(f"{today}_data.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                ("pair", "from", "to", "chang", "time")
            )
except Exception as ex:
    print(f"{ex}")



def csv_writer(pr, frm, to, chng, tm):
    with open(f"{today}_data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                pr,
                frm,
                to,
                chng,
                tm
            )
        )

colorama.init()
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
#init colors

prices = {}

def strick_price(symbol):
    summ = []
    with open(f"{today}_data.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if symbol in row:
                summ.append(float(row[3]))
                #print(symbol, row[3], row[4])
    res = round(sum(summ), 2)
    if res > 0:
        return str(f"{GREEN}{res}%{RESET}")
    else: return str(f"{RED}{res}%{RESET}")


print(f"{YELLOW}[*]\t" + "PAIR\t\t" + "PRICE FROM\t" + " PRICE TO\t" + f"CHACNGES%\tSUMM%\tTIME{RESET}")
def check_binance_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M:%S")
    data = response.json()
    for item in data:
        symbol = item["symbol"]
        price = float(item["price"])
        if symbol.endswith("USDT"):
            if  round(price, 5) != 0.0:
                if symbol in prices:
                    change = (price - prices[symbol]) / prices[symbol] * 100 # percentage change
                    if price > prices[symbol] * 1.01 or price < prices[symbol] * 0.99: # 1% change
                        if change > 2:
                            if len(symbol) > 7:
                                print(f"{GREEN}[+]\t" + f"{symbol}\t" + f"{str(round(prices[symbol], 5))}\t\t" + f"{str(round(price, 5))}\t" + f"\t\t" + str(round(change, 2)) + f"%\t{RESET}" + strick_price(symbol)+"\t"+ time )
                            else:
                                print(f"{GREEN}[+]\t" + f"{symbol}\t\t" + f"{str(round(prices[symbol], 5))}\t\t" + f"{str(round(price, 5))}\t" + f"\t\t" + str(round(change, 2)) + f"%\t{RESET}" + strick_price(symbol)+"\t"+ time)
                            csv_writer(symbol, prices[symbol], price, change, time)
                        elif change > 0:
                            if len(symbol) > 7:
                                print(f"{GREEN}[+]{RESET}\t" + f"{symbol}\t" + f"{str(round(prices[symbol], 5))}\t\t" + f"{str(round(price, 5))}\t" + f"\t\t{GREEN}" + str(round(change, 2)) + f"%\t{RESET}" + strick_price(symbol)+"\t"+ time)
                            else:
                                print(f"{GREEN}[+]{RESET}\t" + f"{symbol}\t\t" + f"{str(round(prices[symbol], 5))}\t\t" + f"{str(round(price, 5))}\t" + f"\t\t{GREEN}" + str(round(change, 2)) + f"%\t{RESET}" + strick_price(symbol)+"\t"+ time)
                            csv_writer(symbol, prices[symbol], price, change, time)
                        elif change < 0:
                            if len(symbol) > 7:
                                print(f"{RED}[-]{RESET}\t" + f"{symbol}\t" + f"{str(round(prices[symbol], 5))}\t\t" + f"{str(round(price, 5))}\t" + f"\t\t{RED}" + str(round(change, 2)) + f"%\t{RESET}" + strick_price(symbol)+"\t"+ time)
                            else:
                                print(f"{RED}[-]{RESET}\t" + f"{symbol}\t\t" + f"{str(round(prices[symbol], 5))}\t\t" + f"{str(round(price, 5))}\t" + f"\t\t{RED}" + str(round(change, 2)) + f"%\t{RESET}" + strick_price(symbol)+"\t"+ time)
                            csv_writer(symbol, prices[symbol], price, change, time)
                prices[symbol] = price


while True:
    try:

        check_binance_prices()
        time.sleep(10)
    except Exception as ex:
        print(f"{RED}main error sleep 20 sec{RESET}")
        time.sleep(30)


