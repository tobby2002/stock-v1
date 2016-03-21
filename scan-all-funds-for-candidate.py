import LoadCode
import StockSignal
import StockPrice
import pandas

funds=LoadCode.load_etf_code()

summary=None

for i in range(funds['FundName'].count()):
    try:
        if funds['FundCode'][i] < 500000:
            stock='%s.SZ' % funds['FundCode'][i]
        else:
            stock='%s.SS' % funds['FundCode'][i]

        ret = StockSignal.stock_signal_w_new_find_candidate_with_volume(stock)
    except Exception, ex:
        ret = None
    
    if not isinstance(ret, type(None)):
        ret.insert(0,'code', funds['FundCode'][i])
        ret.insert(ret.columns.size,'name', funds['FundName'][i])
        
        if not isinstance(summary, type(None)):
            summary=pandas.concat([ret, summary])
        else:
            summary=ret
            
if not isinstance(summary, type(None)):
    summary=summary.sort(['Volume'])
#    summary=summary.sort_values(['code', 'Volume'])
    summary.to_csv('funds-candidates.csv')
    print summary.to_string();
