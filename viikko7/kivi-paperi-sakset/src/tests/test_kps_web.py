import pytest
import sys
from pathlib import Path

# Lisää src-kansio Python-polkuun
sys.path.insert(0, str(Path(__file__).parent.parent))

from kps_web import KiviPaperiSaksetWeb
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


class TestKiviPaperiSaksetWeb:
    def test_peli_alustetaan_oikein(self):
        peli = KiviPaperiSaksetWeb()
        assert peli.peli_kaynnissa == True
        assert peli.tuomari.ekan_pisteet == 0
        assert peli.tuomari.tokan_pisteet == 0

    def test_peli_tekoalylla_alustetaan(self):
        tekoaly = Tekoaly()
        peli = KiviPaperiSaksetWeb(tekoaly)
        assert peli.tekoaly is not None

    def test_pelaaja_vs_pelaaja_tasapeli(self):
        peli = KiviPaperiSaksetWeb()
        tulos = peli.pelaa_kierros("k", "k")
        
        assert tulos['virhe'] == False
        assert tulos['pelaaja1_siirto'] == "k"
        assert tulos['pelaaja2_siirto'] == "k"
        assert tulos['tasapelit'] == 1
        assert tulos['ekan_pisteet'] == 0
        assert tulos['tokan_pisteet'] == 0
        assert tulos['peli_paattynyt'] == False

    def test_pelaaja_vs_pelaaja_eka_voittaa(self):
        peli = KiviPaperiSaksetWeb()
        tulos = peli.pelaa_kierros("k", "s")
        
        assert tulos['virhe'] == False
        assert tulos['ekan_pisteet'] == 1
        assert tulos['tokan_pisteet'] == 0
        assert tulos['tasapelit'] == 0
        assert tulos['peli_paattynyt'] == False

    def test_pelaaja_vs_pelaaja_toka_voittaa(self):
        peli = KiviPaperiSaksetWeb()
        tulos = peli.pelaa_kierros("s", "k")
        
        assert tulos['virhe'] == False
        assert tulos['ekan_pisteet'] == 0
        assert tulos['tokan_pisteet'] == 1
        assert tulos['tasapelit'] == 0
        assert tulos['peli_paattynyt'] == False

    def test_virheellinen_siirto_pelaaja1(self):
        peli = KiviPaperiSaksetWeb()
        tulos = peli.pelaa_kierros("x", "k")
        
        assert tulos['virhe'] == True
        assert 'viesti' in tulos
        assert peli.peli_kaynnissa == False

    def test_virheellinen_siirto_pelaaja2(self):
        peli = KiviPaperiSaksetWeb()
        tulos = peli.pelaa_kierros("k", "x")
        
        assert tulos['virhe'] == True
        assert 'viesti' in tulos
        assert peli.peli_kaynnissa == False

    def test_tekoaly_pelaa_siirron(self):
        tekoaly = Tekoaly()
        peli = KiviPaperiSaksetWeb(tekoaly)
        tulos = peli.pelaa_kierros("k")
        
        assert tulos['virhe'] == False
        assert tulos['pelaaja1_siirto'] == "k"
        assert tulos['pelaaja2_siirto'] in ["k", "p", "s"]
        assert tulos['peli_paattynyt'] == False

    def test_parannettu_tekoaly_pelaa(self):
        tekoaly = TekoalyParannettu(10)
        peli = KiviPaperiSaksetWeb(tekoaly)
        tulos = peli.pelaa_kierros("k")
        
        assert tulos['virhe'] == False
        assert tulos['pelaaja2_siirto'] in ["k", "p", "s"]
        assert tulos['peli_paattynyt'] == False

    def test_usea_kierros_kerryttaa_pisteet(self):
        peli = KiviPaperiSaksetWeb()
        
        tulos1 = peli.pelaa_kierros("k", "s")  # eka voittaa
        assert tulos1['peli_paattynyt'] == False
        
        tulos2 = peli.pelaa_kierros("p", "s")  # toka voittaa
        assert tulos2['peli_paattynyt'] == False
        
        tulos3 = peli.pelaa_kierros("k", "k")  # tasapeli
        
        assert tulos3['ekan_pisteet'] == 1
        assert tulos3['tokan_pisteet'] == 1
        assert tulos3['tasapelit'] == 1
        assert tulos3['peli_paattynyt'] == False

    def test_lopeta_peli(self):
        peli = KiviPaperiSaksetWeb()
        peli.pelaa_kierros("k", "s")
        peli.pelaa_kierros("p", "s")
        
        lopputulos = peli.lopeta_peli()
        
        assert lopputulos['ekan_pisteet'] == 1
        assert lopputulos['tokan_pisteet'] == 1
        assert 'lopputulos' in lopputulos
        assert peli.peli_kaynnissa == False

    def test_kaikki_siirtokombinaatiot(self):
        """Testaa kaikki mahdolliset siirtokombinaatiot"""
        peli = KiviPaperiSaksetWeb()
        
        # Kaikki tasapelit
        for siirto in ['k', 'p', 's']:
            tulos = peli.pelaa_kierros(siirto, siirto)
            assert tulos['virhe'] == False
        
        # Kaikki pelaaja 1 voitot
        peli2 = KiviPaperiSaksetWeb()
        tulos = peli2.pelaa_kierros('k', 's')
        assert tulos['ekan_pisteet'] == 1
        
        tulos = peli2.pelaa_kierros('p', 'k')
        assert tulos['ekan_pisteet'] == 2
        
        tulos = peli2.pelaa_kierros('s', 'p')
        assert tulos['ekan_pisteet'] == 3

    def test_peli_paattyy_kun_pelaaja1_saa_3_voittoa(self):
        """Testaa että peli päättyy kun pelaaja 1 saa 3 voittoa"""
        peli = KiviPaperiSaksetWeb()
        
        # Pelaa 2 voittokierrosta
        for _ in range(2):
            tulos = peli.pelaa_kierros('k', 's')  # eka voittaa
            assert tulos['peli_paattynyt'] == False
            assert peli.peli_kaynnissa == True
        
        # Kolmas voitto - pelin pitäisi päättyä
        tulos = peli.pelaa_kierros('k', 's')
        assert tulos['ekan_pisteet'] == 3
        assert tulos['peli_paattynyt'] == True
        assert peli.peli_kaynnissa == False

    def test_peli_paattyy_kun_pelaaja2_saa_3_voittoa(self):
        """Testaa että peli päättyy kun pelaaja 2 saa 3 voittoa"""
        peli = KiviPaperiSaksetWeb()
        
        # Pelaa 2 voittokierrosta
        for _ in range(2):
            tulos = peli.pelaa_kierros('s', 'k')  # toka voittaa
            assert tulos['peli_paattynyt'] == False
            assert peli.peli_kaynnissa == True
        
        # Kolmas voitto - pelin pitäisi päättyä
        tulos = peli.pelaa_kierros('s', 'k')
        assert tulos['tokan_pisteet'] == 3
        assert tulos['peli_paattynyt'] == True
        assert peli.peli_kaynnissa == False

    def test_peli_jatkuu_jos_alle_3_voittoa(self):
        """Testaa että peli jatkuu kun kummallakin alle 3 voittoa"""
        peli = KiviPaperiSaksetWeb()
        
        # Pelaa 2 voittoa kummallekin
        for _ in range(2):
            peli.pelaa_kierros('k', 's')  # eka voittaa
            tulos = peli.pelaa_kierros('s', 'k')  # toka voittaa
            assert tulos['peli_paattynyt'] == False
        
        assert peli.peli_kaynnissa == True
        assert peli.tuomari.ekan_pisteet == 2
        assert peli.tuomari.tokan_pisteet == 2

    def test_tasapelit_eivat_paata_pelia(self):
        """Testaa että tasapelit eivät päätä peliä"""
        peli = KiviPaperiSaksetWeb()
        
        # Pelaa 10 tasapeliä
        for _ in range(10):
            tulos = peli.pelaa_kierros('k', 'k')
            assert tulos['peli_paattynyt'] == False
        
        assert peli.peli_kaynnissa == True
        assert peli.tuomari.tasapelit == 10
