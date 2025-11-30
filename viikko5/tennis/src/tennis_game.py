class TennisGame:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0
        self.score2 = 0
        self.score_names = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}
        self.equal_names = {0: "Love-All", 1: "Fifteen-All", 2: "Thirty-All"}
        self.advantage_threshold = 4
        self.win_margin = 2

    def won_point(self, player):
        if player == self.player1:
            self.score1 = self.score1 + 1
        else:
            self.score2 = self.score2 + 1
    
    def get_tie(self):
        return self.equal_names.get(self.score1, "Deuce")
    
    def get_advantage(self, result):
        if result == 1:
            return "Advantage player1"
        if result == -1:
            return "Advantage player2"
    
    def get_win(self, result):
        if result >= self.win_margin:
            return "Win for player1"
        else:
            return "Win for player2"

    def get_score(self):
        score = ""
        if self.score1 == self.score2:
            score = self.get_tie()

        elif self.score1 >= self.advantage_threshold or self.score2 >= self.advantage_threshold:
            result = self.score1 - self.score2
            
            if result == -1 or result == 1:
                score = self.get_advantage(result)

            else:
                score = self.get_win(result)
        else:
            score = f"{self.score_names[self.score1]}-{self.score_names[self.score2]}"
        return score
