import sqlalchemy as db
import matplotlib.pyplot as plt
from datetime import datetime as dt, timedelta as timedelta
from sqlalchemy.sql import text #, exc

"""
Todo:
Fetch day + number days before
Fetch current value
Fetch from to  
configure database from file  
"""


#constatnts
TABLENAME = 'records'

class MeteoFetch:
    
    def __init__(self, table_name):
        self.engine = db.create_engine('mysql://u943545564_krizjan8:garena09@sql280.main-hosting.eu/u943545564_meteo') # lze resist i pomoci try catch https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects
        self.metadata = db.MetaData()
        self.table = db.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
        self.conn = self.engine.connect()
        
        
    def fetch_day_data(self, data_type, days_back):
        date_to = (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        print(date_to)
        date_from = (dt.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        #todaydtstr = todaydt.strftime("%Y-%d-%m") 
        
        query = text("SELECT * FROM records WHERE timestamp BETWEEN '{}' AND '{}' AND value_type LIKE '{}'".format(date_from, date_to,data_type)) #'2020-05-17 00:00:00.000000'
        
        try:
            dataset = self.conn.execute("SELECT 1")
            self.conn.close()
            
        except: #exc.DBAPIError:
            #if self.conn.connection_invalidated:
                print("Connection was invalidated!")
        self.conn = self.engine.connect()
        dataset = self.conn.execute(query)
                
              
        d, a = {}, []
        for x in dataset:
            for column, value in x.items():
                d = {**d, **{column: value}}
                if d.get("value_type") == data_type:
                    a.append(d)
              
        return a       

def plot(data):
    plt.figure()
    time, values = [], []
    for data_type in data:
        for x in data_type:       
            time.append(x.get("timestamp"))    
            values.append(x.get("value"))
        plt.plot(time,values)
        time.clear()
        values.clear()
    plt.legend(loc='best')    
        
  
    
    #plt.setp(lines, color ='b')
    plt.xlabel("Time")
    plt.ylabel("Temperature [°]")
    plt.title("Teplota v obyvaku")
    #plt.axis([0, 6, 0, 20])
    plt.grid(True)
    
    plt.show()
            
    
"main"    
service = MeteoFetch(TABLENAME)
days_back = 60
data = list()
#data.append(service.fetch_day_data("in_humi"))
data.append(service.fetch_day_data("out_temp",days_back))
data.append(service.fetch_day_data("in_temp",days_back))
#data.append(service.fetch_day_data("in_press",days_back))
#data.append(service.fetch_day_data("in_humi",days_back))
plot(data)

#
#data2 = list()
#data2.append(service.fetch_day_data("in_humi",days_back))
#data2.append(service.fetch_day_data("in_press",days_back))
#plot(data2)

#tlak a humu za posledni dva dnz
#teplota prekryta za posledni dva dny
#teploty za poslednich 7 dni



#%%

import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


root= tk.Tk()
fmt = mdates.DateFormatter('%H:%M')
  
time1, time2, intemp, outtemp = [], [], [], []
data_type = service.fetch_day_data("out_temp",4)
for x in data_type:       
    time1.append(x.get("timestamp"))    
    outtemp.append(x.get("value"))
    
data_type = service.fetch_day_data("in_temp",4)
for x in data_type:       
    time2.append(x.get("timestamp"))     
    intemp.append(x.get("value"))    


figure1 = plt.Figure(figsize=(10,5), dpi=100)
ax1 = figure1.add_subplot(111)
ax1.plot(time2, intemp)
ax1.plot(time1, outtemp)
ax1.xaxis.set_major_formatter(fmt)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)
ax1.set_title('Temperatures last 4 days')
ax1.legend(['In','Out'])
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature [°]")
ax1.grid(True)


press, time1 = [],[]
data_type = service.fetch_day_data("in_press",5)
for x in data_type:       
    time1.append(x.get("timestamp"))    
    press.append(x.get("value"))
    
figure2 = plt.Figure(figsize=(5,4), dpi=100)
ax2 = figure2.add_subplot(111)
ax2.xaxis.set_major_formatter(fmt)
ax2.yaxis.tick_right()
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
ax2.plot(time1, press,'r')

ax2.set_title('Pressure last 5days')
#ax2.legend(['Pressure'])
ax2.set_xlabel("Time")
ax2.set_ylabel("Pressure [hPa]")
ax2.grid(True)


time, values = [], []
data_type = service.fetch_day_data("in_humi",2)
for x in data_type:       
    time.append(x.get("timestamp"))    
    values.append(x.get("value"))

figure3 = plt.Figure(figsize=(5,4), dpi=100)
ax3 = figure3.add_subplot(111)
ax3.plot(time, values, 'g')
ax3.xaxis.set_major_formatter(fmt)
ax3.yaxis.tick_right()

scatter3 = FigureCanvasTkAgg(figure3, root) 
scatter3.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
ax3.set_title('Humidity last 2 days')
ax3.set_xlabel("Time")
ax3.set_ylabel("Humidity [%]")
ax3.grid(True)

root.mainloop()


#%%

import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data1 = {'Country': ['US','CA','GER','UK','FR'],
         'GDP_Per_Capita': [45000,42000,52000,49000,47000]
        }
df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])


data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        }
df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])


data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
         'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
        }  
df3 = DataFrame(data3,columns=['Interest_Rate','Stock_Index_Price'])
 

root= tk.Tk() 
  
figure1 = plt.Figure(figsize=(10,5), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH)
df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Country Vs. GDP Per Capita')

figure2 = plt.Figure(figsize=(5,4), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
ax2.set_title('Year Vs. Unemployment Rate')

figure3 = plt.Figure(figsize=(5,4), dpi=100)
ax3 = figure3.add_subplot(111)
ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
scatter3 = FigureCanvasTkAgg(figure3, root) 
scatter3.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
ax3.legend(['Stock_Index_Price']) 
ax3.set_xlabel('Interest Rate')
ax3.set_title('Interest Rate Vs. Stock Index Price')

root.mainloop()
 
#%% tet

todaydt = dt.now() - timedelta(days=1)
todaydtstr = todaydt.strftime("%Y-%d-%m") 

print(todaydtstr)


#%%
"""
todaydt = dt.now()
todaydtstr = todaydt.strftime("%Y-%d-%m")
yesterdaydt = todaydt - timedelta(days=1)
yesterdaystr =yesterdaydt.strftime("%Y-%d-%m")

from datetime import datetime as dt, timedelta as td
from datetime import timedelta
now = dt.now() - timedelta(days=1)
now = now.replace(hour=0, minute=0, second=0, microsecond=0)
#time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
print(now)
print(dt.now().replace(microsecond=0).isoformat(sep=' '))
a = "aaa" + now.strftime("%Y-%d-%m %H:%M:%S") + "ss"
print(a)

#todayQuery = "SELECT * FROM records_test WHERE timestamp > '" + todaydtstr + " 00:00:00' AND value_type LIKE 'in_temp'"
#yesterdayQuery = "SELECT * FROM records_test WHERE timestamp < '" + yesterdaystr + " 00:00:00' AND timestamp < '" + yesterdaystr +" 23:59:59' AND value_type LIKE 'in_temp'"



#s = text("SELECT * FROM records_test WHERE timestamp > '2020-01-25 22:15:00' AND value_type LIKE 'in_temp'")
todayQuery = text(todayQuery)
#yesterdayQuery = text(yesterdayQuery)
todayset = 
#yesterday = conn.execute(yesterdayQuery)
"""