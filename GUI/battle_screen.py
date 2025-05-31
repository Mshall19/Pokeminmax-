from tkinter import *
from api import get_pokemon_data  # o tu función para obtener los datos de pokémon
from pokemon import Pokemon
from trainer import Trainer
from battle import Battle

class BattleScreen:
    def __init__(self, root, player_name, selected_ids):
        self.window = Toplevel(root)
        self.window.title("¡Batalla Pokémon!")
        self.window.geometry("800x600")

        self.player_name = player_name
        self.player_pokemon = [self.create_pokemon(pid) for pid in selected_ids]
        self.enemy_pokemon = [self.create_pokemon(pid) for pid in self.get_enemy_ids(selected_ids)]

        self.player = Trainer(player_name, self.player_pokemon)
        self.enemy = Trainer("IA", self.enemy_pokemon, is_ai=True)
        self.battle = Battle(self.player, self.enemy)

        self.setup_interface()
        self.update_display()

    def create_pokemon(self, poke_id):
        # Aquí deberías tener algo como una función que devuelva una instancia de la clase Pokémon
        poke_data = get_pokemon_data(poke_id)
        return Pokemon.from_api_data(poke_data)  # o lo que uses en tu proyecto

    def get_enemy_ids(self, selected_ids):
        # IDs entre 1 y 9 que no estén en los seleccionados
        all_ids = list(range(1, 10))
        return [pid for pid in all_ids if pid not in selected_ids][:3]

    def setup_interface(self):
        self.info_label = Label(self.window, font=("Arial", 16))
        self.info_label.pack(pady=20)

        self.attack_button = Button(self.window, text="Atacar", font=("Arial", 14), command=self.player_attack)
        self.attack_button.pack(pady=10)

        self.status_text = Text(self.window, height=15, width=80, state="disabled", font=("Courier", 12))
        self.status_text.pack(pady=10)

    def player_attack(self):
        result = self.battle.play_turn()
        self.update_display()
        self.log(result)

        if self.battle.is_over():
            winner = self.battle.get_winner()
            self.info_label.config(text=f"¡{winner.name} ha ganado!")
            self.attack_button.config(state="disabled")

    def update_display(self):
        p_poke = self.player.current_pokemon()
        e_poke = self.enemy.current_pokemon()
        self.info_label.config(
            text=f"{p_poke.name} ({p_poke.current_hp} HP) vs {e_poke.name} ({e_poke.current_hp} HP)"
        )

    def log(self, text):
        self.status_text.config(state="normal")
        self.status_text.insert("end", text + "\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")
