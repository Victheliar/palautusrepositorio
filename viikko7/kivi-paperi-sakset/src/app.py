from flask import Flask, render_template, request, session, redirect, url_for
from kps_web import KiviPaperiSaksetWeb
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Pelityyppien määrittelyt
PELI_TYYPIT = {
    'pvp': {'nimi': 'Pelaaja vs Pelaaja', 'tekoaly': None},
    'ai_easy': {'nimi': 'Pelaaja vs Tekoäly', 'tekoaly': 'easy'},
    'ai_hard': {'nimi': 'Pelaaja vs Parannettu Tekoäly', 'tekoaly': 'hard'}
}

def hae_peli():
    """Hakee session peliinstanssin tai luo uuden"""
    if 'peli' not in session or session['peli'] is None:
        return None
    return session['peli']

@app.route('/')
def index():
    """Etusivu - valitse pelityyppi"""
    session.clear()
    return render_template('index.html', peli_tyypit=PELI_TYYPIT)

@app.route('/aloita/<pelityyppi>')
def aloita_peli(pelityyppi):
    """Aloita uusi peli valitulla tyypillä"""
    if pelityyppi not in PELI_TYYPIT:
        return redirect(url_for('index'))
    
    # Luo uusi peli
    session.clear()
    session['pelityyppi'] = pelityyppi
    session['historia'] = []
    
    return redirect(url_for('pelaa'))

@app.route('/pelaa', methods=['GET', 'POST'])
def pelaa():
    """Pelisivu"""
    if 'pelityyppi' not in session:
        return redirect(url_for('index'))
    
    pelityyppi = session['pelityyppi']
    peli_info = PELI_TYYPIT[pelityyppi]
    
    # Tarkista onko peli jo päättynyt
    historia = session.get('historia', [])
    if historia and historia[-1].get('peli_paattynyt'):
        return redirect(url_for('lopeta'))
    
    if request.method == 'POST':
        pelaaja1_siirto = request.form.get('siirto')
        pelaaja2_siirto = request.form.get('siirto2') if pelityyppi == 'pvp' else None
        
        # Nouda nykyiset kumulatiiviset pisteet viimeisestä onnistuneesta kierroksesta
        ekan_pisteet = 0
        tokan_pisteet = 0
        tasapelit = 0
        for kierros in reversed(historia):
            if not kierros.get('virhe'):
                ekan_pisteet = kierros.get('ekan_pisteet', 0)
                tokan_pisteet = kierros.get('tokan_pisteet', 0)
                tasapelit = kierros.get('tasapelit', 0)
                break
        
        # Tarkista onko peli jo päättynyt
        if ekan_pisteet >= 3 or tokan_pisteet >= 3:
            return redirect(url_for('lopeta'))
        
        # Luo uusi peli
        tekoaly = None
        if peli_info['tekoaly'] == 'easy':
            tekoaly = Tekoaly()
        elif peli_info['tekoaly'] == 'hard':
            tekoaly = TekoalyParannettu(10)
        
        peli = KiviPaperiSaksetWeb(tekoaly)
        
        # Aseta pisteet ennen uutta kierrosta
        peli.tuomari.ekan_pisteet = ekan_pisteet
        peli.tuomari.tokan_pisteet = tokan_pisteet
        peli.tuomari.tasapelit = tasapelit
        
        # Pelaa kierros
        tulos = peli.pelaa_kierros(pelaaja1_siirto, pelaaja2_siirto)
        
        # Tallenna historia
        if 'historia' not in session:
            session['historia'] = []
        
        historia = session['historia']
        historia.append(tulos)
        session['historia'] = historia
        session.modified = True
        
        # Jos peli päättyi, ohjaa lopetussivulle
        if tulos.get('peli_paattynyt'):
            return redirect(url_for('lopeta'))
        
        return redirect(url_for('pelaa'))
    
    # GET-pyyntö - näytä pelisivu
    
    # Laske kokonaispisteet viimeisestä onnistuneesta kierroksesta
    ekan_pisteet = 0
    tokan_pisteet = 0
    tasapelit = 0
    for kierros in reversed(historia):
        if not kierros.get('virhe'):
            ekan_pisteet = kierros.get('ekan_pisteet', 0)
            tokan_pisteet = kierros.get('tokan_pisteet', 0)
            tasapelit = kierros.get('tasapelit', 0)
            break
    
    return render_template('pelaa.html', 
                         pelityyppi=pelityyppi,
                         peli_info=peli_info,
                         historia=historia,
                         ekan_pisteet=ekan_pisteet,
                         tokan_pisteet=tokan_pisteet,
                         tasapelit=tasapelit)

@app.route('/lopeta')
def lopeta():
    """Lopeta peli ja näytä tulokset"""
    historia = session.get('historia', [])
    pelityyppi = session.get('pelityyppi', 'pvp')
    peli_info = PELI_TYYPIT.get(pelityyppi, PELI_TYYPIT['pvp'])
    
    # Laske kokonaispisteet viimeisestä onnistuneesta kierroksesta
    ekan_pisteet = 0
    tokan_pisteet = 0
    tasapelit = 0
    for kierros in reversed(historia):
        if not kierros.get('virhe'):
            ekan_pisteet = kierros.get('ekan_pisteet', 0)
            tokan_pisteet = kierros.get('tokan_pisteet', 0)
            tasapelit = kierros.get('tasapelit', 0)
            break
    
    return render_template('lopeta.html',
                         historia=historia,
                         peli_info=peli_info,
                         ekan_pisteet=ekan_pisteet,
                         tokan_pisteet=tokan_pisteet,
                         tasapelit=tasapelit)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
