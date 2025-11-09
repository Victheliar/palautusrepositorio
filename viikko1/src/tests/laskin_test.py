import unittest
from laskin import Laskin


class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def lue(self):
        return self.inputs.pop(0)

    def kirjoita(self, teksti):
        self.outputs.append(teksti)


class TestLaskin(unittest.TestCase):
    def test_yksi_summa_oikein(self):
        io = StubIO(["1", "3", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        self.assertEqual(io.outputs[0], "Summa: 4")

    def test_kaksi_summaa_oikein(self):
        io1 = StubIO(["1","5","-9999"])
        laskin = Laskin(io1)
        laskin.suorita()
        self.assertEqual(io1.outputs[0], "Summa: 6")
        io2 = StubIO(["3", "5", "-9999"])
        laskin = Laskin(io2)
        laskin.suorita()
        self.assertEqual(io2.outputs[0], "Summa: 8")
