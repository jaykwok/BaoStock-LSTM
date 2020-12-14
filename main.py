import baostock as bs
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import numpy as np

#登录系统
try:
    lg = bs.login()
except lg.error_code as e:
    print('login respond error! Code is ',e,', and message is ',lg.error_msg)

stock_code=['sz.002714','sz.300009']
rs=[]

#获取历史股票K线数据：
for code in stock_code:
    try:
        temp=bs.query_history_k_data_plus(code,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date='2020-01-01',
        frequency="d", adjustflag="2")
        rs.append(temp)
    except temp.error_code as e:
        print('Query history k data plus respond error! Stock code is ',e,' Error code is ',rs.error_code,', and message is ',rs.error_msg)

result=[]
for data_temp in rs:
    data_list = []
    while data_temp.next():
        data_list.append(data_temp.get_row_data())

    result.append(pd.DataFrame(data_list, columns=data_temp.fields))
    data_list.clear()

#计算股票代码序列的股票日均价
mid=[]
i=0
while(i<len(stock_code)):
    volume=np.array(result[i].loc[:,'volume']).astype(np.float)
    amount=np.array(result[i].loc[:,'amount']).astype(np.float)
    mid.append(amount/volume)
    i=i+1


# 绘图
plt.figure(1)
plt.plot(mid[0])
plt.title(stock_code[0])
plt.figure(2)
plt.plot(mid[1])
plt.title(stock_code[1])
plt.show()

#lstm测试效果



#登出系统
try:
    lg = bs.logout()
except lg.error_code as e:
    print('login respond error! Code is ',e,', and message is ',lg.error_msg)