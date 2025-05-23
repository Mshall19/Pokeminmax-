from pokemon import Pokemon
from trainer import Trainer
from battle import Battle
from minimax import MinimaxAI
from api import PokeAPI

class PokemonCLI:
    def __init__(self):
        self.player = None
        self.opponent = None
        self.battle = None
    
    def start_game(self):
        print("===== POKEMINMAX =====")
        print("Un combate Pokémon estratégico con IA usando Minimax")
        
        # Configurar equipos
        self.setup_teams()
        
        # Iniciar combate
        self.battle = Battle(self.player, self.opponent)
        self.run_battle()
    
    def setup_teams(self):
        api = PokeAPI()
        
        print("\nConfiguración del equipo del jugador:")
        player_name = input("Ingresa tu nombre: ")
        player_team = []
        
        # Permitir al usuario elegir sus Pokémon
        for i in range(3):  # Equipos de 3 Pokémon por simplicidad
            while True:
                pokemon_name = input(f"\nElige el Pokémon #{i+1} (nombre en inglés): ")
                pokemon = api.create_pokemon_from_api(pokemon_name)
                if pokemon:
                    player_team.append(pokemon)
                    print(f"¡{pokemon.name} añadido a tu equipo!")
                    break
                print("Pokémon no encontrado. Intenta de nuevo.")
        
        self.player = Trainer(player_name, player_team)
        
        # Equipo oponente (puede ser aleatorio o predefinido)
        print("\nConfiguración del equipo oponente:")
        opponent_team = []
        default_opponent_pokemon = ["charizard", "blastoise", "venusaur"]  # Clásicos
        
        for poke_name in default_opponent_pokemon:
            pokemon = api.create_pokemon_from_api(poke_name)
            if pokemon:
                opponent_team.append(pokemon)
        
        self.opponent = Trainer("Líder IA", opponent_team, is_ai=True)
    
    def run_battle(self):
        print("\n¡Comienza el combate!")
        print(f"{self.player.name} vs {self.opponent.name}")
        
        while True:
            # Turno del jugador
            player_result = self.player_turn()
            if player_result:  # El combate terminó
                break
            
            # Turno de la IA
            ai_result = self.ai_turn()
            if ai_result:  # El combate terminó
                break
    
    def player_turn(self) -> bool:
        """Maneja el turno del jugador. Devuelve True si el combate terminó."""
        print("\n=== TU TURNO ===")
        active_pokemon = self.player.active_pokemon
        print(f"Pokémon activo: {active_pokemon.name} (PS: {active_pokemon.current_hp}/{active_pokemon.max_hp})")
        
        # Mostrar movimientos disponibles
        print("\nMovimientos disponibles:")
        for i, move in enumerate(active_pokemon.moves):
            print(f"{i+1}. {move.name} (Tipo: {move.move_type}, Poder: {move.power})")
        
        # Seleccionar movimiento
        while True:
            try:
                choice = int(input("Elige un movimiento (1-4): ")) - 1
                if 0 <= choice < len(active_pokemon.moves):
                    break
                print("Opción inválida. Intenta de nuevo.")
            except ValueError:
                print("Por favor ingresa un número.")
        
        # Ejecutar movimiento
        message, battle_over = self.battle.execute_move(self.player, choice, self.opponent)
        print(message)
        
        return battle_over
    
    def ai_turn(self) -> bool:
        """Maneja el turno de la IA. Devuelve True si el combate terminó."""
        print("\n=== TURNO DE LA IA ===")
        active_pokemon = self.opponent.active_pokemon
        print(f"Pokémon activo de la IA: {active_pokemon.name} (PS: {active_pokemon.current_hp}/{active_pokemon.max_hp})")
        
        # La IA elige el mejor movimiento usando Minimax
        minimax = MinimaxAI(self.battle)
        best_move = minimax.get_best_move()
        move = active_pokemon.moves[best_move]
        
        print(f"La IA usó {move.name}!")
        
        # Ejecutar movimiento
        message, battle_over = self.battle.execute_move(self.opponent, best_move, self.player)
        print(message)
        
        return battle_over