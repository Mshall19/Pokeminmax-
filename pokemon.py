from dataclasses import dataclass
from typing import List

@dataclass
class Move:
    name: str
    move_type: str  # e.g., "fire", "water"
    power: int
    accuracy: int = 100  # Siempre acertará en este proyecto

@dataclass
class Pokemon:
    name: str
    pokemon_type: str  # o List[str] para tipos duales
    max_hp: int
    current_hp: int
    moves: List[Move]
    speed: int  # Para determinar orden de ataque
    
    def is_fainted(self) -> bool:
        return self.current_hp <= 0
    
    def available_moves(self) -> List[Move]:
        return [move for move in self.moves]