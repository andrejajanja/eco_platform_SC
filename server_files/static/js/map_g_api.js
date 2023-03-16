function mapInitialization() {
    let centar = {"lat": 44.810556, "lng":20.472354}
    if(ciscenja.length != 0){
        centar = ciscenja[0];
        ciscenja.forEach(function (elem){
            markeri.push(new google.maps.Marker({
                position: elem,
                icon: "/static/images/broom32.png"
            }));
        });
        markeri.forEach(function (elem){       
            elem.setMap(mapica);
        })
    }
    const mapica = new google.maps.Map(document.getElementById("mapa"), {
        zoom: 5,
        center: centar,
      });
}
window.initMap = mapInitialization;