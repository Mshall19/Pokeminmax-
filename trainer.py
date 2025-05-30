class Trainer:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = pokemons
        self.active_index = 0

    @property
    def active_pokemon(self):
        return self.pokemons[self.active_index]

    def has_available_pokemon(self):
        return any(not p.is_fainted() for p in self.pokemons)

    def switch_to_next_available(self):
        for i, p in enumerate(self.pokemons):
            if not p.is_fainted():
                self.active_index = i
                return True
        return False
