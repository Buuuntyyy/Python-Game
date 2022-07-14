
import sqlite3

""""
def create_dict(pseudo, score, rank):
    compte = {
        "Pseudo": str(pseudo),
        "Score": int(score),
        "classement": int(rank)
    }

    return compte


c1 = create_dict("Inzerg", 0, 1), create_dict("Pierre", 0, 2), create_dict("Renaid", 0, 3), create_dict("Aladin", 0, 4)  , create_dict("JPG", 0, 5), create_dict("antoine", 0, 6)
c2 = create_dict("Thomas", 0, 7)

with open('compte.json', 'w+') as f:
    re = f.readlines()
    json.dump(c1, f, indent=2)


connexion = sqlite3.connect('comptes.db')
cur = connexion.cursor()
#requete = "create table comptes(id integer primary key autoincrement, pseudo text, score integer, rank integer)"
requete = "insert into comptes(pseudo, score, rank) values ('Alouette', 0, 0)"
cur.execute(requete)
connexion.commit()
connexion.close()
"""

conn = sqlite3.connect('comptes.db')
cursor = conn.cursor()
update = "UPDATE comptes SET score = 10 WHERE pseudo = 'Inzerg'"
cursor.execute(update)
conn.commit()
conn.close()

con = sqlite3.connect('comptes.db')
cu = con.cursor()
pseudo = 'Inzerg'
cu.execute("INSERT or ignore INTO comptes(pseudo) values ('Pierre ')")
con.commit()
con.close()

conne = sqlite3.connect('comptes.db')
curs = conne.cursor()
