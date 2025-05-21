from model import *
from bottle import Bottle, run, template, request, redirect, response

def preveri_registracija(ime,priimek,email):
    '''funkcija preverja ali je uporabnik že v bazi'''
    
    uporabniki = Uporabniki.dobi_uporabnika()
    tabela_uporabnikov = [(i.ime,i.priimek,i.email) for i in uporabniki]
    if (f'{ime}', f'{priimek}', f'{email}') in tabela_uporabnikov:
        return True
    else:
        return False

def preveri_prijava(ime,geslo):
    '''funckija preverja ali se lahko uporabnik prijavi'''
    uporabniki = Uporabniki.dobi_uporabnika()
    tabela_uporabnikov = [(i.ime,i.geslo) for i in uporabniki]
    if (f'{ime}', f'{geslo}') not in tabela_uporabnikov:
        return False
    else:
        return True
      
# def izdelki_po_kategorijah():
#     '''funkcija naredi slovar, kjer so kljuèi kategorije_id in vrednosti imena izdelkov'''
#     izdelki = Izdelki.vsi_izdelki()
#     kategorije = dict()
#     for st_kategorij in izdelki:
#         kategorije[st_kategorij.kategorija_id] = []
#     for i in izdelki:
#         kategorije[i.kategorija_id].append(i.naziv)
#     return kategorije

app = Bottle()

skrivnost = "ne-povem"

@app.route('/', method="GET")
def home_page():
    ime = request.get_cookie("uporabnik", secret=skrivnost)
    return template('homepage', ime=ime)

@app.route('/izdelki', method="GET")
def izdelki_page():
    izdelki = Izdelki.vsi_izdelki()
    ime = request.get_cookie("uporabnik", secret=skrivnost)
    
    return template('izdelki', izdelki=izdelki, ime=ime)

@app.route('/kosarica', method="GET")
def kosarica_page():
    return template('kosarica')

@app.route('/prijava', method="GET")
def prijava_page():
    return template('prijava')

@app.route('/prijava', method="POST")
def prijava_page():
    ime = request.forms.get('ime')
    geslo = request.forms.get('geslo')
    if preveri_prijava(ime,geslo) == True:
        response.set_cookie('uporabnik', ime, secret=skrivnost, path='/')
        return redirect('/')
    else:
        return "<a href='/prijava'> Prijava ni uspela, prosimo poskusite znova</a>"

@app.route('/odjava')
def odjava():
    response.delete_cookie("uporabnik", path='/')
    return redirect('/')

@app.route('/registracija', method="GET")
def registracija_page():
    return template('registracija')

@app.route('/registracija', method="POST")
def registracija_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    email = request.forms.get('email')
    geslo = request.forms.get('geslo')
    
    if preveri_registracija(ime,priimek,email) == True:
        return "<a href='/registracija'> Uporabnik že obstaja, prosimo poskusite znova</a>"
    
    Uporabniki.shrani_uporabnika(ime,priimek,email,geslo)
    response.set_cookie('uporabnik', ime, secret=skrivnost, path='/')
    return redirect('/')
        
    
    
if __name__ == "__main__":
    app.run(host='localhost', port=8080, reloader=True, debug=True)


