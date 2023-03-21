function mapInitialization() {
    let centar = {"lat": 44.810556, "lng":20.472354}
    const mapica = new google.maps.Map(document.getElementById("mapa"), {
        zoom: 5,
        center: centar,
        mapTypeId: google.maps.MapTypeId.HYBRID
      });
    let markeri = [];
    events.forEach(function (elem){
        markeri.push(new google.maps.Marker({
            position: elem[0],
            icon: `/static/images/${elem[1]}32.png`
        }));
    });
    markeri.forEach(function (elem){       
        elem.setMap(mapica);
    })
}
window.initMap = mapInitialization;