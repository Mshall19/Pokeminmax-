from typing import Dict
from copy import deepcopy
from battle import Battle

class MinimaxAI:
    def __init__(self, battle: Battle, depth: int = 3):
        self.battle = battle
        self.depth = depth
    
    def evaluate_state(self, battle_state: dict) -> float:
        """Función heurística para evaluar un estado del combate."""
        player_pokemon = battle_state['player']['active']
        opponent_pokemon = battle_state['opponent']['active']
        
        # Ponderaciones para los factores de evaluación
        hp_weight = 0.6
        type_advantage_weight = 0.3
        remaining_pokemon_weight = 0.1
        
        # Calcula ventaja en PS (0-1)
        hp_score = (opponent_pokemon['current_hp'] / opponent_pokemon['max_hp']) - \
                   (player_pokemon['current_hp'] / player_pokemon['max_hp'])
        
        # Calcula ventaja de tipo
        type_score = 0
        for move in player_pokemon['moves']:
            effectiveness = 1.0
            if move['type'] in battle_state['type_chart'] and \
               opponent_pokemon['type'] in battle_state['type_chart'][move['type']]:
                effectiveness = battle_state['type_chart'][move['type']][opponent_pokemon['type']]
            type_score += (effectiveness - 1)
        
        type_score = type_score / len(player_pokemon['moves']) if player_pokemon['moves'] else 0
        
        # Calcula ventaja en número de Pokémon restantes
        remaining_score = (battle_state['opponent']['remaining'] - battle_state['player']['remaining']) / 6
        
        # Combinación ponderada
        total_score = (hp_weight * hp_score + 
                      type_advantage_weight * type_score + 
                      remaining_pokemon_weight * remaining_score)
        
        return total_score
    
    def minimax(self, state: dict, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        if depth == 0 or state['game_over']:
            return self.evaluate_state(state)
        
        if maximizing_player:  # Es el turno de la IA
            max_eval = float('-inf')
            for move_idx in range(len(state['opponent']['active']['moves'])):
                new_state = self.simulate_move(state, 'opponent', move_idx)
                eval = self.minimax(new_state, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Poda alfa-beta
            return max_eval
        else:  # Es el turno del jugador
            min_eval = float('inf')
            for move_idx in range(len(state['player']['active']['moves'])):
                new_state = self.simulate_move(state, 'player', move_idx)
                eval = self.minimax(new_state, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Poda alfa-beta
            return min_eval
    
    def get_best_move(self) -> int:
        """Devuelve el índice del mejor movimiento según minimax."""
        battle_state = self.get_current_state()
        best_move = 0
        max_eval = float('-inf')
        
        for move_idx in range(len(battle_state['opponent']['active']['moves'])):
            new_state = self.simulate_move(battle_state, 'opponent', move_idx)
            eval = self.minimax(new_state, self.depth-1, float('-inf'), float('inf'), False)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move_idx
        
        return best_move
    
    def get_current_state(self) -> dict:
        """Convierte el estado actual del combate a un diccionario para minimax."""
        return {
            'player': {
                'active': {
                    'name': self.battle.player.active_pokemon.name,
                    'type': self.battle.player.active_pokemon.pokemon_type,
                    'current_hp': self.battle.player.active_pokemon.current_hp,
                    'max_hp': self.battle.player.active_pokemon.max_hp,
                    'moves': [{'name': m.name, 'type': m.move_type, 'power': m.power} 
                             for m in self.battle.player.active_pokemon.moves],
                },
                'remaining': sum(1 for p in self.battle.player.pokemon_team if not p.is_fainted()),
            },
            'opponent': {
                'active': {
                    'name': self.battle.opponent.active_pokemon.name,
                    'type': self.battle.opponent.active_pokemon.pokemon_type,
                    'current_hp': self.battle.opponent.active_pokemon.current_hp,
                    'max_hp': self.battle.opponent.active_pokemon.max_hp,
                    'moves': [{'name': m.name, 'type': m.move_type, 'power': m.power} 
                             for m in self.battle.opponent.active_pokemon.moves],
                },
                'remaining': sum(1 for p in self.battle.opponent.pokemon_team if not p.is_fainted()),
            },
            'type_chart': self.battle.type_chart,
            'game_over': not (self.battle.player.has_available_pokemon() and self.battle.opponent.has_available_pokemon()),
        }
    
    def simulate_move(self, state: dict, attacker: str, move_idx: int) -> dict:
        """Simula un movimiento y devuelve un nuevo estado."""
        new_state = deepcopy(state)
        attacker_data = new_state[attacker]['active']
        defender = 'opponent' if attacker == 'player' else 'player'
        defender_data = new_state[defender]['active']
        
        if move_idx >= len(attacker_data['moves']):
            return new_state  # Movimiento inválido, no cambia el estado
        
        move = attacker_data['moves'][move_idx]
        
        # Calcula efectividad
        effectiveness = 1.0
        if move['type'] in new_state['type_chart'] and defender_data['type'] in new_state['type_chart'][move['type']]:
            effectiveness = new_state['type_chart'][move['type']][defender_data['type']]
        
        # Calcula daño (simplificado)
        damage = int((move['power'] * effectiveness))
        
        # Aplica daño
        defender_data['current_hp'] = max(0, defender_data['current_hp'] - damage)
        
        # Verifica si el defensor fue debilitado
        if defender_data['current_hp'] <= 0:
            new_state[defender]['remaining'] -= 1
            new_state['game_over'] = new_state[defender]['remaining'] <= 0
        
        return new_state