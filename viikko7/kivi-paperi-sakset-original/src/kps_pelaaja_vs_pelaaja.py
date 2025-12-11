# from tuomari import Tuomari
from kivipaperisakset import KiviPaperiSakset


class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = input("Toisen pelaajan siirto: ")
        return tokan_siirto
    
    
    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"
