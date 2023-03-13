function mapInitialization() {
    const mapica = new google.maps.Map(document.getElementById("mapa"), {
      zoom: 7, //this needs to be fixed in the future
      center: ciscenja[0], //this needs to be fixed in the future
    });
    let markeri = [];
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
window.initMap = mapInitialization;