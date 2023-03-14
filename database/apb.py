import random
query = '''USE EKO;
GO
'''
imena = ["andreja", "miki", "marija", "pedja", "aca", "nemanja", "dunja"]
prezimena = ["tadic", "simic", "sapic", "milovanovic", "arsenovic", "petrovic"]
je = ["true", "false"]
for ime in imena:
    br = 0
    for prez in prezimena:
        query+=f"INSERT INTO formica VALUES ('{ime}','{prez}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}','{random.choice(je)}');\nGO\n"
        br+=1
f = open("database/automatic_base.sql", "w")
f.write(query)
f.close()