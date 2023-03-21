function mapInitialization() {
    let centar = {"lat": 44.810556, "lng":20.472354}
    const mapica = new google.maps.Map(document.getElementById("mapa"), {
        zoom: 5,
        center: centar,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        mapTypeControl: false,
        streetViewControl: false
      });
    let markeri = [];
    events.forEach(function (elem){
        let pomMarker;
        let pomInfo;
        pomInfo = new google.maps.InfoWindow({
            content: `Event type: ${elem[1]}` //finnish content of this also close all the opened infoWindows if new marker is clicked
        })
        pomMarker = new google.maps.Marker({
            position: elem[0],
            icon: `/static/images/${elem[1]}32.png`
        })
        pomMarker.addListener("click", ()=>{
            pomInfo.open({
                anchor: pomMarker, mapica
            });
        });

        markeri.push(pomMarker);
    });
    markeri.forEach(function (elem){       
        elem.setMap(mapica);
    })
}
window.initMap = mapInitialization;