import random
query = '''USE EKO;
GO
'''

def nasumicni_datum():
    godine = list(range(2014,2024))
    meseci = list(range(1,13))
    dani = list(range(1,31))    
    return f"{random.choice(godine)}-{random.choice(meseci)}-{random.choice(dani)}"

imena = ["andreja", "miki", "marija", "pedja", "aca", "nemanja", "dunja"]
prezimena = ["tadic", "simic", "sapic", "milovanovic", "arsenovic", "petrovic"]

je = ["true", "false"]

for ime in imena:
    br = 0
    for prez in prezimena:
        query+=f"INSERT INTO poziv VALUES ('{ime}','{prez}','Neki opis sta bi osoba zelela da radi', '{random.choice(je)}','{random.choice(je)}','{random.choice(je)}', '{nasumicni_datum()}', '14:20:00');\nGO\n"
        br+=1
f = open("baza/popuni_odgovore.sql", "w")
f.write(query)
f.close()