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

html =f'''<!DOCTYPE html lang = "en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{ime_rute} • The Environmental Team</title>
        <link rel="icon" href="/static/images/logo.png" type="image/x-icon"/>
        <script defer type="text/javascript" src='/static/js/{ime_rute}.js'></script>
        <link rel="stylesheet" type="text/css" href='/static/styles/head-style.css'>
        <link rel="stylesheet" type="text/css" href='/static/styles/{ime_rute}.css'>
    </head>
    <body>
        <nav class="green-border-navbar green-fill-navbar navbar">
            <a href="/">
                <img class="navbar-left" src="/static/images/logo.png"/>
            </a>
            <ul class="navbar-middle">
                <li>
                    <a href="/events">
                        Events
                    </a>
                </li>
                <li>
                    <a href="/map">
                        Map
                    </a>
                </li>
                <li>
                    <a href="/contact-us">
                        Contact us
                    </a>
                </li>
                <li>
                    <a href="/about-us">
                        About us
                    </a>
                </li>
            </ul>
            <div class="navbar-right">
                {{%include loged_in %}}
            </div>
        </nav>
        <div class = "context">
        </div>
        <div class="footer green-fill">
            <div class="row space-between">
                <div class="about-grid">
                    <div class="graphic-logo">
                        <img src="/static/images/logo.png" width="200" height="200" alt="Logo">
                    </div>
                    <div class="text-logo">
                        The Environmental Team
                    </div>                    
                    <div class="empty"></div> <!-- empty div just used to form nice-looking grid -->
                    <div class="description">
                        Insert some slogan or moto here
                    </div>
                </div>
                <div class="nav-grid">
                    <div class="nav-link"><a href="/events">events</a></div>
                    <div class="nav-link"><a href="/map">map</a></div>
                    <div class="nav-link"><a href="/contact-us">contact us</a></div>
                    <div class="nav-link"><a href="/about-us">about us</a></div>
                </div>
            </div>
            <div class="row center">
                <div class="authors">
                    Made by Andreja Janković, andrejajanja@gmail.com, Year 2023
                </div>
            </div>
        </div>
    </body>
</html>'''

css = '''.context{

}
'''
js = '''const url_stranice = window.location.href;\n'''

server = f'''placeholder-start\n@app.route('/{ime_rute}', methods = ["GET", "POST"])
def {ime_rute}_route():
    if request.method == "POST":
        return "This route doesn't have any reponces for the POST request at the moment"
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