type_chart = {
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

def get_type_multiplier(attack_type, target_types):
    multiplier = 1.0
    for t in target_types:
        multiplier *= type_chart.get(attack_type, {}).get(t, 1.0)
    return multiplier

def calculate_damage(attacker, defender, move):
    base_power = move['power']
    multiplier = get_type_multiplier(move['type'], defender.types)
    return int(base_power * multiplier)

def apply_move(attacker, defender, move):
    damage = calculate_damage(attacker, defender, move)
    defender.receive_damage(damage)

class Battle:
    def __init__(self, player_trainer, enemy_trainer):
        self.player = player_trainer
        self.enemy = enemy_trainer
        self.turn = 0  # 0: jugador, 1: IA

    def play_turn(self):
        # Simulación de turno
        if self.turn == 0:
            result = self.player_attack()
        else:
            result = self.enemy_attack()
        self.turn = 1 - self.turn
        return result

    def player_attack(self):
        enemy = self.enemy.current_pokemon()
        player = self.player.current_pokemon()
        damage = 10  # Simplificado
        enemy.current_hp -= damage
        return f"{player.name} atacó a {enemy.name} causando {damage} daño."

    def enemy_attack(self):
        enemy = self.enemy.current_pokemon()
        player = self.player.current_pokemon()
        damage = 10
        player.current_hp -= damage
        return f"{enemy.name} atacó a {player.name} causando {damage} daño."

    def is_over(self):
        return self.player.has_lost() or self.enemy.has_lost()

    def get_winner(self):
        return self.enemy if self.player.has_lost() else self.player
