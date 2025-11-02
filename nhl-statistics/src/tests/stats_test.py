import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    def test_correct_search(self):
        player = self.stats.search("Semenko")
        self.assertAlmostEqual(str(player), "Semenko EDM 4 + 12 = 16")
    
    def test_incorrect_search(self):
        player = self.stats.search("Popiskelija")
        self.assertAlmostEqual(player, None)
        
    def test_team(self):
        team_list = self.stats.team("EDM")
        players = [str(player) for player in team_list]
        self.assertEqual(players, ["Semenko EDM 4 + 12 = 16", "Kurri EDM 37 + 53 = 90", "Gretzky EDM 35 + 89 = 124"])
        
    def test_sort_by_points(self):
        sorted_players = self.stats.top(4)
        players = [str(player) for player in sorted_players]
        self.assertEqual(players, ["Gretzky EDM 35 + 89 = 124", "Lemieux PIT 45 + 54 = 99", "Yzerman DET 42 + 56 = 98" ,"Kurri EDM 37 + 53 = 90", "Semenko EDM 4 + 12 = 16",])