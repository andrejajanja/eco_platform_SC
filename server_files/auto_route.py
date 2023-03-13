#skripta koja pravi novu rutu za ceo server ukljucujuci i neophodne fajlove
import sys,os
status = 1
try:
    if sys.argv[1] == "--help":
        print("andreja@janja.xyz ako ne mozete da se snadjete")
        status = 0
except:
    print("Niste uneli nikakav argument")
    status = 0
if status == 0:
    exit()

try:
    ime_rute, akcija = sys.argv[1],sys.argv[2]
except:
    print("NISTE DALI DOVOLJAN BROJ ARGUMENATA, MORA 2")
    status = 0

if status == 0:
    exit()

#case kada brise rutu
if akcija == "0":
    try:
        tren_srv =""
        with open("server_files/server.py", mode="r") as f:
            tren_srv = f.read()
            
        novi = tren_srv[:tren_srv.find("placeholder-start")] + "placeholder-start\n\n#" + tren_srv[tren_srv.find("placeholder-end"):]

        with open("server_files/server.py", mode="w", encoding="UTF-8") as f:
            f.write(novi)

        os.remove(f"server_files/static/styles/{ime_rute}.css")
        os.remove(f"server_files/templates/{ime_rute}.html")
        os.remove(f"server_files/static/js/{ime_rute}.js")
        print("\nObrisite rucno samo jos code za rutu u server.py file_u, ukoliko ga niste izmestali iz odgovorajuce rute\n")
    except:
        print("\nRuta ne moze biti obrisana jer je nema\n")
    exit()

html = f'''<!DOCTYPE html lang = "en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{ime_rute} • The Environmental Team</title>
        <link rel="icon" href="/static/images/light-bulb.png" type="image/x-icon"/>
        <script type = "text/javascript" src='/static/js/lib.js'></script>
        <script defer type="text/javascript" src='/static/js/{ime_rute}.js'></script>
        <link rel="stylesheet" type="text/css" href='/static/styles/head_style.css'>
        <link rel="stylesheet" type="text/css" href='/static/styles/{ime_rute}.css'>
    </head>
    <body>
        <div id = "header">
            <h1 id = "naslov">The Environmental Team</h1>
            <div id = "stranice">
                <a class = "dugme_head" href = "/events">Events</a>
                <a class = "dugme_head" href = "/map">Map</a>
                <a class = "dugme_head" href = "/about-us">About Us</a>
            </div>
        </div>
        <div id = "kontekst">

        </div>
        <div id = "footer">
            <p>Made by Andreja Janković, 2023, andrejajanja@gmail.com</p>
        </div>
    </body>
</html>'''
css = ''''''
js = '''const url_stranice = window.location.href;\n\n\n'''

server = f'''placeholder-start\n@app.route('/{ime_rute}', methods = ["GET", "POST"])
def {ime_rute}_route():
    if request.method == "POST":
        return "sdsad"
    if request.method == "GET":
        return render_template("{ime_rute}.html")\n\n#'''

tren_srv =""
with open("server_files/server.py", mode="r") as f:
    tren_srv = f.read()

novi = tren_srv[:tren_srv.find("placeholder-start")] + server + tren_srv[tren_srv.find("placeholder-end"):]

with open("server_files/server.py", mode="w", encoding="UTF-8") as f:
    f.write(novi)
with open(f"server_files/static/styles/{ime_rute}.css", mode="w", encoding="UTF-8") as f:
    f.write(css)
with open(f"server_files/templates/{ime_rute}.html", mode="w", encoding="UTF-8") as f:
    f.write(html)
with open(f"server_files/static/js/{ime_rute}.js", mode="w", encoding="UTF-8") as f:
    f.write(js)

print("\nUspesno kreirana nova ruta\n")