import sqlite3

# di = file_to_dict("python_playground/formica.json")

# kon = sqlite3.connect("EKO.db")
# cur = kon.cursor()
# cur.execute("drop table Users")
# kon.commit()
# kon.close()

skripta = ""
with open("database/automatic_base.sql","r") as file:
    skripta = file.read()

kon = sqlite3.connect("EKO.db")
cur = kon.cursor()
cur.executescript(skripta)
#cur.execute("Drop table formica")
kon.commit()
kon.close()