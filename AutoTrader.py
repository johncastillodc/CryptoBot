from VirtualAccount import VirtualAccount
from Config import *
import time
import sys
from datetime import datetime


class AutoTrader:

    def __init__(self,model):
        self.advisor = model
        self.account = VirtualAccount()
        self.trade_amount = 1000
        self.start_btc_price = 0 
        self.end_btc_price = 0
        self.now = datetime.now()

    def buy(self):
        prev_bought_at = self.account.bought_btc_at # How much did I buy BTC for before
        if self.account.usd_balance - self.trade_amount >= 0:
            if prev_bought_at == 0 or self.account.last_transaction_was_sell or (prev_bought_at > self.account.btc_price): #or (self.account.btc_price/prev_bought_at -1 > 0.005):
                print(">> BUYING $",self.trade_amount," WORTH OF ***"+COIN+ "***")
                self.account.btc_amount += self.trade_amount / self.account.btc_price
                self.account.usd_balance -= self.trade_amount
                self.account.bought_btc_at = self.account.btc_price
                self.account.last_transaction_was_sell = False
            else:
                print(">> Not worth buying more ***"+COIN+ "*** at the moment")
        else:
            print(">> Not enough USD left in your account to buy ***"+COIN+ "***")

    def sell(self):
        if self.account.btc_balance - self.trade_amount >= 0:
            print(">> SELLING $",self.trade_amount," WORTH OF ***"+COIN+ "***")
            self.account.btc_amount -= (self.trade_amount / self.account.btc_price)
            self.account.usd_balance += self.trade_amount
            self.account.last_transaction_was_sell = True
        else:
            print(">> Not enough ***"+COIN+"*** left in your account to buy USD ")

    def runSimulation(self,samples):
        
        print("\n\n\n> Starting to run simulation for ...",TESTING_YEARS)
        print("\n\n >> Training bot with Time Series Model for testing data...")
        time.sleep(TIMING) 
        
        sample = self.advisor.trainModel(samples)

        print("\n\n >> SHORT strategy based on EMA 21-9 crossover...")
        
        extract_curto_compra = sample[sample['Compra_curto'].isnull()==False]
        print("\n\n>>SHORT Buy dates: \n: "+str(extract_curto_compra))
        time.sleep(TIMING*2) 

        extract_curto_venda = sample[sample['Venda_curto'].isnull()==False] 
        print("\n>>SHORT Sell dates: \n: "+str(extract_curto_venda))
        time.sleep(TIMING*2) 

        print("\n\n >> LONG TREND strategy based on EMA 200 support ...")

        extract_longo_compra = sample[sample['BUY_TREND'].isnull()==False]
        print("\n\n>>LONG Buy dates: \n: "+str(extract_longo_compra))
        time.sleep(TIMING*2) 

        extract_longo_venda = sample[sample['SELL_TREND'].isnull()==False] 
        print("\n>>LONG Sell dates: \n: "+str(extract_longo_venda))
        time.sleep(TIMING*2) 


        
        print("\n\n  *********************************************************************************************")
        print("  *                 Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
                  self.account.btc_balance, " USD: $", self.account.usd_balance, "                           *")
        print("  *********************************************************************************************")

        day_count = 0

        for i in sample.iterrows():
            #print("The index is: \n"+str(i))
            day_count += 1
            short_prediction = self.advisor.predict_short(i[1].Compra_curto, i[1].Venda_curto)
            #print(str(i[0]) +" - "+short_prediction)
            
            
            long_prediction = self.advisor.predict_long(i[1].BUY_TREND, i[1].SELL_TREND)

            if (long_prediction != 'HODL'):
                print("\n"+str(i[0]) +" - "+long_prediction)
            else:
                sys.stdout.write('.')

            time.sleep(TIMING/12)
            btc_price = i[1].price

            if (i[0] == str(TESTING_YEARS)+"-01-01"):
                self.start_btc_price = i[1].price

            if (COIN == "bitcoin" and TESTING_YEARS==2013 and i[0] == str(TESTING_YEARS)+"-04-28"):
                self.start_btc_price = i[1].price

            today = int(self.now.strftime("%d"))
            yesterday = str(today -1)

            dating = self.now.strftime("%Y-%m-")
            allyesterday = dating+yesterday

            if (i[0] == allyesterday or i[0] == str(TESTING_YEARS)+"-12-31"):
                self.end_btc_price = i[1].price

            if (short_prediction != 'HODL' or long_prediction != 'HODL'):
                print("\n\n##########################################   DAY ",day_count,"   #########################################")
                print(str(i[0]) +" - "+short_prediction)
                print("The Price is: "+str(i[1].price))
                time.sleep(TIMING)


            if self.account.btc_price != 0:
                self.account.btc_balance = self.account.btc_amount * btc_price
            self.account.btc_price = btc_price
            if short_prediction == 'BUY' or long_prediction == "BUY Trend":
                self.buy()
            if short_prediction == 'SELL' or long_prediction == "SELL Trend":
                self.sell()
            self.account.btc_balance = self.account.btc_amount * btc_price
            #time.sleep(TIMING/12)  # Only for Visual Purposes
        
            if (short_prediction != 'HODL' or long_prediction != 'HODL'):
                print("    ********************************************************************************************   ")
                print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
              self.account.btc_balance, " USD: $", self.account.usd_balance, "")
                print("#################################################################################################\n\n")  

        profit = ((self.account.usd_balance + self.account.btc_balance - 2000) / (2000) ) *100
        holdprofit = ((self.end_btc_price - self.start_btc_price)/self.start_btc_price) *100

        print("\n*****************************************   TOTAL   *********************************************")
        print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
              self.account.btc_balance, " USD: $", self.account.usd_balance, "")
        print("\n        =======================        PROFIT: "+str(round(profit,2 ))+"%      =========================\n")
        print("\n        =======================   HOLD PROFIT: "+str(round(holdprofit,2 ))+"%      =========================\n")

        print("*************************************************************************************************")
        

