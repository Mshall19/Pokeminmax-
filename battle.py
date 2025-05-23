from typing import Tuple, Dict
from pokemon import Pokemon, Move
from trainer import Trainer

class Battle:
    def __init__(self, player: Trainer, opponent: Trainer):
        self.player = player
        self.opponent = opponent
        self.type_chart = self.load_type_chart()
    
    @staticmethod
    def load_type_chart() -> Dict[str, Dict[str, float]]:
        # Simplificamos la tabla de tipos a los más comunes
        return {
            "normal": {"rock": 0.5, "ghost": 0},
            "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5},
            "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2},
            "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "flying": 0.5, "bug": 0.5, "rock": 2, "ground": 2},
            "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0},
            "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2},
            "fighting": {"normal": 2, "ice": 2, "rock": 2, "flying": 0.5, "psychic": 0.5},
            "poison": {"grass": 2, "poison": 0.5, "ground": 0.5},
            "ground": {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "rock": 2, "flying": 0},
            "flying": {"grass": 2, "electric": 0.5, "fighting": 2, "bug": 2, "rock": 0.5},
            "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5},
            "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "psychic": 2},
            "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2},
            "ghost": {"normal": 0, "psychic": 2, "ghost": 2},
            "dragon": {"dragon": 2}
        }
    
    def calculate_damage(self, attacker: Pokemon, move: Move, defender: Pokemon) -> int:
        """Calcula el daño basado en tipos y poder del movimiento."""
        effectiveness = 1.0
        
        # Obtener efectividad del tipo del movimiento contra el tipo del defensor
        if move.move_type in self.type_chart and defender.pokemon_type in self.type_chart[move.move_type]:
            effectiveness = self.type_chart[move.move_type][defender.pokemon_type]
        
        # Fórmula simplificada de daño
        damage = int((move.power * effectiveness))
        return max(1, damage)  # Mínimo 1 de daño
    
    def execute_move(self, attacker: Trainer, move_index: int, defender: Trainer) -> Tuple[str, bool]:
        """Ejecuta un movimiento y devuelve el resultado y si el combate terminó."""
        if attacker.active_pokemon.is_fainted() or not attacker.has_available_pokemon():
            return "El Pokémon atacante está debilitado.", True
        
        move = attacker.active_pokemon.moves[move_index]
        damage = self.calculate_damage(
            attacker.active_pokemon,
            move,
            defender.active_pokemon
        )
        
        defender.active_pokemon.current_hp -= damage
        result_message = f"{attacker.name}'s {attacker.active_pokemon.name} usó {move.name} y causó {damage} de daño!"
        
        if defender.active_pokemon.is_fainted():
            result_message += f"\n{defender.name}'s {defender.active_pokemon.name} se debilitó!"
            if not defender.has_available_pokemon():
                result_message += f"\n{attacker.name} gana el combate!"
                return result_message, True
        
        return result_message, False