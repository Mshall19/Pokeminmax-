import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from minimax import obtener_mejor_ataque
from trainer import Trainer

class BattleScreen(tk.Toplevel):
    def __init__(self, master, player_trainer, ai_trainer):
        super().__init__(master)
        self.title("Pokémon Battle")
        self.geometry("1200x1000")

        self.bg_image = None
        if os.path.exists("GUI/bg.jpg"):
            image = Image.open("GUI/bg.jpg")
            image = image.resize((1200, 1000), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            background_label = tk.Label(self, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.player_trainer = player_trainer
        self.ai_trainer = ai_trainer

        self.current_player_pokemon = player_trainer.current_pokemon()
        self.current_ai_pokemon = ai_trainer.current_pokemon()

        self.setup_ui()
        self.update_battle_display()

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        self.main_frame = tk.Frame(self, bg='#2c3e50')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.pokemon_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        self.pokemon_frame.pack(fill=tk.X, pady=10)

        self.player_frame = tk.Frame(self.pokemon_frame, bg='#2c3e50')
        self.player_frame.pack(side=tk.LEFT, expand=True)

        self.ai_frame = tk.Frame(self.pokemon_frame, bg='#2c3e50')
        self.ai_frame.pack(side=tk.RIGHT, expand=True)

        self.health_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        self.health_frame.pack(fill=tk.X, pady=5)

        self.info_frame = tk.Frame(self.main_frame, bg='#34495e', width=500)
        self.info_frame.pack(pady=5)
        self.info_frame.pack_propagate(False)

        self.info_label = tk.Label(
            self.info_frame,
            text="La batalla ha comenzado.",
            font=("Arial", 12),
            bg='#34495e',
            fg='white'
        )
        self.info_label.pack(pady=5)

        self.buttons_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        self.buttons_frame.pack(fill=tk.X, pady=10)

        self.setup_pokemon_display()
        self.setup_health_bars()
        self.setup_attack_buttons()

    def setup_pokemon_display(self):
        self.player_sprite = tk.Label(self.player_frame, bg='#2c3e50')
        self.player_sprite.pack()

        self.player_name = tk.Label(self.player_frame, font=("Arial", 14), bg='#2c3e50', fg='white')
        self.player_name.pack()

        self.ai_sprite = tk.Label(self.ai_frame, bg='#2c3e50')
        self.ai_sprite.pack()

        self.ai_name = tk.Label(self.ai_frame, font=("Arial", 14), bg='#2c3e50', fg='white')
        self.ai_name.pack()

    def setup_health_bars(self):
        self.player_health = tk.Label(self.health_frame, font=("Arial", 12), bg='#2c3e50', fg='white')
        self.player_health.pack(side=tk.LEFT, padx=10)

        tk.Label(self.health_frame, text="vs", font=("Arial", 14), bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=10)

        self.ai_health = tk.Label(self.health_frame, font=("Arial", 12), bg='#2c3e50', fg='white')
        self.ai_health.pack(side=tk.LEFT, padx=10)

    def setup_attack_buttons(self):
        self.attack_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text=f"Ataque {i+1}",
                font=("Arial", 12),
                width=15,
                command=lambda idx=i: self.player_attack(idx)
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=5)
            self.attack_buttons.append(btn)

    def update_battle_display(self):
        if not self.player_sprite.winfo_exists():
            return  # ✅ Previene crash si el widget fue destruido

        self.update_sprite(self.player_sprite, self.current_player_pokemon)
        self.update_sprite(self.ai_sprite, self.current_ai_pokemon)

        self.player_name.config(text=self.current_player_pokemon.name)
        self.ai_name.config(text=self.current_ai_pokemon.name)

        self.player_health.config(
            text=f"{self.current_player_pokemon.current_hp}/{self.current_player_pokemon.max_hp} PS"
        )
        self.ai_health.config(
            text=f"{self.current_ai_pokemon.current_hp}/{self.current_ai_pokemon.max_hp} PS"
        )

        self.update_attack_buttons()


    def update_sprite(self, label, pokemon):
        sprite_path = f"sprites/{pokemon.id}.png"
        if os.path.exists(sprite_path):
            img = Image.open(sprite_path).resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo
        else:
            label.config(text="No sprite", image='')

    def update_attack_buttons(self):
        moves = self.current_player_pokemon.moves
        for i, btn in enumerate(self.attack_buttons):
            if i < len(moves):
                btn.config(text=moves[i]['name'], state=tk.NORMAL)
            else:
                btn.config(text="", state=tk.DISABLED)

    def player_attack(self, move_index):
        move = self.current_player_pokemon.moves[move_index]
        damage = self.calculate_damage(self.current_player_pokemon, self.current_ai_pokemon, move)
        self.current_ai_pokemon.receive_damage(damage)
        self.update_info_text(f"{self.current_player_pokemon.name} usó {move['name']} causando {damage} de daño.")

        if self.current_ai_pokemon.is_fainted():
            self.update_info_text(f"{self.current_ai_pokemon.name} ha sido derrotado.")
            self.handle_fainted_pokemon(self.ai_trainer, is_ai=True)
            if self.check_battle_end():
                return

        self.ai_turn()
        self.update_battle_display()

    def ai_turn(self):
        best_move = obtener_mejor_ataque(self.ai_trainer, self.player_trainer)
        if best_move:
            damage = self.calculate_damage(self.current_ai_pokemon, self.current_player_pokemon, best_move)
            self.current_player_pokemon.receive_damage(damage)
            self.update_info_text(f"{self.current_ai_pokemon.name} usó {best_move['name']} causando {damage} de daño.")

            if self.current_player_pokemon.is_fainted():
                self.update_info_text(f"{self.current_player_pokemon.name} ha sido derrotado.")
                self.handle_fainted_pokemon(self.player_trainer, is_ai=False)
                self.check_battle_end()

    def calculate_damage(self, attacker, defender, move):
        base_damage = move['power']
        type_multiplier = 1.0
        return int(base_damage * type_multiplier)

    def handle_fainted_pokemon(self, trainer, is_ai):
        if trainer.switch_to_next_available():
            if is_ai:
                self.current_ai_pokemon = trainer.current_pokemon()
            else:
                self.current_player_pokemon = trainer.current_pokemon()
        else:
            pass

    def check_battle_end(self):
        if self.player_trainer.has_lost():
            messagebox.showinfo("Batalla terminada", "¡Has perdido la batalla!")
            self.destroy()
            return True
        elif self.ai_trainer.has_lost():
            messagebox.showinfo("Batalla terminada", "¡Has ganado la batalla!")
            self.destroy()
            return True
        return False

    def update_info_text(self, text):
        self.info_label.config(text=text)
