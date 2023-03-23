import random
query = ""
imena = ["andreja", "miki", "marija", "pedja", "aca", "nemanja", "dunja"]
prezimena = ["tadic", "simic", "sapic", "milovanovic", "arsenovic", "petrovic"]
je = ["true", "false"]
for ime in imena:
    br = 0
    for prez in prezimena:
        query+=f"INSERT INTO formica VALUES (NULL, '{ime}','{prez}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}');\n"
        br+=1
f = open("database/automatic_base.sql", "w")
f.write(query)
f.close()