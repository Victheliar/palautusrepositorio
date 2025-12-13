import pytest
import sys
from pathlib import Path

# Lisää src-kansio Python-polkuun
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


class TestFlaskApp:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        with app.test_client() as client:
            yield client

    def test_etusivu_latautuu(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Valitse pelityyppi' in response.data

    def test_etusivu_nayttaa_pelityypit(self, client):
        response = client.get('/')
        assert b'Pelaaja vs Pelaaja' in response.data
        content = response.data.decode('utf-8')
        assert 'Tekoaly' in content or 'Tekoäly' in content

    def test_aloita_peli_pvp(self, client):
        response = client.get('/aloita/pvp', follow_redirects=True)
        assert response.status_code == 200

    def test_aloita_peli_ai_easy(self, client):
        response = client.get('/aloita/ai_easy', follow_redirects=True)
        assert response.status_code == 200

    def test_aloita_peli_ai_hard(self, client):
        response = client.get('/aloita/ai_hard', follow_redirects=True)
        assert response.status_code == 200

    def test_aloita_peli_virheellinen_tyyppi(self, client):
        response = client.get('/aloita/invalid', follow_redirects=True)
        assert response.status_code == 200
        assert b'Valitse pelityyppi' in response.data

    def test_pelaa_sivu_ilman_pelityyppia_redirectaa(self, client):
        response = client.get('/pelaa', follow_redirects=True)
        assert b'Valitse pelityyppi' in response.data

    def test_pelaa_sivu_pvp_nakyy(self, client):
        # Aloita peli ensin
        client.get('/aloita/pvp')
        response = client.get('/pelaa')
        assert response.status_code == 200
        assert b'Pelaaja 1' in response.data
        assert b'Pelaaja 2' in response.data

    def test_pelaa_kierros_pvp(self, client):
        # Aloita peli
        client.get('/aloita/pvp')
        
        # Pelaa kierros
        response = client.post('/pelaa', data={
            'siirto': 'k',
            'siirto2': 's'
        }, follow_redirects=True)
        
        assert response.status_code == 200

    def test_pelaa_kierros_ai(self, client):
        # Aloita tekoälypeli
        client.get('/aloita/ai_easy')
        
        # Pelaa kierros
        response = client.post('/pelaa', data={
            'siirto': 'k'
        }, follow_redirects=True)
        
        assert response.status_code == 200

    def test_lopeta_peli_nayttaa_tulokset(self, client):
        # Aloita ja pelaa
        client.get('/aloita/pvp')
        client.post('/pelaa', data={'siirto': 'k', 'siirto2': 's'})
        
        # Lopeta
        response = client.get('/lopeta')
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert 'Peli' in content

    def test_session_toimii(self, client):
        # Aloita peli
        response = client.get('/aloita/pvp', follow_redirects=True)
        
        # Session pitäisi sisältää pelityyppi
        with client.session_transaction() as session:
            assert 'pelityyppi' in session
            assert session['pelityyppi'] == 'pvp'

    def test_pisteiden_laskenta(self, client):
        # Aloita peli
        client.get('/aloita/pvp')
        
        # Pelaa useita kierroksia (ei vielä 3 voittoa)
        client.post('/pelaa', data={'siirto': 'k', 'siirto2': 's'})  # eka voittaa
        client.post('/pelaa', data={'siirto': 'p', 'siirto2': 's'})  # toka voittaa
        client.post('/pelaa', data={'siirto': 'k', 'siirto2': 'k'})  # tasapeli
        
        response = client.get('/pelaa')
        assert response.status_code == 200

    def test_peli_paattyy_automaattisesti_3_voiton_jalkeen(self, client):
        # Aloita peli
        client.get('/aloita/pvp')
        
        # Pelaa 3 voittokierrosta pelaaja 1:lle
        for _ in range(3):
            response = client.post('/pelaa', data={'siirto': 'k', 'siirto2': 's'}, follow_redirects=False)
        
        # Viimeisen kierroksen jälkeen pitäisi ohjata /lopeta-sivulle
        assert response.status_code == 302
        assert '/lopeta' in response.location

    def test_peli_ohjaa_lopetussivulle_jos_jo_paattynyt(self, client):
        # Aloita ja pelaa loppuun
        client.get('/aloita/pvp')
        for _ in range(3):
            client.post('/pelaa', data={'siirto': 'k', 'siirto2': 's'})
        
        # Yritä päästä takaisin pelisivulle
        response = client.get('/pelaa', follow_redirects=False)
        assert response.status_code == 302
        assert '/lopeta' in response.location

    def test_static_css_latautuu(self, client):
        response = client.get('/static/style.css')
        assert response.status_code == 200
        assert b'body' in response.data or b'container' in response.data
