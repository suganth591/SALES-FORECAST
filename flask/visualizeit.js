google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);


function drawChart() {
  var data = window.opener.sessionStorage.getItem("data");
  data = JSON.parse(data);
  data.unshift(['Date','Upper','Sales','Lower']);
  var data = google.visualization.arrayToDataTable(data);
var options = {
  title:'Sales Forecasting '+window.opener.sessionStorage.getItem("Name")+"\n\n",
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
