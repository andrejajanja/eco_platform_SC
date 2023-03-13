const url_stranice = window.location.href;
let ciscenja = []
async function ucitaj_kords() {
    let odg = await req_json({ra: "loks"}, "POST");
    let pom;
    odg.forEach(function (e){
        pom = e.split(",");
        ciscenja.push({lat: parseFloat(pom[0]), lng: parseFloat(pom[1])});
    })
    return;
}
ucitaj_kords();