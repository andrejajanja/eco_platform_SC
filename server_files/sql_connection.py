from lib import User_log
from pyodbc import connect

konekcija = connect(r"Driver={ODBC Driver 17 for SQL Server};Server=localhost\SQLEXPRESS;Database=EKO;Trusted_Connection=yes;")
k = konekcija.cursor()
r = k.execute("SELECT * from Ids where email = 'andreja0@janja.xyz';")
print(User_log(r.fetchall()))
konekcija.close()