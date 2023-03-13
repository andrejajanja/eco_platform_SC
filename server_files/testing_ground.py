from lib import file_to_dict
import bs4

def dict_u_html(di: dict, default_path: str, default_file: str) -> None:
    #otvara pocetni fajl
    soup = ""
    formatter = bs4.formatter.HTMLFormatter(indent=4)
    with open(default_file, mode="r", encoding="UTF-8") as fp:
        soup = bs4.BeautifulSoup(fp.read(), features="html.parser")

    soup.head.title.string = f"The Environmental Team • {di['title']}"

    forma = soup.find("form", attrs={"id": "kontekst"})

    #making a header

    forma["data-time"] = f'''{di["exp_date"].replace("-", " ")} {di["exp_time"].replace(":", " ")}'''
    forma["data-frm"] = di["file"]
    forma.input["value"] = di["title"]
    forma.textarea.string = di["description"]

    #filling in fields
    for item in di["fields"]: #vidi da li ovde treba da se doda imena na svako polje
        pom = bs4.BeautifulSoup('''<div class = "polje">
            <p class = "fld_head"></p>
        </div>''', features="html.parser")

        if item["type"] == "sentc":
            pom.p.string = item["head"]
            inp = pom.new_tag("input")
            inp["class"] = "txt_in"
            inp["value"] = ""
            inp["type"] = "text"
            pom.div.append(inp)
            forma.insert(len(forma)-2, pom)
            continue

        if item["type"] == "parag":
            pom.p.string = item["head"]
            inp = pom.new_tag("textarea")
            inp["class"] = "parag_in"        
            pom.div.append(inp)
            forma.insert(len(forma)-2, pom)
            continue

        if item["type"] == "checkb":
            pom.p.string = item["head"]
            for opc in item["options"]:
                kutija = bs4.BeautifulSoup('''<div class = "checkbox_polje">
                    <input type="checkbox" class = "checkb_in">
                    <p class = "checkp_in"></p>
                </div>''',features="html.parser")
                kutija.p.string = opc
                pom.div.append(kutija)
            forma.insert(len(forma)-2, pom)
            continue

        if item["type"] == "date":
            pom.p.string = item["head"]
            inp = pom.new_tag("input")
            inp["class"] = "date_in"
            inp["type"] = "date"
            pom.div.append(inp)
            forma.insert(len(forma)-2, pom)
            continue

        if item["type"] == "time":
            pom.p.string = item["head"]
            inp = pom.new_tag("input")
            inp["class"] = "time_in"
            inp["type"] = "time"
            pom.div.append(inp)
            forma.insert(len(forma)-2, pom)

    with open(f"{default_path}{di['file']}.html", mode="w", encoding="UTF-8") as fp:
        fp.write(soup.prettify(formatter=formatter))

di = file_to_dict("server_files/server_data/form_layouts/form_name.json")
dict_u_html(di, "server_files/templates/forms/", "server_files/templates/form_layout.html")