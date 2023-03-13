const url_stranice = window.location.href;
const forma = document.querySelector("#kontekst");
let expiration_date = forma.dataset.time.split(" ").map(Number);
expiration_date = new Date(expiration_date[0], expiration_date[1]-1,expiration_date[2],expiration_date[3],expiration_date[4]);

function check_time(){
    if(expiration_date.getTime() <  new Date()){
        alert("Oops! This form has expired, you'll be redirected to home page.");
        window.location = window.origin + "/";
    }
}

forma.addEventListener("submit", async function(e){
    e.preventDefault();
    check_time();
    respo = "";
    let pomp;
    for (let i = 1; i < (forma.childElementCount - 1); i++) {
        pomp = forma.children[i].cloneNode(true);

        if (pomp.childElementCount > 2) {
            //slucaj kada je checkb tip polja
            for (let j = 1; j < pomp.childElementCount; j++) {
                respo += (pomp.children[j].children[0].checked) + "`";
            }            
        }else{
            respo += pomp.children[1].value + "`";
        }        
    }
    let odg = await req_json({"form": forma.dataset.frm, "data": respo}, "POST");
    alert(odg["msg"])
})

check_time();