const url_stranice = window.location.href;
let events = []
async function ucitaj_kords() {
    let odg = await req_json({ra: "loks"}, "POST");
    let pom;
    odg.forEach(function (e){
        pom = e[0].split(",");
        events.push([{lat: parseFloat(pom[0]), lng: parseFloat(pom[1])}, e[1], e[2], e[3], e[0]]);
    })
    return;
}
ucitaj_kords();