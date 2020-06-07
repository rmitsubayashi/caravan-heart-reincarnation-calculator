class ExperiencePoints:
    def __init__(self, monster_name, table):
        self.monster_name = monster_name
        self.table = table

class ExperienceTable:
    def __init__(self):
        self.hp = []
        self.mp = []
        self.attack = []
        self.defense = []
        self.speed = []
        self.intelligence = []

class ExperienceTableRow:
    def __init__(self, level_reached, experience_required, amount):
        self.level_reached = level_reached
        self.experience_required = experience_required
        self.amount = amount