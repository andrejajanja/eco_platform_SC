function sifruj(plaintext)
{
    if(plaintext != null && plaintext != undefined && plaintext != "") { 
        return md5(plaintext);
    }
    return 0;
}
const url_stranice = window.location.href;
const forma = document.querySelector("#kontekst")
let status_dis = document.querySelector("#status_login")
forma.addEventListener("submit", async function(e){
    e.preventDefault();
    if(e.submitter.dataset.fun == "log"){
        let hash = sifruj(forma.pass.value)
        if(hash == 0){
            status_dis.style.display = "inline";
            status_dis.innerHTML = "You didn't enter your password correctly"
        }else{
            let odgovor = await req_json({ra: "log", us: forma.usname.value, ps: hash}, "POST")
            if(odgovor.status == 1){
                status_dis.style.display = "none";
                window.location.href = location.origin + "/user";        
            }else{
                status_dis.style.display = "inline";
                status_dis.innerHTML = odgovor.message;
            }            
        }
        return;
    }
    if(e.submitter.dataset.fun == "reg"){
        window.location.href = location.origin + "/registration";
        return;
    }
    if(e.submitter.dataset.fun == "forgp"){
        window.location.href = location.origin + "/forgotpassword";
        return;
    }
});