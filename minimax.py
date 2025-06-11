from copy import deepcopy

def evaluate(trainer_ai, trainer_player):
    ai_score = sum(p.current_hp for p in trainer_ai.pokemons if not p.is_fainted())
    player_score = sum(p.current_hp for p in trainer_player.pokemons if not p.is_fainted())
    return ai_score - player_score


def minimax(ai, player, depth, alpha, beta, maximizing):
    if depth == 0 or not ai.has_available_pokemon() or not player.has_available_pokemon():
        return evaluate(ai, player), None

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        for move in ai.active_pokemon.moves:
            temp_player = deepcopy(player)
            temp_ai = deepcopy(ai)
            from battle import apply_move
            apply_move(temp_ai.active_pokemon, temp_player.active_pokemon, move)
            if temp_player.active_pokemon.is_fainted():
                temp_player.switch_to_next_available()
            eval_score, _ = minimax(temp_ai, temp_player, depth-1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in player.active_pokemon.moves:
            temp_player = deepcopy(player)
            temp_ai = deepcopy(ai)
            from battle import apply_move
            apply_move(temp_player.active_pokemon, temp_ai.active_pokemon, move)
            if temp_ai.active_pokemon.is_fainted():
                temp_ai.switch_to_next_available()
            eval_score, _ = minimax(temp_ai, temp_player, depth-1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


# ✅ Esta es la función que debes agregar al final del archivo
def obtener_mejor_ataque(trainer_ai, trainer_player):
    _, mejor_ataque = minimax(trainer_ai, trainer_player, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing=True)
    return mejor_ataque
