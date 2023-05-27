import pandas as pd
import sys
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import json

conn=mysql.connector.connect(host="localhost",user="suganth",password="suganth",database="project")
cur=conn.cursor()
s=sys.argv
path=s[1]
periodicity=s[2]
n_value=s[3]
id=s[4]
name=s[5]
os.system('touch '+path+'console.txt')
sys.stdout=open(path+'console.txt','w')
data = pd.read_csv(path+'data.csv', index_col=0, parse_dates=True)
valm=7
if(periodicity=='Weekly'):
    data=data.resample('W').sum()
    n_value=int(n_value)
if(periodicity=='Monthly'):
    data=data.resample('M').sum()
    valm=7
if(periodicity=='Yearly'):
    data=data.resample('M').sum()
    n_value=int(n_value)*12
    valm=7
data=data[:-1]
cur.execute("update reports set progress=33 where email='%s' and name='%s'"%(id,name))
conn.commit()
model = pm.auto_arima(data, start_p=0, start_q=0, max_p=5, max_q=5,
                      seasonal=True, trace=True, error_action='ignore',D=1,d=0,
                      suppress_warnings=True, stepwise=True,m=valm)
pred,conf=model.predict(int(n_value)+2,return_conf_int=True,alpha=0.60)
last=data[::-1]
last=last[0:1]
cur.execute("update reports set progress=66 where email='%s' and name='%s'"%(id,name))
conn.commit()
time.sleep(3)
new_row = pd.DataFrame({'Date':last.index[0],'Sales':np.nan,0:last.values[0][0]},index=[0])
new_row=new_row.set_index('Date')
pred=pd.concat([new_row,pred])
temp=[]
len_of_conf=len(conf)
temp.append(last.values[0][0])
temp.append(last.values[0][0])
conf=np.insert(conf,0,temp).reshape(len_of_conf+1,2)
cc=pd.DataFrame(conf)
#data1=pd.DataFrame({'Sales':data['Sales'],'Lower':np.NaN,'Upper':np.NaN})
data1=pd.DataFrame({'Lower':data['Sales'],'Sales':data['Sales'],'Upper':data['Sales']})
csv=pd.DataFrame({'Sales':pred[0],'Lower':cc[0].values,'Upper':cc[1].values})
csv=csv[1:]
csv=pd.concat([data1,csv])
data=data.to_json
pred=pred.to_json
dict={}
dict['Actual']=data
dict['Predicted']=pred
csv.to_csv(path+"result.csv")
os.system("touch "+path+"summary.txt")
os.system("touch "+path+"report.html")
fff=open(path+'summary.txt','w')
fff.write(str(model.summary()))
fff.close()
sys.stdout=open(path+'report.html','w')
print("<html><head><title>"+name+"""
</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
<script src="https://www.gstatic.com/charts/loader.js"></script>
</head>
<body>
<style>
html{
background:#efffd8;
}
tt{
margin-left:15px;
}
</style>
<h1 style="text-align:center;">
"""+name)
print("""
<br><br>
</h1>
<h2 text-align:center;>UPLOADED BY : """+id+"""</h2>
<h2>Prediction Graph</h2><br>
<div style="height:100%;" id="myChart"></div>
<br>
<h2>Model Summary</h2><br>
<style>
.summary{
background:#fae5a7;
padding:5px;
border:4px solid black;
width:100%;
letter-spacing:4px;
font-size:large;
text-align:center;
}
.console{
background:black;
color:white;
letter-spacing:3px;
font-size:large;
}
</style>
<div class='summary'><b><pre>
"""
)
summaryf=open(path+'summary.txt','r')
summarytxt=summaryf.readlines()
for i in summarytxt:
    print(i)
print("</pre></b></div>")
print("<br><h2>Console Output</h2><br><div class='console'><pre><br>")
consolef=open(path+"console.txt",'r')
consolef=consolef.readlines()
for i in consolef:
    print("<tt>"+i+"</tt>")
print("</pre></div>")
print("""
</body>
</html>
""")
print("""
<script>
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    """
)
da=pd.read_csv(path+"result.csv",sep=',')
da=da.values.tolist()
print("""
window.sessionStorage.setItem('data','"""+str(json.dumps(da)).replace(" ","")+"""')
var data = JSON.parse(window.sessionStorage.getItem("data"));
  data= JSON.stringify(data)
  data = JSON.parse(data);
  data.unshift(['Date','Upper','Sales','Lower']);
  var data = google.visualization.arrayToDataTable(data);
var options = {
  title:'"""+name+"""',
  titleTextStyle: {
    fontSize: 30,
    bold: true,
    color: 'grey',
    padding:'50px',
  },
  interpolateNulls: true,
  series:{
    0:{lineWith:2,color:'grey'},
    1:{lineWidth:6,color:'blue'},
    2:{lineWidth:2,color:'grey'},
  },
  areaOpacity: 0.2,
    backgroundColor: {
      stroke: 'grey',
      strokeWidth: 10
    }
};

var chart = new google.visualization.LineChart(document.getElementById('myChart'));
  chart.draw(data, options);
}
</script>
""")
os.system("touch "+path+"readme.txt")
sys.stdout=open(path+"readme.txt",'w')
print("""
SALES FORECASTING

1. report.html - 
        i)Prediction Graph of Input data
        ii)Summary of the Model used
        iii)Console Output while training the model and finding Best Fit
2.data.csv
        - Input Data Uploaded at the time of Report creation
3.result.csv
        - The predicted Value for Graph creation is stored in this file
4.config.json
        - The Input parameters such as owner, periodicity , and period is listed in this file
""")