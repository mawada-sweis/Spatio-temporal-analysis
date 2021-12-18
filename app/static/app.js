function draw_rectangle(){
    lon_max = document.getElementById("lon_max").value
    lat_max = document.getElementById("lat_max").value
    lon_min = document.getElementById("lon_min").value
    lat_min = document.getElementById("lat_min").value
    
    //define rectangle geographical bounds
    var bounds = [[lon_max, lat_max],[lon_min, lat_min]];
    
    // create an orange rectangle
    L.rectangle(bounds, {color: "#ff7800", weight: 1}).addTo(map);
        
    // zoom the map to the rectangle bounds
    map.fitBounds(bounds);    
}
