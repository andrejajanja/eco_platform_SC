//#region variables
const url_stranice = window.location.href;
let folded = true;
let kontekst = document.querySelector("#kontekst");
let loader = document.querySelector("#loader");
let posts = document.querySelector("#posts");
let posts_list = document.querySelector("#posts_list");
let editor = document.querySelector("#editor");
let img_cont = document.querySelector("#images_container");
let image_box = document.querySelector("#image_box");
let img_btn = document.querySelector("#img_btn");
//event components
let add_dugme = document.querySelector("#images_add_btn");
let images = document.querySelector("#images");
let prew = document.querySelector("#previewed");
let file_upload = document.querySelector("#files");
let title = document.querySelector("#post_title");
let lok_btn = document.querySelector("#btn_lok");
let forms = document.querySelector("#sel_frm");
let dogs = document.querySelector("#sel_eve");
let date = document.querySelector("#post_date");
let event_txt = document.querySelector("#editor_text")
let default_image = window.location.origin +"/static/images/insert-picture-icon.png";
//templates
let templates = document.querySelector("#templates").content;
let lil_img = templates.querySelector(".added_image");
let post_add = templates.querySelector(".posts_post");
let opcija_frm = templates.querySelector(".opcija_frm");
let pom_kords = [];
//#endregion variables

let f = "https://stackoverflow.com/questions/10317017/javascript-get-domain-only-from-document-referrer";

//#region functions
async function savePost() {
    let pomm;
    if(editor.dataset.tren == ""){
        if(title.value == ""){
            alert("You can't save a post without title.");
            return;
        }else{
            pomm = title.value.replaceAll(" ", "-").toLowerCase();
            editor.dataset.tren = pomm;
        }
        
    }else{
        
        pomm = editor.dataset.tren;
    }

    if(dogs.selectedIndex == 0)
    {
        alert("You must select an event type.");
        return;
    }

    if(date.value == ""){
        alert("You must select a date on which the event occurs.");
        return;
    }

    pom = {};
    pom["head"] = title.value;
    pom["date"] = date.value;
    pom["txt"] = event_txt.value;
    pom["lok"] = lok_btn.dataset.lok;
    pom["kords"] = lok_btn.dataset.cords;
    pom["frm"] = forms.value;
    pom["type"] = dogs.value;
    pom["imgs"] = [];
    for (let i = 1; i < images.children.length; i++) {
        if(images.children[i].src == ""){
            continue;
        }
        pom["imgs"].push(images.children[i].src);
    }
    odg = await req_json({"ra": "svd","file": pomm, "data": JSON.stringify(pom), "lok": lok_btn.dataset.cords}, "POST");
    await dajPostove();
}
async function dajForme() {
    let pom;
    let odg = await req_json({"ra": "frms"}, "POST");
    forms.innerHTML = "";
    pom = opcija_frm.cloneNode(true);
    pom.value = "";
    pom.innerHTML = "Choose a form";
    forms.appendChild(pom);
    JSON.parse(odg["frms"]).forEach(function(frm){
        pom = opcija_frm.cloneNode(true);
        pom.value = frm;
        pom.innerHTML = frm;
        forms.appendChild(pom);
    })
}
function dodeliDesniKlik() {
    for (let i = 1; i < images.children.length; i++) { 
        images.children[i].onmousedown = async function (e) {
            if (e.which == 3) {
                let odg = await req_json({"ra": "dlt_img", "img": images.children[i].src}, "POST");                
                console.log(odg["msg"]);
                await savePost();
                images.removeChild(images.children[i]);                
                dodeliDesniKlik();
            }
        };
    }    
}
async function dajPostove() {
    let odg = await req_json({"ra": "posts"}, "POST");
    let pom;
    posts_list.innerHTML = "";
    odg["posts"].forEach(function (v){
        pom = post_add.cloneNode(true);
        pom.children[0].dataset.post = v[0];
        pom.children[2].dataset.post = v[0];
        pom.children[1].value = v[0];
        if(v[1] == "1"){
            pom.children[2].style.display = "block";
        }

        posts_list.appendChild(pom);
    });
}
function ocistiPovrsinu(){
    editor.dataset.tren = "";
    pom = images.children[0].cloneNode(true);
    images.innerHTML = "";
    images.appendChild(pom);
    add_dugme = document.querySelector("#images_add_btn");
    if (!folded) {
        add_dugme.style.opacity = "1";
        add_dugme.style.display = "block";
    }
    prew.src = "static/images/insert-picture-icon.png";
    title.value = "";
    title.disabled = false;
    date.value = "";
    event_txt.value = "";
    lok_btn.value = "Pick a location";
    lok_btn.dataset.lok = "";
    lok_btn.dataset.cords = "";
    forms.selectedIndex = "0";
    dogs.selectedIndex = "0";
    window.localStorage.removeItem("post_lok");
    window.localStorage.removeItem("current_post")
}
async function popuniEditor(name){
    pom = await req_json({"ra": "lp", "n": name}, "POST");
    pom = JSON.parse(pom["data"]);
    editor.dataset.tren = window.localStorage.getItem("current_post");
    title.value = pom["head"];
    title.disabled = true;
    date.value = pom["date"]
    event_txt.value = pom["txt"];
    forms.value = pom["frm"];
    dogs.value = pom["type"];
    if(pom_kords.length == 0){
        lok_btn.dataset.lok = pom["lok"];
        lok_btn.value = pom["lok"];
        lok_btn.dataset.cords = pom["kords"];
    }else{
        if(pom_kords[0] != pom["lok"]){
            lok_btn.dataset.lok = pom_kords[0];
            lok_btn.value = pom_kords[0];
        }else{
            lok_btn.dataset.lok = pom["lok"];
            lok_btn.value = pom["lok"];
        }
        if(pom_kords[1] != pom["kords"]){
            lok_btn.dataset.cords = pom_kords[1];
        }else{
            lok_btn.dataset.cords = pom["kords"];
        }
    }    
    let img;
    img = images.children[0].cloneNode(true);
    images.innerHTML = "";
    images.appendChild(img);
    add_dugme = document.querySelector("#images_add_btn");
    pom["imgs"].forEach(function (v) {
        img = lil_img.cloneNode(true);
        img.src = v;
        images.appendChild(img);
    });
    dodeliDesniKlik();
    if (!folded) {
        for (let i = 1; i < images.children.length; i++) {
            images.children[i].classList.add("added_image_clicked");
        }
    }
    prew.src = "static/images/insert-picture-icon.png";
    return pom["kords"]
}
//#endregion functions

//#region event listeners
prew.onmousedown = function (e){
    if (e.which == 3) {        
        if (prew.src == default_image) {
            return;
        }
        dodeliDesniKlik();
        prew.src = "static/images/insert-picture-icon.png";
    }
}
file_upload.onchange = async function(e){
    if(title.value == ""){
        alert("You can't add images to post with no name");
        return;
    }
    let preskoceni = [];
    let pom;
    let slike = new FormData();
    for (let i = 0; i < file_upload.files.length; i++) {
        if(!file_upload.files[i].type.includes("image")){
            preskoceni.push(file_upload.files[i].name)
            continue;
        }
        slike.append("imgs", file_upload.files[i]);
    }
    kontekst.style.display = "none";
    loader.style.display = "flex";
    try {
        let odg = await fetch(url_stranice, {
            method: "PUT",
            body: slike,
        })
        .then((response) => {return response.json();})
        console.log(odg["msg"]);
        while (file_upload.length > 0) {
            file_upload.pop();
        }          
    } catch {
        kontekst.style.display = "flex";
        loader.style.display = "none";
        alert("A front-end error occured while trying to upload images")
        return;
    }
    slike.forEach(function (s){
        pom = lil_img.cloneNode(true);
        pom.classList.add("added_image_clicked");
        pom.src = "/static/event_images/" + s.name;
        images.appendChild(pom);
    })
    dodeliDesniKlik();
    kontekst.style.display = "flex";
    loader.style.display = "none";
    if(preskoceni.length != 0){
        pom = "";
        preskoceni.forEach(function (v){
            pom += "\n" + v;
        })
        alert("File upload finnished, these files were skipped because they are not images:\n" + pom);
    }
    await savePost();
}
image_box.addEventListener("contextmenu", function (e){
    e.preventDefault();
}, false);
images.addEventListener("contextmenu", function (e){
    e.preventDefault();
}, false);
posts.addEventListener("submit", async function(e){
    e.preventDefault();
    let pom;
    switch (e.submitter.dataset.fun) {
        case "post":
            kontekst.style.display = "none";
            loader.style.display = "flex";
            editor.dataset.tren = e.submitter.value;
            window.localStorage.setItem("current_post", e.submitter.value)
            if(e.submitter.parentNode.children[2].style.display == "block"){
                editor.dataset.pubed = "1";
            }else{
                editor.dataset.pubed = "0";
            }
            await popuniEditor(e.submitter.value);
            kontekst.style.display = "flex";
            loader.style.display = "none";
            return;
        case "delp":
            if(e.submitter.dataset.post == editor.dataset.tren){
                ocistiPovrsinu();    
            }
            pom = await req_json({"ra": "dlt", "post": e.submitter.dataset.post},"POST");
            await dajPostove();
            return;
        case "new":
            ocistiPovrsinu();
            return;
        case "unpubp":
            pom = await req_json({"ra": "unpub", "post": e.submitter.dataset.post, "kords": e.submitter.parentNode.dataset.kords},"POST");
            e.submitter.style.display = "none";
            editor.dataset.pubed = "0";
            alert(pom["msg"]);
            return;
        default:
            break;
    }
})
editor.addEventListener("submit", async function(e){
    e.preventDefault();
    let pom,odg;
    switch (e.submitter.dataset.fun) {
        case "fold":
            //animations when button is clicked
            img_btn.animate([
                {transform: 'translateY(0)',},
                {transform: 'translateY(3vh)'},
                {transform: 'translateY(0)',}
            ],
            {
                duration: 200,
                iterations: 1
            })
            if(folded){
                //promeni ove id-jeve da rade kao klase da bi ovo moglo lepse da se napise
                img_cont.style.height = "70%";
                event_txt.style.height = "10%";
                image_box.style.display = "inline-flex";
                image_box.style.opacity = "1";
                images.style.flexDirection = "column";
                images.style.width = "20%";
                images.style.overflowX = "hidden";
                images.style.overflowY = "auto";
                images.style.borderRight = "0.01vh solid var(--boja-tema)";
                add_dugme.style.opacity = "1";
                add_dugme.style.display = "block";
                for (let i = 1; i < images.children.length; i++) {
                    images.children[i].classList.add("added_image_clicked");
                }
            }else{
                img_cont.style.height = "20%";
                event_txt.style.height = "60%";
                image_box.style.display = "none";
                image_box.style.opacity = "0";
                images.style.flexDirection = "row";
                images.style.width = "100%";
                images.style.overflowX = "auto";
                images.style.overflowY = "hidden";
                images.style.borderRight = "none";
                add_dugme.style.opacity = "0";
                add_dugme.style.display = "none";
                for (let i = 1; i < images.children.length; i++) {
                    images.children[i].classList.remove("added_image_clicked");
                }
            }
            folded = !folded
            return;
        case "img":
            pom = e.submitter.src;
            if (prew.src != default_image) {                        
                e.submitter.src = prew.src;
            }            
            prew.src = pom;
            return;
        case "add_img":
            file_upload.click();
            return;
        case "save":
            await savePost();
            return;
        case "pub":
            if(editor.dataset.tren == ""){
                alert("No post was selected");
                return;
            }
            if(editor.dataset.pubed == "1"){
                alert("Post has already been published!");
                return;
            }
            odg = await req_json({"ra": "pub", "name": editor.dataset.tren}, "POST");
            await dajPostove();
            alert(odg["msg"]);            
            return;
        case "lok":
            window.localStorage.setItem("post_lok", "");
            window.localStorage.setItem("current_post", editor.dataset.tren);
            window.location.href = window.origin + "/map-editor";
            return;
        default:
            return;
    }
})
//#endregion event listeners

//#region functions that execute at the end of the load
dodeliDesniKlik();dajPostove();dajForme();

if(window.localStorage.getItem("post_lok")!=null && window.localStorage.getItem("post_lok")!=""){
    pom_kords = JSON.parse(window.localStorage.getItem("post_lok"));
    window.localStorage.removeItem("post_lok");
}
if(window.localStorage.getItem("current_post")!=null && window.localStorage.getItem("current_post")!=""){
    let pom = window.localStorage.getItem("current_post");
    popuniEditor(pom);
}
//#endregion functions that execute at the end of the load