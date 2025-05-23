from typing import List
from pokemon import Pokemon

class Trainer:
    def __init__(self, name: str, pokemon_team: List[Pokemon], is_ai: bool = False):
        self.name = name
        self.pokemon_team = pokemon_team
        self.active_pokemon = pokemon_team[0] if pokemon_team else None
        self.is_ai = is_ai
    
    def has_available_pokemon(self) -> bool:
        return any(not pokemon.is_fainted() for pokemon in self.pokemon_team)
    
    def switch_pokemon(self, index: int) -> bool:
        """Cambia al Pokémon activo. Devuelve True si fue exitoso."""
        if 0 <= index < len(self.pokemon_team) and not self.pokemon_team[index].is_fainted():
            self.active_pokemon = self.pokemon_team[index]
            return True
        return False