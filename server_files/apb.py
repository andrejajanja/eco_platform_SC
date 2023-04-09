from all_library import SQLConnector
import random
root = ""
query = ""
imena = ["andreja", "miki", "marija", "pedja", "aca", "nemanja", "dunja"]
prezimena = ["tadic", "simic", "sapic", "milovanovic", "arsenovic", "petrovic"]
je = ["true", "false"]
kon = SQLConnector(f"{root}EKO.db", root)
for ime in imena:
    br = 0
    for prez in prezimena:
        kon.execute_query(f"INSERT INTO example_form VALUES (NULL, '{ime}','{prez}','OVO JE NEKO OPIS POLJE','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}');\n", True)
        br+=1

# f = open("database/automatic_base.sql", "w")
# f.write(query)
# f.close()