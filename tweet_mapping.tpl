<!DOCTYPE html>
<html>

<head>
   <title>Leaflet marker array example</title>

       <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" />
<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>


    <!--
        <script src='https://api.tiles.mapbox.com/mapbox.js/v2.1.9/mapbox.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox.js/v2.1.9/mapbox.css' rel='stylesheet' />
        -->




</head>
<body>

   <div id="map" style="height: 600px"></div>



   <script type="text/javascript">
 var map = new L.Map('map');

      	 L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            maxZoom: 18
         }).addTo(map);
         map.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

         var nigeria = new L.LatLng(9.00,7.00);
         map.setView(nigeria,6);

        var myStyle = {
        radius:2.5,
        fillColor: "red",
        color: "red",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.6
            };



         //list will be past from the documents

        var markers=JSON.parse("{{! points }}");
        //alert(markers)
         //Loop through the markers array
         for (var i=0; i<markers.length ; i++) {

             var lon = markers[i][0];
             var lat = markers[i][1];
             //var popupText = markers[i][2];

             var markerLocation = new L.LatLng(lat, lon);
             var marker = new L.circleMarker(markerLocation,myStyle);
             map.addLayer(marker);

             //marker.bindPopup(popupText);
            //marker.on('mouseover', function (e) {
            //this.openPopup();
            //});
            //marker.on('mouseout', function (e) {
            //this.closePopup();
       // });
         }





</script>
</body>
</html>