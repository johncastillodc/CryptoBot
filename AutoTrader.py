from VirtualAccount import VirtualAccount
from Config import *
import time
import sys
from datetime import datetime
import dateutil.relativedelta


class AutoTrader:

    def __init__(self,model):
        self.advisor = model
        self.account = VirtualAccount()
        self.trade_amount = 1000 ## for 2016
        self.start_btc_price = 0 
        self.end_btc_price = 0
        self.now = datetime.now()
        self.sellingAll = False
        self.buyingAll = False
        

    def buy(self):
        prev_bought_at = self.account.bought_btc_at # How much did I buy BTC for before
        if self.account.usd_balance - self.trade_amount >= 0:
            if prev_bought_at == 0 or self.account.last_transaction_was_sell or (prev_bought_at > self.account.btc_price): #or (self.account.btc_price/prev_bought_at -1 > 0.005):
                if self.sellingAll == True:
                    print("\n>> BUYING ALL: $",self.trade_amount," ***"+COIN+ "***")
                else:
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
            if self.sellingAll == True:
                print("\n>> SELLING ALL: $",self.trade_amount," ***"+COIN+ "***")
            else:
                print("\n>> SELLING $",self.trade_amount," WORTH OF ***"+COIN+ "***")
            self.account.btc_amount -= (self.trade_amount / self.account.btc_price)
            self.account.usd_balance += self.trade_amount
            self.account.last_transaction_was_sell = True
        else:
            print(">> Not enough ***"+COIN+"*** left in your account to buy USD ")

    def runSimulation(self,year):
        
        print("\n\n\n> Starting to run simulation for ...",TESTING_YEARS)
        print("\n...Training bot with TIME SERIES Model using testing data...")
        time.sleep(TIMING) 
        
        sample = self.advisor.trainModel(year)

        if COIN == "bitcoin":
            if TESTING_YEARS == 2013:
                self.account.btc_balance= 144
            if TESTING_YEARS == 2014:
                self.account.btc_balance = 771
            if TESTING_YEARS == 2015:
                self.account.btc_balance= 314
            if TESTING_YEARS == 2016:
                self.account.btc_balance = 434
            if TESTING_YEARS == 2017:
                self.account.btc_balance = 998
            if TESTING_YEARS == 2018:
                self.account.btc_balance = 13657
            if TESTING_YEARS == 2019:
                self.account.btc_balance= 3843
            if TESTING_YEARS == 2020:
                self.account.btc_balance = 7200
            if TESTING_YEARS == 2021:
                self.account.btc_balance = 29374
            if TESTING_YEARS == 2022:
                self.account.btc_balance = 46195
        self.trade_amount = self.account.btc_balance
        self.initial_balance = self.account.btc_balance

        
        print("\n\n  *********************************************************************************************")
        print("  *                 Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
                  self.account.btc_balance, " USD: $", self.account.usd_balance, "                      *")
        print("  *********************************************************************************************")

        day_count = 0

      

        for i in sample.iterrows():
            day_count += 1            

            time.sleep(TIMING/12)
            btc_price = i[1].price

            if (i[0] == str(TESTING_YEARS)+"-01-01"):
                self.start_btc_price = i[1].price

            if (COIN == "bitcoin" and TESTING_YEARS==2013 and i[0] == str(TESTING_YEARS)+"-04-29"):
                self.start_btc_price = i[1].price

            today = int(self.now.strftime("%d"))
            if today<10:
                yesterday = "0"+str(today -1)
            else:
                yesterday = str(today -1)

            dating = self.now.strftime("%Y-%m-")
            allyesterday = dating+yesterday

            if today==1:
                lastMonth = self.now + dateutil.relativedelta.relativedelta(months=-1)
                allyesterday = lastMonth.strftime("%Y-%m-")+'31'

            if (i[0] == allyesterday or i[0] == str(TESTING_YEARS)+"-12-31"):
                self.end_btc_price = i[1].price
                  
            short_prediction = self.advisor.predict_short(i[1].Compra_curto, i[1].Venda_curto)           
            long_prediction = self.advisor.predict_long(i[1].BEAR_TREND, i[1].BULL_TREND)

            if (long_prediction == "Bull Trend" and  short_prediction == 'BUY' ) or (long_prediction == "Bull Trend" and  short_prediction == 'SELL' ) or (long_prediction == "Bear Trend" and self.account.last_transaction_was_sell == False ) :
                print("\n\n##########################################   DAY ",day_count,"   #########################################")
                print("\n"+str(i[0]) +" - "+long_prediction)
                print(str(i[0]) +" - "+short_prediction)
                print("The ***"+COIN+ "*** Price is: "+str(i[1].price))
                time.sleep(TIMING)
            else:
                sys.stdout.write('.')

            self.account.btc_balance = self.account.btc_amount * btc_price
            self.account.btc_price = btc_price

            if (long_prediction == "Bull Trend"):
                if short_prediction == 'BUY' :
                    if self.buyingAll == True:
                        self.trade_amount = self.account.usd_balance
                        self.buy()
                    else:
                        self.buy()
                if short_prediction == 'SELL':
                    self.sell()
            
            if (long_prediction == "Bear Trend" and self.account.last_transaction_was_sell == False):
                self.trade_amount = self.account.btc_balance
                self.sellingAll = True
                self.buyingAll = True
                self.sell()

            self.account.btc_balance = self.account.btc_amount * btc_price
        
            if (long_prediction != 'HODL' and short_prediction != 'HODL') or (self.sellingAll == True):
                print("\n    ********************************************************************************************   ")
                print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
              self.account.btc_balance, " USD: $", self.account.usd_balance, "")
                print("#################################################################################################\n\n")
                self.sellingAll = False

        profit = ((self.account.usd_balance + self.account.btc_balance - self.initial_balance) / (self.initial_balance) ) *100
        holdprofit = ((self.end_btc_price - self.start_btc_price)/self.start_btc_price) *100

        print("\n*****************************************   TOTAL   *********************************************")
        print("#           Account Balance: $", (self.account.usd_balance + self.account.btc_balance), " BTC: $",
              self.account.btc_balance, " USD: $", self.account.usd_balance, "")
        print("\n        =======================    BOT PROFIT: "+str(round(profit,2 ))+"%      =========================\n")
        print("\n        =======================   HOLD PROFIT: "+str(round(holdprofit,2 ))+"%      =========================\n")

        print("*************************************************************************************************")
        

