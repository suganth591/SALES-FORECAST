import csv
import random
from datetime import timedelta
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import datetime
import time
def create():
        with open('sales.csv','w',newline='') as file:
         dx=datetime.datetime(2015,1,1)
         writer=csv.writer(file)
         writer.writerow(["Date","Sales"])
         x=random.randint(250,1000)
         for i in range(365*2):
          x+=random.randint(-2100,3000)
          d=random.randint(1000,10000)
          if(x<0):
           x=random.randint(100,500)
          x+=d/10000
          writer.writerow([dx.strftime("%Y-%m-%d"),str(round(x,4))])
          print(i,dx.strftime("%d-%m-%y"),x)
          dx=dx+timedelta(days=1)
def verify():
        df=pd.read_csv('sales.csv')
        df['Date']=pd.to_datetime(df['Date'])
        df.set_index(df['Date'],inplace=True)
        df=df.drop(columns=['Date'])
        X = df.values
        result=adfuller(X)
        return result
create()
while(verify()[1]>0.05 or verify()[0]>verify()[4]['5%'] or verify()[0]>verify()[4]['1%']):
    print(verify())
    create()
print(verify())
print("created")
