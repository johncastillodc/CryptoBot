from Model import Model
from Config import *
from AutoTrader import AutoTrader
from PriceIndices import MarketHistory
import time

if __name__ == '__main__':

    print("\n> Welcome to the Swing Holder CryptoBot\n\n")
  
    history = MarketHistory()
    df_history = history.get_history(COIN, "2013-01-01","2022-01-01")  
    df_history= df_history.iloc[::-1].reset_index()
    
    print("> Creating TRAINING Data for ***"+ COIN + "***"+ " from 2013-04-28 to 2022-01-01\n")
    train_data  =  history.get_price(COIN, "2013-04-28","2022-01-01") 
    train_data = train_data.iloc[::-1].reset_index()
    time.sleep(TIMING) 


    test_model = Model("AutoTraderAI", train_data)
    auto_trader = AutoTrader(test_model)
    time.sleep(TIMING+TIMING) 
    auto_trader.runSimulation(TESTING_YEARS)
