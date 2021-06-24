from Model import Model
from Config import *
from AutoTrader import AutoTrader
from PriceIndices import MarketHistory
import time

if __name__ == '__main__':

    print("\n> Welcome to HODL Crypto-Investing AI\n\n")
  
    history = MarketHistory()
    df_history = history.get_history(COIN, "2013-01-01","2022-01-01")  
    df_history= df_history.iloc[::-1].reset_index()
    
    print("> Creating TRAINING Data for ***"+ COIN + "***"+ " from 2013-04-28 to 2022-01-01\n")
    train_data  =  history.get_price(COIN, "2013-04-28","2022-01-01") 
    train_data = train_data.iloc[::-1].reset_index()
    #print(">>PriceData:\n"+str(train_data.head(1)))
    time.sleep(TIMING) 

    print("> Creating TESTING Data for ***"+ COIN + "***"+ " from " +str(TESTING_YEARS-1)+"-12-31 to "+str(TESTING_YEARS)+"-12-31\n")
    test_data  =  history.get_price(COIN, str(TESTING_YEARS-1)+"-12-31",str(TESTING_YEARS)+"-12-31") 
    test_data = test_data.iloc[::-1].reset_index()
    #print(">>TestData: \n"+str(test_data.head(1)))
    time.sleep(TIMING) 

    test_model = Model("AutoTraderAI", train_data)
    auto_trader = AutoTrader(test_model)
    time.sleep(TIMING+TIMING) 
    auto_trader.runSimulation(test_data)
