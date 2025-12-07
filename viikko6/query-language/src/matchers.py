class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True

class Or:
    def __init__(self, *matchers):
        self._matchers = matchers
    
    def test(self, player):
        for matcher in self._matchers:
            if matcher.test(player):
                return True
        return False

class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value

class All:
    def test(self, player):
        return True

class Not:
    def __init__(self, matcher):
        self.matcher = matcher
    
    def test(self, player):
        return not self.matcher.test(player)

class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr
    
    def test(self, player):
        player_value = getattr(player, self._attr)
        return player_value < self._value
    
class QueryBuilder:
    def __init__(self):
        self._matchers = []
        self._one_of = False
        
    def one_of(self, query1, query2):
        if not self._matchers:
            return All()
        if len(self._matchers) == 1:
            return self._matchers[0]
        return Or(*self._matchers)
        
    def build(self, one_of=False):
        # return All()
        if not self._matchers:
            return All()
        if len(self._matchers) == 1:
            return self._matchers[0]
        return And(*self._matchers)
    
    def plays_in(self, team):
        self._matchers.append(PlaysIn(team))
        return self
    
    def has_at_least(self, value, attr):
        self._matchers.append(HasAtLeast(value, attr))
        return self
    
    def has_fewer_than(self, value, attr):
        self._matchers.append(HasFewerThan(value, attr))
        return self