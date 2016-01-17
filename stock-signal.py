import tushare
import pandas
import numpy

import StockPrice
import KDJ2
import RSI2
import ForceIndex2
import EMA

count=0
period=5

def KDJ_signal(hist_data):
    data=KDJ2.KDJ(hist_data,8)
    return 1 if data['J'][count-1] > data['J'][count-2] else 0

def RSI_signal(hist_data):
    data=RSI2.RSI(hist_data,13)
    return 1 if data['RSI'][count-1] > data['RSI'][count-2] else 0

def ForceIndex_signal(hist_data):
    data=ForceIndex2.FI(hist_data,13)
    return 1 if data['FI'][count-1] > data['FI'][count-2] else 0

def EMA_signal(hist_data):
    data=EMA.EMA(hist_data,13)
    return 1 if data['EMA'][count-1] > data['EMA'][count-2] else 0

def close_signal(hist_data):
    return 1 if hist_data['Close'][count-1] > hist_data['Close'][count-2] else 0

def adj_close_signal(hist_data):
    return 1 if hist_data['Adj Close'][count-1] > hist_data['Adj Close'][count-2] else 0

def calculate_stock_signal(hist_data):
    count=hist_data['Open'].count()
    
    if KDJ_signal(hist_data)*RSI_signal(hist_data)*ForceIndex_signal(hist_data) == 0:
        return 0
    else:
        return hist_data['Close'][count-1]

def stock_signal(stock):
    hist_data=StockPrice.StockPrice(stock)
    
    calculate_stock_signal(hist_data)

def stock_signal_w(stock):
    hist_data=StockPrice.StockPrice_w(stock)
    
    calculate_stock_signal(hist_data)

def adj_close_signal_new(hist_data):
    data=pandas.DataFrame(numpy.zeros(hist_data['Open'].count()),index=hist_data.index,columns=['close_s'])
    
    for i in range(hist_data['Open'].count()):
        data['close_s'][i]=1 if hist_data['Adj Close'][i]>hist_data['Adj Close'][i-1] else 0
    return data

def calculate_stock_signal_new(hist_data):
    count=hist_data['Open'].count()

    all_data=hist_data.join(KDJ2.KDJ(hist_data,period)).join(RSI2.RSI(hist_data,period)).join(ForceIndex2.FI(hist_data,period)).join(EMA.EMA(hist_data,period))
    all_data=all_data.join(adj_close_signal_new(hist_data))

    data=pandas.DataFrame(numpy.zeros(hist_data['Open'].count()*5).reshape(count,5),index=hist_data.index,columns=['signal','price','buy','sell','profit'])

    for i in range(count):
        data['price'][i]=all_data['Adj Close'][i]
        
        sum=all_data['KDJ_s'][i]+all_data['RSI_s'][i]+all_data['FI_s'][i]
        if sum>2 :
            if data['signal'].sum()>0:
	        continue
	    
            data['signal'][i]=1
            data['buy'][i]=all_data['Adj Close'][i]
        elif data['signal'].sum()>0 :
            if all_data['FI_s'][i]>0 :
	        continue;
            elif (all_data['EMA_s'][i]+all_data['close_s'][i])>0:
                continue
            else :
                data['sell'][i]=all_data['Adj Close'][i]
	        j=i-1
	        while data['signal'][j]<0.1 :
	            j=j-1
                data['profit'][i]=(data['sell'][i]-data['buy'][j])/data['buy'][j]
                data['signal'][i]=-1
                
    return all_data.join(data)

def stock_signal_w_new(stock):
    hist_data=StockPrice.StockPrice_w(stock)
    
    all_data=calculate_stock_signal_new(hist_data)

    all_data.to_csv('%sw-all-data.csv' % stock)
    
    return all_data
    
def stock_signal_w_new_sum(stock):
    all_data=stock_signal_w_new(stock)
    
    print stock,all_data['profit'].sum()

def stock_signal_w_new_detail(stock):
    all_data=stock_signal_w_new(stock)

    detail_data=all_data.select(lambda x: True if all_data.loc[x]['signal']!=0 else False)
    return detail_data[['signal','Adj Close', 'EMA', 'buy', 'sell', 'profit']]

def stock_signal_w_new_find_candidate(stock):
    all_data=stock_signal_w_new(stock)

    count=all_data['signal'].count()
    if all_data['signal'].sum() > 0 and all_data['Volume'][count-1] > 0:
        for i in range(count-1, 0, -1):
            if all_data['signal'][i]==1:
                return all_data.select(lambda x: True if x==all_data.index[i] else False)[['signal','Adj Close', 'EMA', 'buy', 'sell', 'profit']]
                break

def stock_signal_w_new_close_ema(stock):
    all_data=stock_signal_w_new(stock)

    print all_data[['signal','Adj Close', 'EMA']]
