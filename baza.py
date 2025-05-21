import sqlite3
import pandas

def naredi_tabelo(conn):
    with conn:
        #UPORABNIKI
        conn.execute(
            """CREATE TABLE IF NOT EXISTS uporabniki (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ime TEXT NOT NULL,
            priimek TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            geslo TEXT NOT NULL
        );"""
        )
        #KATEGORIJE
        conn.execute(
        """CREATE TABLE IF NOT EXISTS kategorije (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naziv TEXT NOT NULL
        );"""
        )
        #IZDELKI
        conn.execute(
            """CREATE TABLE IF NOT EXISTS izdelki (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naziv TEXT NOT NULL,
            opis TEXT NOT NULL,
            cena REAL NOT NULL,
            kategorija_id INTEGER NOT NULL,
            FOREIGN KEY (kategorija_id) REFERENCES kategorije (id)
            );"""
        )
        #NAROCILA
        conn.execute(
            """CREATE TABLE IF NOT EXISTS narocila (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uporabnik_id INTEGER NOT NULL,
            skupna_cena REAL NOT NULL,
            datum DATETIME NOT NULL,
            dostava_id INTEGER NOT NULL,
            FOREIGN KEY (uporabnik_id) REFERENCES uporabniki (id)
            )"""
        )
        #POSTAVKE NAROČIL
        conn.execute(
            """CREATE TABLE IF NOT EXISTS postavke_narocil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            narocilo_id INTEGER NOT NULL,
            izdelek_id INTEGER NOT NULL,
            kolicina INTEGER NOT NULL,
            skupna_cena REAL NOT NULL,
            FOREIGN KEY (narocilo_id) REFERENCES narocila (id),
            FOREIGN KEY (izdelek_id) REFERENCES izdelki (id)
        );"""
        )
        #DOSTAVA
        conn.execute(
            """CREATE TABLE IF NOT EXISTS dostava (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesto TEXT NOT NULL,
            postna_stevilka TEXT NOT NULL
        );"""
        )

def dodaj_podatke(conn):
    with conn:
        tab = ["podatki/kategorije.csv", "podatki/uporabniki123456.csv", "podatki/dostava.csv", "podatki/narocilo.csv",
               "podatki/postavke.csv", "podatki/izdelkii.csv"]
        #IZDELKI
        with open(tab[5], encoding="utf-8") as dat:
            podatki = pandas.read_csv(dat)
            izdelki_tabela = podatki.to_dict(orient="records")
            for izdelki in izdelki_tabela:
                conn.execute("""
                    INSERT INTO izdelki(id, naziv, opis, cena, kategorija_id)
                    VALUES (?,?,?,?,?)
                    """, (izdelki["id"], izdelki["naziv"], izdelki["opis"], izdelki["cena"], izdelki["kategorija_id"]))
        #NAROCILA
        with open(tab[4], encoding="utf-8") as dat:
            podatki = pandas.read_csv(dat)
            postavke_tabela = podatki.to_dict(orient="records")
            for postavke in postavke_tabela:
                conn.execute("""
                    INSERT INTO postavke_narocil (id, narocilo_id, izdelek_id, kolicina, skupna_cena)
                    VALUES (?, ?, ?, ?, ?)
                    """,(postavke["id"], postavke["narocilo_id"],postavke["izdelek_id"],postavke["količina"],postavke["skupna_cena"]))
        #NAROCILA
        with open(tab[3], encoding="utf-8") as dat:
            podatki = pandas.read_csv(dat)
            narocila_tabela = podatki.to_dict(orient="records")
            for narocila in narocila_tabela:
                conn.execute("""
                    INSERT INTO narocila (id, uporabnik_id, skupna_cena, datum, dostava_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,(narocila['id'],narocila['uporabnik_id'],narocila['skupna_cena'], narocila['datum'],narocila['dostava_id']))

        #DOSTAVA
        with open(tab[2], encoding="utf-8") as dat:
            podatki = pandas.read_csv(dat)
            dostava_tabela = podatki.to_dict(orient="records")
            for dostava in dostava_tabela:
                conn.execute("""
                    INSERT INTO dostava (id, mesto, postna_stevilka)
                    VALUES (?, ?, ?)
                    """,(dostava['id'],dostava['mesto'],dostava['postna_stevilka']))
        #UPORABNIKI
        with open(tab[1], encoding="utf-8") as dat:
            podatki = pandas.read_csv(dat)
            tabela = podatki.to_dict(orient="records")
            for uporabnik in tabela:
                conn.execute("""
                    INSERT INTO uporabniki (id, ime, priimek, email, geslo)
                    VALUES (?, ?, ?, ? ,?)
                    """, (uporabnik['id'], uporabnik['ime'], uporabnik['priimek'], uporabnik['email'], uporabnik['geslo']))
        #KATEGORIJA
        with open(tab[0], encoding="utf-8") as dat:
            podatki = pandas.read_csv(dat)
            kategorija_tabela = podatki.to_dict(orient="records")
            for kategorija in kategorija_tabela:
                conn.execute("""
                    INSERT INTO kategorije (id, naziv)
                    VALUES (?, ?)
                """,(kategorija["kategorija_id"], kategorija["naziv_kategorije"]))

              

def pripravi_bazo(conn):
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        #da ne vrne napake, èe bi dajali stvari se enkrat na isto mesto#
        if cur.fetchone() != (0, ):
            return
        naredi_tabelo(conn)
        dodaj_podatke(conn)

#konec