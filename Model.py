import numpy as np
from PriceIndices import Indices
import numpy as np
from Config import *

class Model:

    def __init__(self,model_name,x_train):
        print("> Model is starting ... ",model_name+"\n")
        self.model_name = model_name
        self.model = self.buildModel(x_train)
        
    def crossover_curto(self,df_ema):
        df_ema['Anter_curto'] = df_ema['EMA_9'].shift(1) - df_ema['EMA_21'].shift(1)
        df_ema['Atual_curto'] = df_ema['EMA_9'] - df_ema['EMA_21']
        
        df_ema.loc[(df_ema['Anter_curto'] < 0) & (df_ema['Atual_curto'] > 0), 'Compra_curto'] = df_ema['price']
        df_ema.loc[(df_ema['Anter_curto'] > 0) & (df_ema['Atual_curto'] < 0), 'Venda_curto'] = df_ema['price']

        columns = ['date', 'price','EMA_9', 'EMA_21', 'Compra_curto', 'Venda_curto']
        print("\n>> EMA-9 and EMA-21 processed: \n"+str(df_ema[columns]))
        return df_ema[columns]

    
    def crossover_longo(self,df_ema):
        distance = ( ( df_ema['price'] - df_ema['EMA_200'] )/df_ema['price'] )* 100

        df_ema.loc[distance > LONG_SELL_CPT , 'Venda_longo'] = df_ema['price']
        df_ema.loc[distance < -LONG_BUY_CPT, 'Compra_longo'] = df_ema['price']

        columns = ['date', 'price', 'EMA_200', 'Compra_longo', 'Venda_longo']

        return df_ema[columns]


    def buildModel(self,x_train):
        indices = Indices(df=x_train)
        df_ema_curto = indices.get_exponential_moving_average(periods=[9,21])
        output_df_curto = self.crossover_curto(df_ema_curto)
        output_df_curto.set_index('date', inplace=True)
        #print("BuildModel - output_df_curto: "+str(output_df_curto.head()))
        df_ema_longo = indices.get_exponential_moving_average(periods=[21,200])
        output_df_longo = self.crossover_longo(df_ema_longo)
        output_df_longo.set_index('date', inplace=True)

        df_ema_curto['EMA_200'] = df_ema_longo['EMA_200']
        return output_df_curto,output_df_longo
    
    def trainModel(self,ds):   
        indices = Indices(df=ds)
        df_curto = indices.get_exponential_moving_average(periods=[9,21])
        df_curto = self.crossover_curto(df_curto)
        df_curto.set_index('date', inplace=True)
        # print("TrainModel - df: "+str(df.head()))
        df_longo = indices.get_exponential_moving_average(periods=[21,200])
        df_longo = self.crossover_longo(df_longo)
        df_longo.set_index('date', inplace=True)

        df_curto['EMA_200'] = df_longo['EMA_200']
        df_curto['BUY_TREND'] = df_longo['Compra_longo']
        df_curto['SELL_TREND'] = df_longo['Venda_longo']
        dfmerged = df_curto
        return dfmerged

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
            long_prediction = 'BUY Trend'
        elif (np.isnan(longo_vende) == False):
            long_prediction = 'SELL Trend'
        else:
            long_prediction = 'HODL'

        return long_prediction