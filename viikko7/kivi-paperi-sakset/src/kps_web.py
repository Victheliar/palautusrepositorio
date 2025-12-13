from tuomari import Tuomari

class KiviPaperiSaksetWeb:
    """Web-yhteensopiva versio kivi-paperi-sakset pelistä"""
    
    VOITTOPISTEraja = 3
    
    def __init__(self, tekoaly=None):
        self.tuomari = Tuomari()
        self.tekoaly = tekoaly
        self.peli_kaynnissa = True
    
    def pelaa_kierros(self, pelaaja1_siirto, pelaaja2_siirto=None):
        """Pelaa yhden kierroksen ja palauttaa tulokset"""
        
        # Tarkista että siirrot ovat kelvollisia
        if not self._onko_ok_siirto(pelaaja1_siirto):
            self.peli_kaynnissa = False
            return {
                'virhe': True,
                'viesti': 'Virheellinen siirto pelaaja 1:ltä',
                'lopputulos': str(self.tuomari)
            }
        
        # Jos tekoäly, hae toisen pelaajan siirto tekoälyltä
        if self.tekoaly is not None:
            pelaaja2_siirto = self.tekoaly.anna_siirto()
            if hasattr(self.tekoaly, 'aseta_siirto'):
                self.tekoaly.aseta_siirto(pelaaja1_siirto)
        
        # Tarkista toisen pelaajan siirto
        if not self._onko_ok_siirto(pelaaja2_siirto):
            self.peli_kaynnissa = False
            return {
                'virhe': True,
                'viesti': 'Virheellinen siirto pelaaja 2:lta',
                'lopputulos': str(self.tuomari)
            }
        
        # Kirjaa siirto
        self.tuomari.kirjaa_siirto(pelaaja1_siirto, pelaaja2_siirto)
        
        # Tarkista onko peli päättynyt (5 voittoa)
        if self.tuomari.ekan_pisteet >= self.VOITTOPISTEraja or self.tuomari.tokan_pisteet >= self.VOITTOPISTEraja:
            self.peli_kaynnissa = False
        
        return {
            'virhe': False,
            'pelaaja1_siirto': pelaaja1_siirto,
            'pelaaja2_siirto': pelaaja2_siirto,
            'tilanne': str(self.tuomari),
            'ekan_pisteet': self.tuomari.ekan_pisteet,
            'tokan_pisteet': self.tuomari.tokan_pisteet,
            'tasapelit': self.tuomari.tasapelit,
            'peli_paattynyt': not self.peli_kaynnissa
        }
    
    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"
    
    def lopeta_peli(self):
        """Palauttaa lopullisen tuloksen"""
        self.peli_kaynnissa = False
        return {
            'lopputulos': str(self.tuomari),
            'ekan_pisteet': self.tuomari.ekan_pisteet,
            'tokan_pisteet': self.tuomari.tokan_pisteet,
            'tasapelit': self.tuomari.tasapelit
        }
