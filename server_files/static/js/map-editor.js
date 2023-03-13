const url_stranice = window.location.href;
let forma = document.querySelector("#kontekst");
let frm_lok = document.querySelector("#place");
let adr = document.querySelector("#adr");
let krd = document.querySelector("#kord");
let marker;

function mapInitialization() {
    let geocoder = new google.maps.Geocoder();
    const map = new google.maps.Map(document.getElementById("mapa"), {
        zoom: 5,
        center: { lat: 49.5260, lng: 15.2551 },
    });
    marker = new google.maps.Marker({
        position: {lat: 0, lang: 0},
        map,
      });
    map.addListener("click", async (event) => {
        marker.setPosition(event.latLng);
        let rez = await geocoder.geocode({location: event.latLng}).then((result) => {return result.results});
        adr.value = rez[3]["formatted_address"];
        let dic = event.latLng.toJSON()
        krd.value = dic["lat"] + "," + dic["lng"];
    })
}
window.initMap = mapInitialization;
frm_lok.addEventListener("submit", function(e){
    e.preventDefault();
    window.localStorage.setItem("post_lok", JSON.stringify([adr.value, krd.value]));
    window.location.href = window.origin + "/event-editor";
})