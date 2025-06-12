class Trainer:  # No Entrenador
    def __init__(self, name, pokemons, is_ai=False):
        self.name = name
        self.pokemons = pokemons
        self.is_ai = is_ai
        self.active_index = 0

    def current_pokemon(self):
        return self.pokemons[self.active_index]

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
    
    def has_lost(self):
        return not self.has_available_pokemon()


