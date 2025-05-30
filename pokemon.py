class Pokemon:
    def __init__(self, name, types, hp, moves):
        self.name = name
        self.types = types
        self.max_hp = hp
        self.hp = hp
        self.moves = moves

    def is_fainted(self):
        return self.hp <= 0

    def receive_damage(self, damage):
        self.hp = max(self.hp - damage, 0)
