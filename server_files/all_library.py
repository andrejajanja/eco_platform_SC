import random,string,json,bs4,pyodbc
from pyodbc import connect

#Classes
class User_log:
    def __init__(self, data) -> None:
        if data == []:
            self.status = False
            return None
        self.status = True
        data = data[0]
        self.email = data[1]
        self.password = data[2]

    def __str__(self) -> str:
        return f"User_log: {self.email} {self.password}"
        
class User:
    def __init__(self, data) -> None:
        if data == []:
            self.status = False
            return None
        self.status = True
        data = data[0]
        self.id = data[0]
        self.email = data[1]
        self.ime = data[2]
        self.prezime = data[3]
        self.grad = data[4]

    def jsonify(self):
        return json.dumps(self)
    

    def __str__(self) -> str:
        if self.status:
            return f"{self.id} {self.email} {self.ime} {self.prezime} {self.grad}"
        else:
            return "Empty Object"

class SQLConnector:
    '''
    Class description:
    ------
    Napisi ovo nekad
    
    Constructor arguments
    ------
    conn_str - str - connection string required to connect to the sql server
    Method list:
    ------
    executr_query
    
    '''
    def __init__(self, conn_str: str) -> None:
        self.con = pyodbc.connect(conn_str)
    
    def execute_query(self,query: str, commit: bool):
        '''
        Description:
        ------
        Takes query as a string and execute it against a certain database
        
        Input params:
        ------
        query - str - query to be executed against a certain table
        commit - boolean - True is used when query is INSERT INTO based ,False is used when query is SELECT based
        
        Output:
        ------
        True if commit was True, and query executed successfuly was successful, or the error massage sent by the server\n
        Data fetched from the database if commit was false
        '''
        kurs = self.con.cursor()
        try:
            kurs.execute(query)
            if(commit):
                self.con.commit()
                return True                
            else:
                return kurs.fetchall()
        except Exception as e:
            return e.args

    def __str__(self) -> str:
        return "This is an instance of SQLConnector class"

#Functions
def random_string(n: int):
    '''
    Description:
    ------
    Creates a string of random chracters of lenght x
    
    Input params:
    ------
    x - int
    
    Output:
    ------
    s - str - string of random characters
    '''
    return "".join(random.choice(string.ascii_letters) for i in range(n))

def execute_select_sql(query: str) -> list:
    pom = []
    konekcija = connect(r"Driver={ODBC Driver 17 for SQL Server};Server=localhost\SQLEXPRESS;Database=EKO;Trusted_Connection=yes;")
    k = konekcija.cursor()
    #SQL INJECTION HAZARD WITH THIS KIND OF QUERY
    r = k.execute(query)
    pom = r.fetchall()
    konekcija.close()   
    return pom

def dict_to_file(di: dict, file_path: str) -> None:
    '''
    Description:
    ------
    Puts dictinary into .json file
    
    Input params:
    ------
    di - dict - dictionary to be put into file
    file_path - str - path to the file in which dictionary will be stored
    Output:
    ------
    None
    
    '''
    if ".json" not in file_path:
        raise Exception("File path you provided doesn't have .json extention, errors may occur")
    with open(file_path, "w+") as fp:
        json.dump(di,fp,indent=4)

def file_to_dict(file_path: str) -> dict:
    '''
    Description:
    ------
    Takes name of the json file and loads it into dictionary object
    
    Input params:
    ------
    file_path - str - path to .json file
    
    Output:
    ------
    di - dict - dictionary reconstructed from the file
    
    '''

    if ".json" not in file_path:
        raise Exception("File path you provided doesn't have .json extention, errors may occur")

    di = {}
    with open(file_path, "r",encoding="UTF-8") as fp:
        di = json.loads(fp.read())
    return di

def create_table_from_dict(di):
    kolone = ""
    for i,p in enumerate(di["fields"]):
        pom = ""
        if p["type"] == "sentc":
            pom = f"\tKOL{i} varchar(100) NOT NULL,\n"

        if p["type"] == "parag":
            pom = f"\tKOL{i} varchar(3000) NOT NULL,\n"

        if p["type"] == "checkb":
            for j,o in enumerate(p["options"]):
                pom += f"\tKOL{i}_{j} BIT NOT NULL,\n"

        if p["type"] == "date":
            pom = f"\tKOL{i} DATE NOT NULL,\n"

        if p["type"] == "time":
            pom = f"\tKOL{i} TIME NOT NULL,\n"
        kolone += pom
    return f'''CREATE TABLE {di["file"]} (
        ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    {kolone});'''

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

def insert_into(table, data):
    pom = ""
    for v in data.split("`"):
        pom += f"'{v}',"
    kom = f'''INSERT INTO {table} VALUES ({pom[:-1]});'''
    return kom

def generate_post_from_dict(di, file: str, default_file: str, default_path: str) -> None:
    slike_ln = len(di["imgs"])
    soup = ""
    with open(default_file, mode="r", encoding="UTF-8") as fp:
        soup = bs4.BeautifulSoup(fp.read(), features="html.parser")
    soup.head.title.string = f"{di['head']} • The Environmental Team"
    cont = soup.find("div", attrs={"id": "kontekst"})

    pomd = ""
    for x in di["date"].split("-")[::-1]:
        pomd += f"{x}."

    frmLink = ""
    if di["frm"] != "":
        frmLink = f'''<a id = "frmLnk" href = "/forms/{di["frm"]}">Join us by filling out this form!</a>'''

    cont.append(f'''<div id ="postHeader">
            <img id = "typeImg" src ="/static/images/{di["type"]}.png">
            <h1 id = "ttl">{di['head']}</h1>
            <div id = "location">
                <img src = "/static/images/location.png">
                <a onclick = "clickLink('{di["head"]}')" title = "Click here to see the location" rel = "next" target = "_blank" href = "/map">{di["lok"]}</a>
            </div>
            <div id = "time">
                <img src = "/static/images/calendar.png">
                <p>{pomd}</p>
            </div>              
            {frmLink}
        </div> ''')

    for i, paragraf in enumerate(di["txt"].split("\n")):
        cont.append(f'''<p class = "postParag">{paragraf}</p>''')
        if i < slike_ln:
            cont.append(f'''<img class = "postImg" src = "/{di["imgs"][i][di["imgs"][i].find("static"):]}">''')

    formatter = bs4.formatter.HTMLFormatter(indent=4)
    with open(f"{default_path}{file}.html", mode="w", encoding="UTF-8") as fp:
        fp.write(soup.prettify(formatter=formatter))

def generate_events_page(di: dict, file: str)->None:
    with open(file, mode="r", encoding="UTF-8") as fp:
        soup = bs4.BeautifulSoup(fp.read(), features="html.parser")
    cont = soup.find("div", attrs={"id": "kontekst"})
    date = ""
    for x in di['date'].split("-")[::-1]:
        date += f"{x}."
    cont.insert(0, f'''<a href="/events/{di['head'].lower().replace(" ", "-")}" target="_self" rel="next" class="event">
                <img src="/static/images/{di['type']}.png" class="event_img">
                <h1 class="event_ttl">{di['head']}</h1>
                <img src="/static/images/location.png" class="event_img">
                <p class = "event_txt">{di['lok']}</p>
                <img src="/static/images/calendar.png" class="event_img">
                <p class = "event_txt">{date}</p>
        </a>''')

    formatter = bs4.formatter.HTMLFormatter(indent=4)
    with open(file, mode="w", encoding="UTF-8") as fp:
        fp.write(soup.prettify(formatter=formatter))

def regenerate_events_page(page_name: str, file: str):
    with open(file, mode="r", encoding="UTF-8") as fp:
        soup = bs4.BeautifulSoup(fp.read(), features="html.parser")
    cont = soup.find("div", attrs={"id": "kontekst"})
    for i,post in enumerate(cont):
        
        if type(post) == bs4.element.NavigableString:
            continue
        if post["href"][8:] == page_name:
            post.decompose()
    formatter = bs4.formatter.HTMLFormatter(indent=4)
    with open(file, mode="w", encoding="UTF-8") as fp:
        fp.write(soup.prettify(formatter=formatter))

def format_date(date):
    d = ""
    date = date.split("-")[::-1]
    for x in date:
        d += f"{x}."
    return d
