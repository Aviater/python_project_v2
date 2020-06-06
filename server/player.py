class Player:
    def __init__(self, name, hitpoints):
        self.name = name
        self.hitpoints = hitpoints
        print(f'{self.name} was created.')

    def get_props(self):
        return self.name, self.hitpoints
        
    def reduce_health(self, amount):
        if self.hitpoints <= amount:
            print(f'{self.name} has won the game!')
            return
        
        self.hitpoints = self.hitpoints - amount