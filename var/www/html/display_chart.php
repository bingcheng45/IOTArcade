<?php $url = (isset($_SERVER['HTTPS']) ? "https" : "http") . ": $_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]"; ?>
<html>
  <head>
    <!--Load the AJAX API-->
   <script src="https://code.jquery.com/jquery-3.1.0.min.js"></script>
   <script src="http://d3js.org/d3.v3.min.js"></script>
   <script src="http://dimplejs.org/dist/dimple.v2.1.6.min.js"></script>
   <script>
      var svg;
	  var chart;
	  var mySeries;
	  var xAxis, yAxis;
	  
      function onRefreshChart(){
                             var url = "<?php $url ?>"
		  $("#message").text("Refreshing chart at: " + new Date() + url);
		  
		  var jqxhr = $.get(url + "/get_data.php", onGetResult)
             .done(function() {})
			 .fail(function() {})
			 .always(function() {});
      } //end onRefreshChart
	  
      function onGetResult(data, status){
		
		var ddata = JSON.parse(data);
		$("#chartData").text(data);
		chart.data = ddata;
		chart.draw(500);
	  } //end onGetResult
	  
      $(document).ready(function(){
		  svg = dimple.newSvg("#chartContainer",800,600);
		  chart = new dimple.chart(svg, null);
		  xAxis = chart.addCategoryAxis("x", "Time");
		  xAxis.addOrderRule("Time");
		  yAxis = chart.addMeasureAxis("y", "Light");
		  mySeries = chart.addSeries("LightTime", dimple.plot.line);
		  onRefreshChart();
		  setInterval(onRefreshChart,3000);
		}
	  );
	  
	</script>
    
    <title>IoT</title>
	
  <body>
     
     <div id="chartData"></div>
	 <div id="chartContainer"></div>
     <div id="message"></div>
  </body>
</html>
