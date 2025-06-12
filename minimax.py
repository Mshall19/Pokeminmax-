from copy import deepcopy
from battle import apply_move
from battle import get_type_multiplier

def calculate_type_advantage(attacker, defender):
    if not attacker.moves:
        return 0
    best_multiplier = 0
    for move in attacker.moves:
        multiplier = get_type_multiplier(move['type'], defender.types)
        if multiplier > best_multiplier:
            best_multiplier = multiplier
    return best_multiplier - 1

def evaluate(trainer_ai, trainer_player):
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
    type_advantage = calculate_type_advantage(ai_active, player_active)
    return (ai_score - player_score) * (1 + type_advantage)

def minimax(ai, player, depth, alpha, beta, maximizing):
    if depth == 0 or ai.has_lost() or player.has_lost():
        return evaluate(ai, player), None
    current_trainer = ai if maximizing else player
    best_value = float('-inf') if maximizing else float('inf')
    best_move = None
    moves = sorted(
        current_trainer.active_pokemon.moves,
        key=lambda m: m['power'],
        reverse=maximizing
    )
    for move in moves:
        ai_copy = deepcopy(ai)
        player_copy = deepcopy(player)
        attacker = ai_copy if maximizing else player_copy
        defender = player_copy if maximizing else ai_copy
        apply_move(attacker.active_pokemon, defender.active_pokemon, move)
        if defender.active_pokemon.is_fainted():
            if not defender.switch_to_next_available():
                return evaluate(ai_copy, player_copy), move
        eval_score, _ = minimax(
            ai_copy, 
            player_copy, 
            depth-1, 
            alpha, 
            beta, 
            not maximizing
        )
        if (maximizing and eval_score > best_value) or (not maximizing and eval_score < best_value):
            best_value = eval_score
            best_move = move
            if maximizing:
                alpha = max(alpha, best_value)
            else:
                beta = min(beta, best_value)
            if beta <= alpha:
                break
    return best_value, best_move

def obtener_mejor_ataque(trainer_ai, trainer_player, depth=3):
    _, best_move = minimax(
        trainer_ai,
        trainer_player,
        depth=depth,
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing=True
    )
    return best_move