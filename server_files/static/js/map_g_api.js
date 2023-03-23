let win = document.querySelector("#templates").content.querySelector(".infoWindow");
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
    let check = true;
    events.forEach(function (elem){
        let pomMarker, pomInfo, winCont;
        winCont = win.cloneNode(true);
        winCont.children[0].innerHTML = elem[1];
        winCont.children[1].children[1].innerHTML = elem[2];
        winCont.children[2].children[1].innerHTML = elem[3];
        winCont.children[3].children[1].href = `/events/${elem[1].toLowerCase().replace(" ", "-")}`;
        winCont.children[4].children[1].href = `https://www.google.com/maps/search/?api=1&query=${elem[4]}`
        pomInfo = new google.maps.InfoWindow({
            content: winCont
        })
        pomMarker = new google.maps.Marker({
            position: elem[0],
            icon: `/static/images/${elem[2]}64.png`,
            optimize: true
        })

        if(check && elem[1] == window.localStorage.getItem("highLoc")){
            pomInfo.open({
                anchor: pomMarker, mapica
            });
            window.localStorage.removeItem("highLoc");
            check = false;
        }
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