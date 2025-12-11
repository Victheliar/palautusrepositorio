import pytest
import sys
from pathlib import Path

# Lisää src-kansio Python-polkuun
sys.path.insert(0, str(Path(__file__).parent.parent))

from tuomari import Tuomari


class TestTuomari:
    def setup_method(self):
        self.tuomari = Tuomari()

    def test_alussa_pisteet_nolla(self):
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_tasapeli_kirjataan(self):
        self.tuomari.kirjaa_siirto("k", "k")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0

    def test_eka_voittaa_kivi_sakset(self):
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_sakset_paperi(self):
        self.tuomari.kirjaa_siirto("s", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0

    def test_eka_voittaa_paperi_kivi(self):
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0

    def test_toka_voittaa_kivi_sakset(self):
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1

    def test_toka_voittaa_sakset_paperi(self):
        self.tuomari.kirjaa_siirto("p", "s")
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.ekan_pisteet == 0

    def test_toka_voittaa_paperi_kivi(self):
        self.tuomari.kirjaa_siirto("k", "p")
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.ekan_pisteet == 0

    def test_usean_kierroksen_pisteiden_kasvu(self):
        self.tuomari.kirjaa_siirto("k", "s")  # eka voittaa
        self.tuomari.kirjaa_siirto("p", "s")  # toka voittaa
        self.tuomari.kirjaa_siirto("k", "k")  # tasapeli
        
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 1

    def test_tuomari_str(self):
        self.tuomari.kirjaa_siirto("k", "s")
        self.tuomari.kirjaa_siirto("p", "s")
        tulostus = str(self.tuomari)
        
        assert "1" in tulostus
        assert "1" in tulostus
        assert "0" in tulostus
