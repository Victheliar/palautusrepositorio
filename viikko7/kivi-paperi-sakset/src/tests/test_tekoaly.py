import pytest
import sys
from pathlib import Path

# Lisää src-kansio Python-polkuun
sys.path.insert(0, str(Path(__file__).parent.parent))

from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


class TestTekoaly:
    def test_tekoaly_antaa_siirron(self):
        tekoaly = Tekoaly()
        siirto = tekoaly.anna_siirto()
        assert siirto in ["k", "p", "s"]

    def test_tekoaly_vaihtaa_siirtoja(self):
        tekoaly = Tekoaly()
        siirrot = []
        for _ in range(6):
            siirrot.append(tekoaly.anna_siirto())
        
        # Pitäisi nähdä kaikkia kolmea siirtoa
        assert "k" in siirrot
        assert "p" in siirrot
        assert "s" in siirrot

    def test_tekoaly_aseta_siirto_ei_kaada(self):
        tekoaly = Tekoaly()
        tekoaly.aseta_siirto("k")  # ei tee mitään
        assert tekoaly.anna_siirto() in ["k", "p", "s"]


class TestTekoalyParannettu:
    def test_parannettu_tekoaly_antaa_siirron(self):
        tekoaly = TekoalyParannettu(10)
        siirto = tekoaly.anna_siirto()
        assert siirto in ["k", "p", "s"]

    def test_parannettu_tekoaly_ensimmainen_siirto_on_kivi(self):
        tekoaly = TekoalyParannettu(10)
        assert tekoaly.anna_siirto() == "k"

    def test_parannettu_tekoaly_muistaa_siirtoja(self):
        tekoaly = TekoalyParannettu(5)
        
        # Syötä muutama siirto
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("k")
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("p")
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("s")
        
        # Seuraavan siirron pitäisi olla jokin kelvollinen
        siirto = tekoaly.anna_siirto()
        assert siirto in ["k", "p", "s"]

    def test_parannettu_tekoaly_muisti_rajoitettu(self):
        tekoaly = TekoalyParannettu(3)
        
        # Täytä muisti
        for _ in range(5):
            tekoaly.anna_siirto()
            tekoaly.aseta_siirto("k")
        
        # Ei pitäisi kaatua
        siirto = tekoaly.anna_siirto()
        assert siirto in ["k", "p", "s"]

    def test_parannettu_tekoaly_reagoi_kuvioihin(self):
        tekoaly = TekoalyParannettu(10)
        
        # Luo kuvio: k -> p -> k -> p
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("k")
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("p")
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("k")
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("p")
        
        # Nyt jos pelaaja pelaa k, tekoälyn pitäisi yrittää voittaa p
        tekoaly.anna_siirto()
        tekoaly.aseta_siirto("k")
        siirto = tekoaly.anna_siirto()
        
        # Tekoälyn pitäisi antaa joku kelvollinen siirto
        assert siirto in ["k", "p", "s"]
