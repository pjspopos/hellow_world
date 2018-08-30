import pymssql
import pandas as pd
import numpy as np
import matplotlib as mpl           # 그래프를 그리는 모듈
import matplotlib.pyplot as plt    
import matplotlib.dates as mdates
import datetime

class get_us_stock_info:
    def __init__(self,ticker,division):
        con = pymssql.connect(host='183.90.136.16', user='pjspopos', password='ericseon91')
        cur = con.cursor()
        sql = "select * from RawData.Dbo.us_stock_fidata_sf1 where ticker='{}' and division='{}'".format(ticker,division)
        cur.execute(sql)
        output = pd.DataFrame(cur.fetchall())
        colNameList = []
        for j in range(len(cur.description)):
            desc = cur.description[j]
            colNameList.append(desc[0])
        output.columns=colNameList
        self.ticker=ticker
        self.division=division
        self.df=output
        self.interested_item=["eps","assets","liabilities","debt","roe","roa",\
                 "gp","pe","ps","pb","divyield","currentratio"]
    def get_data(self,tg):
        filter1=self.df[self.df.item==tg]
        tg=filter1[['logdate','value_']]
        tg.set_index('logdate',inplace=True)
        return(tg)
    def draw_data(self,tg):
        filter1=self.df[self.df.item==tg]
        unit=filter1.unit.iloc[0]
        filter2=filter1[['logdate','value_']]
        filter2.set_index('logdate',inplace=True)
        ax=filter2.plot(kind='bar',title=self.ticker,legend=True,figsize=(12,4))
        ax.set_xlabel('timeperiod')
        ax.set_ylabel(unit)
        ax.legend([tg])
    def fundamental_summary(self):
        dict_data={val:self.__class__.get_data(self,val).value_.tolist() for val in self.interested_item}
        index_=self.__class__.get_data(self,'pe').index.tolist()
        df=pd.DataFrame(dict_data,index=index_)
        return(df)
    def draw_fundamental_summary(self):
        summary=self.__class__.fundamental_summary(self)
        axes=summary.plot.bar(rot=0,subplots=True,figsize=(12,12))
        axes[1].legend(loc=2)
    
        
a=get_us_stock_info('AAPL','ART')
b=get_us_stock_info('nvda','arq')
c=get_us_stock_info('AMZN','art')
d=get_us_stock_info('FB','ART')



b.draw_fundamental_summary()

        
        
        




























