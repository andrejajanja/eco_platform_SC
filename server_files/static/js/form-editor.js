//#region variables
const url_stranice = window.location.href;
const explorer = document.querySelector("#explorer");
let maker = document.querySelector("#maker");
let responces = document.querySelector("#responces-box");
let forme = document.querySelector("#past-forms");
let loader = document.querySelector("#loader");
let opisp = document.querySelector("#form-description-field");
let table = document.querySelector(".responces-table");
let copyFlds = document.querySelector("#copyFlds");
//templates
let templates = document.querySelector("#templates").content.cloneNode(true);
let polje_sample = templates.querySelector(".form-field");
let tipovi = templates.querySelector("#dropdown-list-edited-field");
let checkkutija = templates.querySelector(".checkbox-field");
let panel = templates.querySelector(".panel-for-checkboxes");
let form_file = templates.querySelector(".form-in-past-forms");
let checkbSelect = templates.querySelector(".checkboxes-select");
let checkbRow = templates.querySelector(".checkbRow");
let checkAll = templates.querySelector('[data-fun = "checkAll"]');
let uncheckAll = templates.querySelector('[data-fun = "uncheckAll"]');
let threeDots = templates.querySelector(".three-dots");
//let tableHeader = templates.querySelector(".tHeader");
let row = document.createElement("tr");
let field = document.createElement("td");

let frm_name = "";
let trenIndex = 0;
let pocetniIndex = 1;
let publs = {};
//#endregion variables

//#region funkcije
function updateSerial(){
    //napisi ovo malo elegantnije
    for(let i = 0; i<maker.children.length;i++){
        maker.children[i].i = i;
    }
}
function fokusirajMakerElement(e){
    let i = e.currentTarget.parentNode.parentNode.i;
    //dalja logika za dodavanje editora
    if(!(i==(maker.children.length-1)) && !(i<pocetniIndex)){
        //skini ceo editor sa polja koje je bilo pre
        if(trenIndex>0 && !(maker.children[trenIndex].children[0].children.length == 1)){
            try{
                maker.children[trenIndex].children[0].removeChild(maker.children[trenIndex].children[0].lastChild);
                maker.children[trenIndex].children[0].appendChild(threeDots.cloneNode());
                maker.children[trenIndex].children[0].children[1].addEventListener("click", fokusirajMakerElement,false);
                if(maker.children[trenIndex].dataset.type == "checkb"){
                    maker.children[trenIndex].children[1].removeChild(maker.children[trenIndex].children[1].lastChild);
                }   
            }catch{}  
        }
        //doodaj editor na trenutno polje
        maker.children[i].children[0].removeChild(maker.children[i].children[0].children[1]);
        maker.children[i].children[0].appendChild(tipovi.cloneNode(true));
        if(maker.children[i].dataset.type == "checkb"){
            maker.children[i].children[1].appendChild(panel.cloneNode(true))
        }
        maker.children[i].i = i;
    }
    trenIndex = i;
}
function bazdariTipPolja(index){
    let pom_polje = maker.children[index].cloneNode(true);
    let tip = pom_polje.dataset.type;
    pom_polje.replaceChild(pom_polje.children[1].cloneNode(false), pom_polje.children[1]);
    //komp kao komponenta
    if(tip == "sentc"){
        let komp = document.createElement("input");
        komp.className = "text-form-field";
        komp.type = "text"
        komp.name = "vr" + index;
        komp.placeholder = "Short text answer";
        komp.disabled = true;
        pom_polje.children[1].appendChild(komp);
        maker.replaceChild(pom_polje,maker.children[index]);
        maker.children[index].i = index;
        maker.children[index].children[1].className = "sentance-field-type";
        return;
    }

    if(tip == "parag"){
        let komp = document.createElement("textarea");
        komp.className = "paragraph-form-field";
        komp.name = "vr" + index;
        komp.value = "This is a field for paragraph input.";
        komp.disabled = true;
        pom_polje.children[1].appendChild(komp);
        maker.replaceChild(pom_polje,maker.children[index]);
        maker.children[index].i = index;
        maker.children[index].children[1].className = "paragraph-field-type";
        return;
    }

    if(tip == "checkb"){
        let kutija = checkkutija.cloneNode(true)
        let pom_panel = panel.cloneNode(true)

        kutija.children[0].name +=index + ".0";
        kutija.children[1].name +=index + ".0"; 

        pom_polje.children[1].append(kutija, pom_panel)
        maker.replaceChild(pom_polje,maker.children[index]);
        maker.children[index].children[1].className = "checkbox-field-type";
        maker.children[index].i = index;
        return;
    }

    if(tip == "date"){
        let komp = document.createElement("input");
        komp.className = "date-form-field";
        komp.type = "date"
        komp.name = "vr" + index;
        komp.disabled = true;
        pom_polje.children[1].appendChild(komp);
        maker.replaceChild(pom_polje,maker.children[index]);
        maker.children[index].i = index;
        maker.children[index].children[1].className = "date-field";
        return;
    }

    if(tip == "time"){
        let komp = document.createElement("input");
        komp.className = "time-form-field";
        komp.type = "time"
        komp.name = "vr" + index;
        komp.disabled = true;
        pom_polje.children[1].appendChild(komp);
        maker.replaceChild(pom_polje,maker.children[index]);
        maker.children[index].i = index;
        maker.children[index].children[1].className = "time-field";
        return;
    }
}
//puni "Past forms:"" kutiju sa prethodnno napravljenim formama
async function fillFormsExplorer(){
    let form_names = await req_json({ra: "load"}, "POST")
    let pom;
    forme.innerHTML = ""   
    publs = {};
    form_names["forms"].forEach(function (ime_forme, i){
        publs[ime_forme[0]] = ime_forme[1];
        pom = form_file.cloneNode(true);
        pom.dataset.file = ime_forme[0];
        pom.children[1].value = ime_forme[0];
        pom.children[2].style.display = "none";
        if(ime_forme[1] == true){
            pom.children[2].style.display = "block";
        }
        pom.dataset.postoji = ime_forme[1];
        pom.children[2].onmousedown = async function (e) {
            if (e.which == 3) {
                let odg = await req_json({"ra": "unpub", "form": ime_forme[0]}, "POST");
                publs[maker.children[0].children[0].value] = false;
                console.log(publs[maker.children[0].children[0].value]);
                pom.dataset.postoji = false;
                if(odg["msg"] == "1"){
                    forme.children[i].children[2].style.display = "none";
                }else{
                    alert("An Error occured while trying to unpublish form: " + ime_forme[0]);
                }
            }
        };
        forme.appendChild(pom);
    });
}
function new_form() {
    //code cisti sve sot je na forma povrsini;
    pomd = [maker.children[0], maker.children[maker.children.length-1]];
    maker.innerHTML = "";
    maker.appendChild(pomd[0]);
    maker.appendChild(polje_sample.cloneNode(true));
    maker.appendChild(pomd[1]);
    maker.children[0].children[0].value = "";
    maker.children[0].children[0].disabled = false;
    maker.children[0].children[1].children[1].value = "";
    maker.children[0].children[1].children[2].value = "";
    maker.children[0].children[2].value = "";
    maker.children[0].children[3].value = "";
    maker.children[1].addEventListener("click", fokusirajMakerElement, false);
    maker.children[1].i = 1;
    opisp.style.height = "5em";
}

//#endregion funkcije

//#region event listeners

forme.addEventListener("contextmenu", function (e){
    e.preventDefault();
}, false);

explorer.addEventListener("submit", async function(e){
    e.preventDefault()
    maker.style.display = "none";
    loader.style.display = "flex";
    responces.style.display = "none";
    let pomd,odg, di;
    switch (e.submitter.name) {
        case "file":
            odg = await req_json({"ra": "frm_meta", "form_name": e.submitter.parentNode.dataset.file}, "POST");
            di = JSON.parse(odg["form_data"]);

            //resetuje celu formu
            pomd = [maker.children[0], maker.children[maker.children.length-1]];
            maker.innerHTML = "";
            maker.appendChild(pomd[0]);
            maker.appendChild(pomd[1]);
            maker.children[0].children[0].value = di["file"];
            maker.children[0].children[0].disabled = true;
            maker.children[0].children[1].children[1].value = di["exp_date"];
            maker.children[0].children[1].children[2].value = di["exp_time"];
            maker.children[0].children[2].value = di["title"];
            maker.children[0].children[3].value = di["description"];

            //popunjavanje sacuvanih polja
            let pom;
            for (let i = 0; i < di["fields"].length; i++) {
                pom = polje_sample.cloneNode(true);
                pom.dataset.type = di["fields"][i]["type"];
                pom.children[0].children[0].value = di["fields"][i]["head"];
                maker.insertBefore(pom, maker.children[maker.children.length-1]);
                bazdariTipPolja(i+1);            
                if(maker.children[i+1].dataset.type == "checkb"){
                    let checkb;
                    maker.children[i+1].children[1].innerHTML = "";
                    di["fields"][i]["options"].forEach(function (v){
                        checkb = checkkutija.cloneNode(true);
                        checkb.children[1].value = v;
                        maker.children[i+1].children[1].appendChild(checkb);
                    })
                }
                //doodaj ovde da moze i checkb tip polja da bazdari kako valja, jer ovde ne ubacuje uopste
                maker.children[i+1].addEventListener("click", fokusirajMakerElement,false);
            }            
            autoResize();
            maker.style.display = "flex";
            loader.style.display = "none";
            responces.style.display = "none";
            break;
        case "new":
            new_form();
            maker.style.display = "flex";
            loader.style.display = "none";
            responces.style.display = "none";
            break;
        case "publish":
            if(publs[maker.children[0].children[0].value]){
                alert("Form is already published");
                maker.style.display = "flex";
                loader.style.display = "none";
                break;
            }

            if(maker.children[0].children[0].value == ""){
                alert("You didn't select any form");
                maker.style.display = "flex";
                loader.style.display = "none";
                break;
            }

            odg = await req_json({"ra": "pub", "pub_form": maker.children[0].children[0].value}, "POST");
            fillFormsExplorer();
            alert(odg["msg"]);
        
            maker.style.display = "flex";
            loader.style.display = "none";
            break;

        case "resp":
            let option, counter = 1;
            odg = await req_json({"ra": "frm_meta", "form_name": e.submitter.parentNode.dataset.file}, "POST");
            frm_name = e.submitter.parentNode.dataset.file;
            responces.children[0].children[0].innerHTML = "Responces for: " + e.submitter.parentNode.dataset.file;
            responces.children[1].innerHTML = "<p>Filter data:</p>";
            di = JSON.parse(odg["form_data"]);

            copyFlds.innerHTML = "";
            option = document.createElement("option");
            option.innerHTML = "Select column";
            option.value = 0;
            copyFlds.append(option);

            di["fields"].forEach(function (v, i){
                if(v["type"] == "checkb"){
                    pomd = checkbSelect.cloneNode();
                    option = document.createElement("option");
                    option.innerHTML = v["head"];
                    option.value = "0";
                    pomd.append(option);
                    v["options"].forEach(function (opt,j){
                        counter++;
                        option = document.createElement("option");
                        option.innerHTML = opt;
                        option.value = `KOL${i}_${j}`;
                        pomd.append(option);
                    });
                    responces.children[1].append(pomd);
                }else{
                    option = document.createElement("option");
                    option.innerHTML = v["head"];
                    option.value = counter;
                    copyFlds.append(option);
                    counter++;
                }
            })
            table.innerHTML = "";
            let pom1 = document.createElement("tr");
            let pom2 = document.createElement("tr");        
            let colLabel1 = document.createElement("th");
            let colLabel2 = document.createElement("th");
            colLabel1.colSpan = 1;
            colLabel2.append(checkAll.cloneNode());
            colLabel2.append(uncheckAll.cloneNode());
            colLabel2.colSpan = 1;
            pom1.append(colLabel1);
            pom2.append(colLabel2);
            di["fields"].forEach(function (fld) {
                colLabel1 = document.createElement("th");
                colLabel2 = document.createElement("th");
                if (fld["type"] == "checkb") {
                    colLabel1.innerHTML = fld["head"];
                    colLabel1.colSpan = fld["options"].length;
                    colLabel1.className = "checkboxes-table-header";
                    pom1.append(colLabel1);
                    fld["options"].forEach(function (opc) {
                        colLabel2 = document.createElement("th");
                        colLabel2.innerHTML = opc;
                        colLabel2.colSpan = 1;
                        pom2.append(colLabel2);
                    })
                } else {
                    colLabel1.colSpan = 1;
                    colLabel2.innerHTML = fld["head"];
                    colLabel2.colSpan = 1;
                    pom1.append(colLabel1);
                    pom2.append(colLabel2);
                }
                
            })
            table.append(pom1);
            table.append(pom2);
            
            loader.style.display = "none";
            responces.style.display = "flex";
            break;

        case "del":
            odg = await req_json({"ra": "dlt", "form": e.submitter.parentNode.dataset.file, "pub": publs[e.submitter.parentNode.dataset.file]}, "POST");
            await fillFormsExplorer();
            new_form();
            alert(odg["msg"])
            maker.style.display = "flex";
            loader.style.display = "none";
            responces.style.display = "none";
            break;
        default:
            break;
    }
},false)

//svaki submit u celoj maker formi
maker.addEventListener("submit", async function(e){
    e.preventDefault();
    let pomocna;
    let func = e.submitter.dataset.fun;
    switch (func) {
        //#region funkcionalnost za panel za dodavanje, oduzimanje i cuvanje polja;
        case "add_fld":
            let duzina = maker.children.length;
            let pom_fld = polje_sample.cloneNode(true);
            pom_fld.children[0].children[0].name = "na" + (duzina-pocetniIndex-1);
            maker.insertBefore(pom_fld, maker.children[duzina-1]);
            maker.children[duzina-1].children[0].children[1].addEventListener("click", fokusirajMakerElement);
            updateSerial();
            break;
        case "sub_fld":
            if(maker.children.length == (pocetniIndex+2)){
                console.error("There are no more fields that can be deleted");
                return;
            }
            maker.removeChild(maker.children[maker.children.length-2])
            updateSerial();
            break;
        case "save_all":
            let pom_dete, data = {};
            //PROVERA DA LI SME DA SE SACUVA NOVA FORMA POD TIM FILE IMENOM!!!!!!

            //header forme
            pom_dete = maker.children[0].cloneNode(true);
            data["file"] = pom_dete.children[0].value.toLowerCase().replace(" ", "_");
            data["exp_date"] = pom_dete.children[1].children[1].value;
            data["exp_time"] = pom_dete.children[1].children[2].value;
            data["title"] = pom_dete.children[2].value;
            data["description"] = pom_dete.children[3].value;
            let polja = [];
            //pojedinacna polja
            for(let i = 1; i<maker.children.length-1;i++){
                pom_dete = maker.children[i].cloneNode(true);
                let tip = pom_dete.dataset.type;                
                if(tip == "idk" || tip == undefined){
                    //doodaj da obavestava korisnika i obelezava gde nema
                    console.log("Field type unknown, skipping field");
                    continue;
                }

                let field_head = pom_dete.children[0].children[0].value;
                if(field_head==""){
                    //napravi da se highlightuje polje ciji naslov nije unet
                    console.log("Field title unknown, skipping field");
                    continue;
                }

                if(tip == "checkb"){
                    //opc su sve opcije u samom polju, mult je da li moze vise kutija da se klikne odjednom
                    let opc = [], mult = 1;
                    pom_dete = pom_dete.children[1];
                    if(pom_dete.children[pom_dete.children.length-1].className == "panel-for-checkboxes"){
                        pomocna = pom_dete.children.length-1;
                    }else{
                        pomocna = pom_dete.children.length;
                    }

                    
                    for (let j = 0; j < pomocna; j++) {
                        opc.push(pom_dete.children[j].children[1].value);                        
                    }
                    polja.push({"type": "checkb", "head": field_head, "options": opc, "multiple": mult});
                    continue;
                }
                polja.push({"type": tip, "head": field_head});
            }
            data["fields"] = polja;

            //optimizuj da ovde salje ime pod kojim fajl treba da bude upisan, da ne bi morao da ga raspakuje pa pakuje opet
            let odg = await req_json({"ra": "svd", "data": JSON.stringify(data)},"POST");
            if(odg["msg"] == "1"){
                await fillFormsExplorer();
            }else{                
                alert("Server error while saving a form");
            }
            break;
        //#endregion funkcionalnost za panel za dodavanje, oduzimanje i cuvanje polja;
        
        //#region panel za dodavanje i oduzimanje konkretnih checkboxova u polju
        case "add_checkb":
            pomocna = maker.children[trenIndex].cloneNode(true);
            pomocna.children[1].insertBefore(checkkutija.cloneNode(true),pomocna.children[1].lastChild);
            maker.replaceChild(pomocna,maker.children[trenIndex]);
            maker.children[trenIndex].i = trenIndex;
            break;
        case "sub_checkb":
            pomocna = maker.children[trenIndex].cloneNode(true);
            let duzinica = pomocna.children[1].children.length;
            if(duzinica == 1){
                console.error("There are no more checkboxes that can be deleted");
                break;
            }
            pomocna.children[1].removeChild(pomocna.children[1].children[duzinica-2]);
            maker.replaceChild(pomocna,maker.children[trenIndex]);
            maker.children[trenIndex].i = trenIndex;
            break;
        //#endregion panel za dodavanje i oduzimanje konkretnih checkboxova u polju
        default:
            break;
    }
},false)

maker.addEventListener("input", function(e){
    e.preventDefault();
    if(e.target.dataset.fun == "select"){
        maker.children[trenIndex].dataset.type = e.target.value;
        bazdariTipPolja(trenIndex);
    }
},false)

opisp.addEventListener('input', autoResize, false)
function autoResize() {
    //zavrsi da ovo radi kada se  forma ucitava
    opisp.style.height = 'auto';
    opisp.style.height = (opisp.scrollHeight+20) + 'px';
}

responces.addEventListener("submit", async function (e) {
    e.preventDefault();
    let pom, odg, childs, trow;
    switch (e.submitter.dataset.fun) {
        case "fetch":
            //ovde mozda loader da se stavi kad dobavlja podatke
            let data = {"conds": []};
            for (let i = 1; i < responces.children[1].children.length; i++) {
                if (responces.children[1].children[i].value != "0") {
                    data["conds"].push(responces.children[1].children[i].value);
                }
            }
            //ovo ne sljaka, samo obrisi podatke iz forme, posle 3. reda (deteta broj 2)
            while (table.children.length > 2){
                table.removeChild(table.children[2])
            }
            //pomeri ovo u deo kada ucitava samu formu
            //filling the table header
            //filling the forms of a row
            odg = await req_json({"ra": "get_data", "data": JSON.stringify(data), "frm": frm_name}, "POST");
            pom = JSON.parse(odg["data"]);
            let tableRow, cell;
            pom.forEach(function (sqlRow){
                tableRow = row.cloneNode(true);
                cell = field.cloneNode(true);
                cell.append(checkbRow.cloneNode());
                tableRow.append(cell);
                sqlRow.shift();
                sqlRow.forEach(function (element){
                    cell = field.cloneNode(true);
                    cell.innerHTML = element;
                    tableRow.append(cell);
                })
                table.append(tableRow);
            })  
            return;
        case "copy":
            if(copyFlds.value == 0){
                alert("You must select a column in order to copt values from it.");
            }
            let clip = ""
            childs = table.children;
            trow;
            for (let i = 2; i < childs.length; i++) {
                trow = childs[i];                
                if(trow.children[0].children[0].checked){
                    clip += trow.children[copyFlds.value].innerHTML + " ";
                }
            }
            navigator.clipboard.writeText(clip);
            alert("Selected fields copied to clipboard.");
            return;
        case "checkAll":
            childs = table.children;            
            for (let i = 2; i < childs.length; i++) {
                trow = childs[i];
                trow.children[0].children[0].checked = true;
            }
            return;            
        case "uncheckAll":
            childs = table.children;            
            for (let i = 2; i < childs.length; i++) {
                trow = childs[i];
                trow.children[0].children[0].checked = false;
            }
            return;
        default:
            break;
    }
    // let podaci = JSON.parse(odg["data"]);
    // podaci.forEach(function (red_sql){
    //     pomd = red.cloneNode(true);
    //     red_sql.forEach(function (p){
    //         po = field.cloneNode(true);
    //         po.innerHTML = p;
    //         pomd.appendChild(po);
    //     });
    //     responces.appendChild(pomd);                
    // });            
})

//#endregion event listeners

//#region funkcije koje se izvrsavaju posthumno

fillFormsExplorer();
for(let i = pocetniIndex; i<maker.children.length-1;i++){
    maker.children[i].children[0].children[1].addEventListener("click", fokusirajMakerElement,false);
    maker.children[i].i = i;
}
//#endregion funkcije koje se izvrsavaju posthumno