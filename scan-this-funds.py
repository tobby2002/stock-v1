# -*- coding: utf-8 -*-

import LoadCode
import StockSignal
import pandas

funds=LoadCode.load_etf_code()

summary=None

ss_funds=[[510050,  '50ETF'],
          [510300,  '300ETF'],
          [510500,  '500ETF'],
          [510900,  'H股ETF'],
          [511010,  '国债ETF'],                    
          [518800, '黄金基金']]
for i in ss_funds:
    try:
        ret = StockSignal.stock_signal_w_new_find_candidate('%s.SS' % i[0])
    except Exception, ex:
        ret = None

    if not isinstance(ret, type(None)) :
        ret.insert(0,'code', i[0])
        ret.insert(ret.columns.size,'name', i[1])
        
        if not isinstance(summary, type(None)):
#            summary=pandas.DataFrame.append(summary,ret)
            summary=pandas.concat([ret, summary])
        else:
            summary=ret

sz_funds=[[159915, '创业板'],
          [159902, '中小板'],
          [150172, '证券B'],
          [150204, '传媒B']]
for i in sz_funds:
    try:
        ret = StockSignal.stock_signal_w_new_find_candidate('%s.SZ' % i[0])
    except Exception, ex:
        ret = None

    if not isinstance(ret, type(None)) :
        ret.insert(0,'code', i[0])
        ret.insert(ret.columns.size,'name', i[1])

        if not isinstance(summary, type(None)):
            summary=pandas.concat([ret, summary])
        else:
            summary=ret

print summary[['code','signal','EMA', 'buy', 'sell','profit','name']].sort_index()
