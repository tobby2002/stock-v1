import numpy
import pandas

def FI(hist_data, period):
    count = hist_data['Open'].count()
    data = pandas.DataFrame(numpy.zeros(count*3).reshape(count,3),
                            index=hist_data.index,
                            columns=['F','FI','FI_s'])

    for i in range(count):
        if hist_data['Volume'][i] > 0:
            data['F'][i]=(hist_data['Adj Close'][i] - hist_data['Adj Close'][i-1])*hist_data['Volume'][i]

            if i >= period:
                data['FI'][i]=(data['F'][i]*2 + data['F'][i-1]*(period-1))/(period+1)
                
            data['FI_s'][i]=1 if data['FI'][i]>data['FI'][i-1] and hist_data['Adj Close'][i]>hist_data['Open'][i] else 0
        else:
            data['F'][i]=0
            data['FI'][i]=0
            data['FI_s'][i]=0
    
    return data
