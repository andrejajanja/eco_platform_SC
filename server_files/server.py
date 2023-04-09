import redis,os,json,sqlite3
from datetime import datetime
from all_library import (User, User_log, random_string,
                    dict_to_file,SQLConnector, create_table_from_dict,file_to_dict,
                    dict_u_html, insert_into, generate_post_from_dict, generate_events_page, generate_main_page,
                    regenerate_events_page, format_date, regenerate_main_page)
from flask import (Flask, jsonify, make_response, redirect, render_template,
                   request)
from waitress import serve
from paste.translogger import TransLogger
print("Imported modules")
root = ""
#root = "/root/eco_platform_SC/"
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
print("Initialized server")

#server specific variables -- this can go to the json file
cookie_dur = 3600 #seconds

#Databases
session_driver = redis.Redis(host = "127.0.0.1", port = "6379", db=0) #db = 0 - session cookies
print("Connected to redis")
kon = SQLConnector(f"{root}EKO.db", root)
print("Loaded and connected to SQL db")

forms_folder = f"{root}server_files/server_data/form_layouts/"
images_folder = f"{root}server_files/static/event_images/"
event_posts = f"{root}server_files/server_data/event_posts/"

active_forms, active_posts, = [],[]
for frm in os.listdir(f"{root}server_files/templates/forms/"):
    active_forms.append(frm[:-5])

for post in os.listdir(f"{root}server_files/templates/event/"):
    active_posts.append(post[:-5])

active_locations, event_locations = list(file_to_dict(f"{root}server_files/server_data/locations.json")), file_to_dict(f"{root}server_files/server_data/savedLocations.json")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods = ["GET", "POST"])
def default():
    if request.method == "GET":
        try:
            if session_driver.exists(request.cookies["session_id"]) == 1:                
                return render_template("main.html", loged_in = "inserted_html/loged.html")
        except:
            pass
        return render_template("main.html", loged_in = "inserted_html/sign_in_html.html")

@app.route('/login', methods = ["GET", "POST"])
def logging_in():
    if request.method == "POST":
        form_data = dict(request.form)

        try:
            pr =  form_data["ra"]
        except KeyError:
            return jsonify({"msg": "Invalid post request for this route"})

        if form_data["ra"] == "log":
            pom = ""
            try:
                koris = User_log(kon.execute_query(f'''SELECT * from Ids where email = '{form_data["us"]}';''', False))
                if koris.status and koris.password == form_data["ps"]:
                        id_korisnika = kon.execute_query(f'''SELECT id from Users where email = '{form_data["us"]}';''', False)[0][0]
                        odgovor = make_response(jsonify({"status": 1}))
                        rnd_str = random_string(8)
                        odgovor.set_cookie("session_id", rnd_str, max_age=cookie_dur)
                        session_driver.set(rnd_str,id_korisnika, cookie_dur)
                        return odgovor
                else:
                    pom = "Wrong email/password"
            except Exception as e:
                print(e)
                pom = "Server error occured while you tried to sign in"
            return make_response(jsonify({"status": 0,"message":pom}))
        return jsonify({"Error": "Procedure not found"})
    if request.method == "GET":
        try:
            if session_driver.exists(request.cookies["session_id"]) == 1:
                return redirect("user")
            else:
                return render_template("login_d.html")
        except:
            return render_template("login_d.html")
    return jsonify({"Error": "Server didn't accept that request type"})

@app.route('/logout', methods = ["GET"])
def logout_route():
    try:
        coockie_id = request.cookies["session_id"]
    except:
        return jsonify({"msg": "Invalid request for this route"})
    session_driver.delete(coockie_id)
    res = make_response(redirect("/"))
    res.set_cookie("session_id", "", max_age=0)
    return res

@app.route('/user', methods = ["GET", "POST"])
def profile_page():
    try:
        if session_driver.exists(request.cookies["session_id"]) != 1:
            return redirect("/login")            
    except:
        return redirect("/login")

    if request.method == "POST":
        try:
            pr =  request.form["ra"]
        except KeyError:
            return jsonify({"msg": "Invalid post request for this route"})

    if request.method == "GET":
        try:
            key = session_driver.get(request.cookies['session_id']).decode()
        except:
            return redirect("/login")
        korisnik = User(kon.execute_query(f"select * from Users where id = {key};", False))
        return render_template("user_d.html", email = korisnik.email, ime = korisnik.ime, prezime = korisnik.prezime, grad = korisnik.grad)
    return jsonify({"Error": "Server didn't accept that request type"})

#FINNISH FORGOT PASSWORD

@app.route('/forms-editor', methods = ["GET", "POST"])
def makeform_route():
    try:
        if session_driver.exists(request.cookies["session_id"]) != 1:
            return redirect("/login")            
    except:
        return redirect("/login")
        
    if request.method == "POST":
        try:
            pr =  request.form["ra"]
        except KeyError:
            return jsonify({"msg": "Invalid post request for this route"})

        if request.form["ra"] == "svd":
            try:
                forma = json.loads(request.form["data"])
                dict_to_file(forma, f"{forms_folder}{forma['file']}.json")
                return jsonify({"msg": "1"})
            except:
                return jsonify({"msg": "0"})
            
        if request.form["ra"] == "dlt":
            try:
                if request.form["pub"] == "true":
                    os.remove(f"{root}server_files/templates/forms/{request.form['form']}.html")
                    rez = kon.execute_query(f"DROP TABLE {request.form['form']};", True)
                    active_forms.remove(request.form['form'])
                    if rez != True:
                        return jsonify({"msg": "A database error occured while deleting the form, please contact the developers"})
                os.remove(f"{forms_folder}{request.form['form']}.json")
                return jsonify({"msg":"Form successfully deleted"})
            except KeyError:
                return jsonify({"msg": "Invalid post request for this function"})
        
        if request.form["ra"] == "get_data":
            data = json.loads(request.form["data"]) 
            query = f"select * from {request.form['frm']}"
            if data["conds"] != []:
                where = " where"
                for fld in data["conds"]:
                    where += f''' {fld} = 'true' and'''
                query += f"{where};"
            rez = [tuple(r) for r in kon.execute_query(query.replace(" and;", ";"), False)]
            return jsonify({"data": json.dumps(rez, default=str)})
        
        if request.form["ra"] == "load":
            forme_u_bazi = [x[0] for x in kon.execute_query("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';", False)]
            imena_formi = [x[:-5] for x in os.listdir(forms_folder)]
            salje = []
            for fr in imena_formi:
                pom = False
                if fr in forme_u_bazi:
                    pom = True
                salje.append((fr, pom))
            return jsonify({"forms": salje})

        if request.form["ra"] == "frm_meta":
            ime = request.form["form_name"]
            respo = ""
            with open(f"{forms_folder}{ime}.json") as fp:
                respo = fp.read()
            return jsonify({"form_data": respo})

        if request.form["ra"] == "pub":
            active_forms.append(request.form["pub_form"])
            di = file_to_dict(f"{forms_folder}{request.form['pub_form']}.json")
            dict_u_html(di, f"{root}server_files/templates/forms/", f"{root}server_files/templates/form_layout.html")
            query = create_table_from_dict(di)
            rez = kon.execute_query(query, True)
            if rez == True:
                return jsonify({"msg": "successfully published a form"})
            else:
                return jsonify({"msg": "An Error occured while publishing the form, please contact the developers"})

        if request.form["ra"] == "unpub":
            try:
                os.remove(f"{root}server_files/templates/forms/{request.form['form']}.html")
                rez = kon.execute_query(f"DROP TABLE {request.form['form']};", True)
                active_forms.remove(request.form['form'])
                if rez != True:
                    raise Exception("Database Error")
                return jsonify({"msg": "1"})
            except Exception as e:
                print(e)
                return jsonify({"msg": "0"})
            
        if request.form["ra"] == "respo":
            tabela = [tuple(red) for red in kon.execute_query(f"select * from {request.form['form']};",False)]
            return jsonify({"s": "vratio odg", "data": json.dumps(tabela,default=str)})

        return jsonify({"msg": "responce of a POST request, there wasn't any function specific return"})
    if request.method == "GET":
        return render_template("form-editor.html")

@app.route('/forms/<frm>', methods = ["GET", "POST"])
def forms_route(frm):
    if request.method == "POST":
        try:
            pr,im =  request.form["form"], request.form["data"]
        except KeyError:
            return jsonify({"msg": "Invalid post request for this route"})
        try:        
            que = insert_into(request.form["form"],request.form['data'][:-1])
            pom = kon.execute_query(que, True) #SQL INJECTION HAZARD
            if pom == True: 
                return jsonify({"msg": "You successfully submited Your form responce."})
            else:
                with open(f"{root}server_files/server_errors/sql_server_related.txt", "a", encoding="UTF-8") as fp:
                    fp.write(f'''--- {datetime.now().strftime("%d/%m/%Y <> %H:%M:%S")} ---\n\nSql insert:\n\t{pom}\n\nQuery that coused the error:\n\t{que}\n\n''')
                return jsonify({"msg": "There was an error while submitting the form, please try again later."})
        except sqlite3.Error as e:
            with open(f"{root}server_files/server_errors/sql_server_related.txt", "a", encoding="UTF-8") as fp:
                fp.write(f'''--- {datetime.now().strftime("%d/%m/%Y <> %H:%M:%S")} ---\n\nSql insert:\n\t{e.args[1]}\n\nQuery that coused the error:\n\t{que}\n\n''')
            return jsonify({"msg": "There was an error while submitting the form, please try again later."})
    if request.method == "GET":
        if frm in active_forms:
            try:
                if session_driver.exists(request.cookies["session_id"]) == 1:                
                    return render_template(f"forms/{frm}.html", loged_in = "inserted_html/loged.html")
            except:
                pass
            return render_template(f"forms/{frm}.html", loged_in = "inserted_html/sign_in_html.html")
        else:
            return render_template("default_event.html")
            
@app.route('/map', methods = ["GET", "POST"])
def map_route():
    if request.method == "POST":
        if request.form["ra"] == "loks":
            r = ""
            with open(f"{root}server_files/server_data/locations.json") as fp:
                r = fp.read()
            return r
        return jsonify({"msg": "responce of a POST request, there wasn't any function specific return"})
    if request.method == "GET":
        try:
            if session_driver.exists(request.cookies["session_id"]) == 1:                
                return render_template("map.html", loged_in = "inserted_html/loged.html")
        except:
            pass
        return render_template("map.html", loged_in = "inserted_html/sign_in_html.html")
        
@app.route('/map-editor', methods = ["GET", "POST"])
def map_editor_route():
    try:
        if session_driver.exists(request.cookies["session_id"]) != 1:
            return redirect("/login")            
    except:
        return redirect("/login")
    
    if request.method == "GET":
        return render_template("map-editor.html")

@app.route('/events', methods = ["GET", "POST"])
def event_route():
    if request.method == "POST":
        return jsonify({"msg": "responce of a POST request, there wasn't any function specific return"})
    if request.method == "GET":
        try:
            if session_driver.exists(request.cookies["session_id"]) == 1:                
                return render_template("events.html", loged_in = "inserted_html/loged.html")
        except:
            pass
        return render_template("events.html", loged_in = "inserted_html/sign_in_html.html")

@app.route('/events-editor', methods = ["GET", "POST", "PUT"])
def event_editor_route():
    global active_posts, active_locations
    try:
        if session_driver.exists(request.cookies["session_id"]) != 1:
            return redirect("/login")            
    except:
        return redirect("/login")

    if request.method == "POST":
        try:
            ra=  request.form["ra"],
        except KeyError:
            return jsonify({"msg": "Invalid post request for this route"})
        if request.form["ra"] == "frms":
            return jsonify({"frms": json.dumps(list(active_forms))})
        if request.form["ra"] == "posts":
            postovi = []
            for post in os.listdir(event_posts):    
                post = post[:-5]
                isActive = 0
                if post in active_posts:
                    isActive = 1
                postovi.append([post,isActive])
            return jsonify({"posts": postovi})
        if request.form["ra"] == "lp":
            pom = ""
            with open(f"{event_posts}{request.form['n']}.json", "r", encoding="UTF-8") as f:
                pom = f.read()
            return jsonify({"data": pom})
        if request.form["ra"] == "dlt_img":
            try:
                p = request.form["img"]
                p = p[p.rfind("/")+1:]
                os.remove(images_folder + p)
                return jsonify({"msg": "Image deleted successfully"})
            except:
                return jsonify({"msg": "Error deleting an images"})
        if request.form["ra"] == "svd":            
            if request.form["lok"] != "":
                event_locations[request.form["file"]] = request.form["lok"]
                dict_to_file(event_locations, f"{root}server_files/server_data/savedLocations.json")
            with open(f"{event_posts}{request.form['file']}.json", "w", encoding="UTF-8") as f:
                f.write(request.form["data"])
            return jsonify({"msg": "event post saved successfully"})
        if request.form["ra"] == "unpub":
            os.remove(f"{root}server_files/templates/event/{request.form['post']}.html")
            regenerate_events_page(request.form['post'], f"{root}server_files/templates/events.html")
            regenerate_main_page(request.form['post'], f"{root}server_files/templates/main.html")
            active_posts.remove(request.form['post'])
            pom = active_locations
            active_locations = {}
            for lok in pom:
                active_locations[lok[0]] = lok[1:]
            active_locations.pop(event_locations[request.form['post']])
            pom = active_locations
            active_locations = []
            for x in zip(pom.keys(), pom.values()):
                x = list(x)
                pom = [x[0]]
                pom.extend(x[1])                
                active_locations.append(pom)
            dict_to_file(active_locations, f"{root}server_files/server_data/locations.json")
            return jsonify({"msg": "Successfully unpublished the post."})
        if request.form["ra"] == "pub":
            try:
                di = file_to_dict(f"{root}server_files/server_data/event_posts/{request.form['name']}.json")
                generate_post_from_dict(di, request.form['name'], f"{root}server_files/templates/event_layout.html", f"{root}server_files/templates/event/")
                active_posts.append(request.form['name'])
                active_locations.append([di["kords"], di["head"], di["type"], format_date(di["date"])])
                generate_events_page(di, f"{root}server_files/templates/events.html")
                generate_main_page(di, f"{root}server_files/templates/main.html")
                dict_to_file(active_locations, f"{root}server_files/server_data/locations.json")
                return jsonify({"msg": "Post published successfuly"})
            except Exception as e:
                print(e)
                return jsonify({"msg": "An Error occured while publishing the post"})    
        if request.form["ra"] == "dlt":
            di = file_to_dict(f"{event_posts}{request.form['post']}.json")
            for p in di["imgs"]:
                p = p[p.rfind("/")+1:].replace("%20", " ")
                os.remove(images_folder + p)
            os.remove(f"{event_posts}{request.form['post']}.json")
            if request.form['post'] in active_posts:
                pom = active_locations
                active_locations = {}
                for lok in pom:
                    active_locations[lok[0]] = lok[1:]
                active_locations.pop(event_locations[request.form['post']])
                pom = active_locations
                active_locations = []
                for x in zip(pom.keys(), pom.values()):
                    x = list(x)
                    pom = [x[0]]
                    pom.extend(x[1])                
                    active_locations.append(pom)
                dict_to_file(active_locations, f"{root}server_files/server_data/locations.json")
                os.remove(f"{root}server_files/templates/event/{request.form['post']}.html")            
            regenerate_events_page(request.form['post'], f"{root}server_files/templates/events.html")
            regenerate_main_page(request.form['post'], f"{root}server_files/templates/main.html")
            event_locations.pop(request.form["post"])
            dict_to_file(event_locations, f"{root}server_files/server_data/savedLocations.json")
            return jsonify({"msg": "File deleted successfully"})    
        return jsonify({"msg": "responce of a POST request, there wasn't any function specific return"})
    if request.method == "PUT":
        for f in request.files.getlist("imgs"):
            f.save(images_folder + f.filename)
        return jsonify({"msg": "Files uploaded successfully"})
    if request.method == "GET":
        return render_template("event-editor.html")

@app.route('/events/<pst>', methods = ["GET"])
def event_layout_route(pst):
    if request.method == "GET":
        if pst in active_posts:
            try:
                if session_driver.exists(request.cookies["session_id"]) == 1:                
                    return render_template(f"event/{pst}.html", loged_in = "inserted_html/loged.html")
            except:
                pass
            return render_template(f"event/{pst}.html", loged_in = "inserted_html/sign_in_html.html")
        else:
            return render_template("default_event.html")

@app.route('/about-us', methods = ["GET", "POST"])
def about_us_route():
    if request.method == "GET":
        try:
            if session_driver.exists(request.cookies["session_id"]) == 1:                
                return render_template("about-us.html", loged_in = "inserted_html/loged.html")
        except:
            pass
        return render_template("about-us.html", loged_in = "inserted_html/sign_in_html.html")

#placeholder-start
#placeholder-end

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 7000)
    # serve(TransLogger(app, 
    #         setup_console_handler=False,
    #         logger_name="EKO", 
    #         format = ('[%(time)s] %(REQUEST_METHOD)s %(status)s\t %(bytes)s [bytes]\t%(REQUEST_URI)s')),
    #         host='0.0.0.0',
    #         port=7000,
    #         threads = 50,
    #         url_scheme = "https"
    # )