from copy import deepcopy
from battle import apply_move
from battle import get_type_multiplier

def calculate_type_advantage(attacker, defender):
    """
    Evalúa la ventaja de tipo del mejor movimiento del atacante contra el defensor.
    Si el atacante no tiene movimientos válidos, retorna 0.
    """
    if not attacker.moves:
        return 0

    # Usar el movimiento que cause más daño teórico
    best_multiplier = 0
    for move in attacker.moves:
        multiplier = get_type_multiplier(move['type'], defender.types)
        if multiplier > best_multiplier:
            best_multiplier = multiplier

    return best_multiplier - 1  # Ajuste: 1 significa sin ventaja


def evaluate(trainer_ai, trainer_player):
    """Función de evaluación mejorada"""
    # Ponderar Pokémon activo más que los reservas
    active_weight = 2.0
    reserve_weight = 0.5
    
    ai_active = trainer_ai.active_pokemon
    ai_score = active_weight * ai_active.current_hp
    ai_score += reserve_weight * sum(
        p.current_hp for p in trainer_ai.pokemons 
        if p != ai_active and not p.is_fainted()
    )
    
    player_active = trainer_player.active_pokemon
    player_score = active_weight * player_active.current_hp
    player_score += reserve_weight * sum(
        p.current_hp for p in trainer_player.pokemons 
        if p != player_active and not p.is_fainted()
    )
    
    # Considerar ventaja de tipo
    type_advantage = calculate_type_advantage(ai_active, player_active)
    
    return (ai_score - player_score) * (1 + type_advantage)

def minimax(ai, player, depth, alpha, beta, maximizing):
    """Algoritmo minimax con optimizaciones"""
    # Condición de terminación mejorada
    if depth == 0 or ai.has_lost() or player.has_lost():
        return evaluate(ai, player), None
    
    current_trainer = ai if maximizing else player
    best_value = float('-inf') if maximizing else float('inf')
    best_move = None
    
    # Ordenar movimientos por poder descendente (mejora la poda)
    moves = sorted(
        current_trainer.active_pokemon.moves,
        key=lambda m: m['power'],
        reverse=maximizing
    )
    
    for move in moves:
        # Simulación del movimiento
        ai_copy = deepcopy(ai)
        player_copy = deepcopy(player)
        
        attacker = ai_copy if maximizing else player_copy
        defender = player_copy if maximizing else ai_copy
        
        apply_move(attacker.active_pokemon, defender.active_pokemon, move)
        
        # Manejo de Pokémon debilitado
        if defender.active_pokemon.is_fainted():
            if not defender.switch_to_next_available():
                # Fin de batalla si no hay reemplazo
                return evaluate(ai_copy, player_copy), move
        
        # Llamada recursiva
        eval_score, _ = minimax(
            ai_copy, 
            player_copy, 
            depth-1, 
            alpha, 
            beta, 
            not maximizing
        )
        
        # Actualizar mejor movimiento
        if (maximizing and eval_score > best_value) or (not maximizing and eval_score < best_value):
            best_value = eval_score
            best_move = move
            
            # Poda alfa-beta
            if maximizing:
                alpha = max(alpha, best_value)
            else:
                beta = min(beta, best_value)
            
            if beta <= alpha:
                break
    
    return best_value, best_move

def obtener_mejor_ataque(trainer_ai, trainer_player, depth=3):
    """Función principal con profundidad configurable"""
    _, best_move = minimax(
        trainer_ai,
        trainer_player,
        depth=depth,
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing=True
    )
    return best_move