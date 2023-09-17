function onClickedEstimateMoisture() {
    console.log("Estimate Moisture button clicked");
    var timeinMin = document.getElementById("uiTime").value;
    var timeHour= timeinMin*60
    var tempreture = document.getElementById("uiTempre").value;
    var air_humidity = document.getElementById("uiAirHum").value;
    var pressure = document.getElementById("uiPressure").value;
    var windSpeed = document.getElementById("uiWindSpeed").value;
    // console.log(timeinMin);
    // console.log(tempreture);
    // console.log(air_humidity);
    // console.log(pressure);
    // console.log(windSpeed);
    // var url = "http://127.0.0.1:5000/predict_home_price"; //Use this if you are NOT using nginx which is first 7 tutorials
    var url = "http://127.0.0.1:5000/predict_soil_moisture"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
    
    $.post(url, {
        timeinMin: parseInt(timeHour),
        tempreture: parseFloat(tempreture),
        air_hum: parseFloat(air_humidity),
        pressure: parseFloat(pressure),
        windSpeed: parseFloat(windSpeed)
    },function(data, status) {
        console.log(data.estimated_moisture);
        uiEstimatedMoist.innerHTML = "<h2>" +  data.estimated_moisture.toString() + "</h2>";
        console.log(status);
    });
  }