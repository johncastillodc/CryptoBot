import numpy as np
from PriceIndices import Indices
import numpy as np
from Config import *
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class Model:

    def __init__(self,model_name,x_train):
        print("> Model is starting ... ",model_name+"\n")
        self.model_name = model_name
        self.model = self.buildModel(x_train)
        
    def crossover_curto(self,df_ema):
        df_ema['Anter_curto'] = df_ema[EMASHORTLOW].shift(1) - df_ema[EMASHORTHIGH].shift(1)
        df_ema['Atual_curto'] = df_ema[EMASHORTLOW] - df_ema[EMASHORTHIGH]
        
        df_ema.loc[(df_ema['Anter_curto'] < 0) & (df_ema['Atual_curto'] > 0), 'Compra_curto'] = df_ema['price']
        df_ema.loc[(df_ema['Anter_curto'] > 0) & (df_ema['Atual_curto'] < 0), 'Venda_curto'] = df_ema['price']

        columns = ['date', 'price',EMASHORTLOW, EMASHORTHIGH, 'Compra_curto', 'Venda_curto']
        return df_ema[columns]

    
    def crossover_longo(self,df_ema):
        distance = ( (df_ema['price'] - df_ema[EMALONG])/df_ema['price'] )* 100

        df_ema.loc[distance >= BEAR_TREND_LIMIT, 'BULL_TREND'] = distance
        df_ema.loc[distance <  BEAR_TREND_LIMIT, 'BEAR_TREND'] = distance

        columns = ['date', 'price', EMALONG, 'BULL_TREND', 'BEAR_TREND']

        return df_ema[columns]


    def buildModel(self,x_train):
        indices = Indices(df=x_train)

        df_ema_longo = indices.get_exponential_moving_average(periods=[140,200])
        output_df_longo = self.crossover_longo(df_ema_longo)
        output_df_longo.set_index('date', inplace=True)

        df_ema_curto = indices.get_exponential_moving_average(periods=[EMASHORTL,EMASHORTH])
        output_df_curto = self.crossover_curto(df_ema_curto)
        output_df_curto.set_index('date', inplace=True)
      
        output_df_longo[EMASHORTLOW] = output_df_curto[EMASHORTLOW]
        output_df_longo[EMASHORTHIGH] = output_df_curto[EMASHORTHIGH]
        output_df_longo['Compra_curto'] = output_df_curto['Compra_curto']
        output_df_longo['Venda_curto'] = output_df_curto['Venda_curto']
      
        dfmerged = output_df_longo
        return dfmerged

    def plot_model(self, data, ano):
        venda = data[data['Venda_curto'].isnull()==False]
        compra = data[data['Compra_curto'].isnull()==False] 
        fig, ax = plt.subplots()
        ax.plot(data.index, data['price'], label='Price', alpha=0.5)
        ax.plot(data.index, data[EMASHORTLOW], label=EMASHORTLOW, color='orange')
        ax.plot(data.index, data[EMASHORTHIGH], label=EMASHORTHIGH, color='brown')
        ax.plot(data.index, data[EMALONG], label=EMALONG, color='blue')
        ax.scatter(data.index, data['Compra_curto'],label='Compra_curto', marker='^', color='green')
        ax.scatter(data.index, data['Venda_curto'],label='Venda_curto', marker='v', color='red')
        ax.scatter(data.index, data['BULL_TREND'], label='BULL_TREND', marker='^', color='green')
        ax.scatter(data.index, data['BEAR_TREND'], label='BEAR_TREND', marker='v', color='red')
        plt.gcf().autofmt_xdate()
        ax.legend()
        ax.set_title("Moeda: "+COIN +"- Estratégia de Médias Moveis - %.i" %ano) 
        ax.set_xlabel('Data')
        ax.set_ylabel('Price')
        plt.show()
        return compra, venda

    def trainModel(self,testing_year): 

        allhistory= self.model 
        print("TrainedModel - All history: \n"+str(allhistory))
        
        extracttesting = allhistory.loc[str(testing_year)+"-01-01":str(testing_year)+"-12-31"]
        print("TrainedModel - Extracted: \n"+str(extracttesting))     

        self.plot_model(extracttesting, testing_year)
        print("\n\n > LONG MARKET TREND strategy based on "+EMALONG+" support ...")

        extract_bull = extracttesting[extracttesting['BULL_TREND'].isnull()==False] 
        print("\n>> Bull Trend dates: \n: "+str(extract_bull))
        time.sleep(TIMING*2) 

        extract_bear = extracttesting[extracttesting['BEAR_TREND'].isnull()==False] 
        print("\n>> Bear Trend dates: \n: "+str(extract_bear))
        time.sleep(TIMING*2) 

        print("\n\n > SHORT MARKET VOLATILITY strategy based on "+EMASHORTLOW+" and "+EMASHORTHIGH+" crossover...")

        extract_curto_compra = extracttesting[extracttesting['Compra_curto'].isnull()==False]
        print("\n>> SHORT Buy dates: \n: "+str(extract_curto_compra))
        time.sleep(TIMING*2) 

        extract_curto_venda = extracttesting[extracttesting['Venda_curto'].isnull()==False] 
        print("\n>> SHORT Sell dates: \n: "+str(extract_curto_venda))
        time.sleep(TIMING*2) 

        return extracttesting

    def predict_short(self,curto_compra, curto_vende):
        if (np.isnan(curto_compra) == False):
            short_prediction = 'BUY' 
        elif (np.isnan(curto_vende) == False):
            short_prediction = 'SELL'      
        else:
            short_prediction = 'HODL'

        return short_prediction

    def predict_long(self,longo_compra, longo_vende):
        if (np.isnan(longo_compra) == False):
            long_prediction = 'Bear Trend'
        elif (np.isnan(longo_vende) == False):
            long_prediction = 'Bull Trend'
        else:
            long_prediction = 'HODL'

        return long_prediction
