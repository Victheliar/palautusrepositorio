class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.team = dict['team']
        self.score = self.goals + self.assists
    
    def __str__(self):
        return f"{self.name:20}{self.team:20} {self.goals} + {self.assists} = {self.score}"
