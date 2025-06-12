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
        self.geometry("800x600")
        self.configure(bg='#2c3e50')
        
        self.player_trainer = player_trainer
        self.ai_trainer = ai_trainer
        
        # Pokémon actuales en batalla
        self.current_player_pokemon = player_trainer.current_pokemon()
        self.current_ai_pokemon = ai_trainer.current_pokemon()
        
        self.setup_ui()
        self.update_battle_display()
        
        # Centrar la ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configura los elementos de la interfaz gráfica"""
        # Frame principal
        main_frame = tk.Frame(self, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame para Pokémon
        pokemon_frame = tk.Frame(main_frame, bg='#2c3e50')
        pokemon_frame.pack(fill=tk.X, pady=20)
        
        # Pokémon del jugador (izquierda)
        self.player_frame = tk.Frame(pokemon_frame, bg='#2c3e50')
        self.player_frame.pack(side=tk.LEFT, expand=True)
        
        # Pokémon de la IA (derecha)
        self.ai_frame = tk.Frame(pokemon_frame, bg='#2c3e50')
        self.ai_frame.pack(side=tk.RIGHT, expand=True)
        
        # Barras de salud
        self.health_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.health_frame.pack(fill=tk.X, pady=10)
        
        # Botones de ataque
        self.buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.buttons_frame.pack(fill=tk.X, pady=20)
        
        # Configurar elementos específicos
        self.setup_pokemon_display()
        self.setup_health_bars()
        self.setup_attack_buttons()

    def setup_pokemon_display(self):
        """Configura los sprites y nombres de los Pokémon"""
        # Jugador
        self.player_sprite = tk.Label(self.player_frame, bg='#2c3e50')
        self.player_sprite.pack()
        
        self.player_name = tk.Label(
            self.player_frame, 
            text="", 
            font=("Arial", 16, "bold"), 
            bg='#2c3e50', 
            fg='white'
        )
        self.player_name.pack()
        
        # IA
        self.ai_sprite = tk.Label(self.ai_frame, bg='#2c3e50')
        self.ai_sprite.pack()
        
        self.ai_name = tk.Label(
            self.ai_frame, 
            text="", 
            font=("Arial", 16, "bold"), 
            bg='#2c3e50', 
            fg='white'
        )
        self.ai_name.pack()

    def setup_health_bars(self):
        """Configura las barras de salud"""
        # Jugador
        tk.Label(
            self.health_frame, 
            text="PS:", 
            font=("Arial", 12), 
            bg='#2c3e50', 
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        self.player_health = tk.Label(
            self.health_frame, 
            text="100/100", 
            font=("Arial", 12), 
            bg='#2c3e50', 
            fg='white'
        )
        self.player_health.pack(side=tk.LEFT)
        
        # Separador
        tk.Label(
            self.health_frame, 
            text="vs", 
            font=("Arial", 14, "bold"), 
            bg='#2c3e50', 
            fg='white'
        ).pack(side=tk.LEFT, padx=20)
        
        # IA
        self.ai_health = tk.Label(
            self.health_frame, 
            text="100/100", 
            font=("Arial", 12), 
            bg='#2c3e50', 
            fg='white'
        )
        self.ai_health.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            self.health_frame, 
            text="PS:", 
            font=("Arial", 12), 
            bg='#2c3e50', 
            fg='white'
        ).pack(side=tk.LEFT)

    def setup_attack_buttons(self):
        """Configura los botones de ataque"""
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text=f"Ataque {i+1}",
                font=("Arial", 12),
                width=15,
                command=lambda idx=i: self.player_attack(idx),
                state=tk.DISABLED
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=5)
            
            # Guardar referencia a los botones
            if not hasattr(self, 'attack_buttons'):
                self.attack_buttons = []
            self.attack_buttons.append(btn)

    def update_battle_display(self):
        """Actualiza toda la información de la batalla"""
        # Actualizar sprites
        self.update_sprite(self.player_sprite, self.current_player_pokemon)
        self.update_sprite(self.ai_sprite, self.current_ai_pokemon)
        
        # Actualizar nombres
        self.player_name.config(text=self.current_player_pokemon.name)
        self.ai_name.config(text=self.current_ai_pokemon.name)
        
        # Actualizar salud
        self.player_health.config(
            text=f"{self.current_player_pokemon.current_hp}/{self.current_player_pokemon.max_hp}"
        )
        self.ai_health.config(
            text=f"{self.current_ai_pokemon.current_hp}/{self.current_ai_pokemon.max_hp}"
        )
        
        # Actualizar botones de ataque
        self.update_attack_buttons()

    def update_sprite(self, label, pokemon):
        """Actualiza el sprite de un Pokémon"""
        if not label.winfo_exists():
            return  # ❌ El widget fue destruido

        sprite_path = f"sprites/{pokemon.id}.png"
        if os.path.exists(sprite_path):
            img = Image.open(sprite_path).resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo  # ✅ mantener referencia
        else:
            label.config(text="No sprite", image='')


    def update_attack_buttons(self):
        """Actualiza los botones de ataque con los movimientos disponibles"""
        for i, move in enumerate(self.current_player_pokemon.moves):
            if i < len(self.attack_buttons):
                self.attack_buttons[i].config(
                    text=move['name'],
                    state=tk.NORMAL
                )

    def player_attack(self, move_index):
        """Maneja el ataque del jugador"""
        if move_index >= len(self.current_player_pokemon.moves):
            return
            
        move = self.current_player_pokemon.moves[move_index]
        
        # Deshabilitar botones durante el turno
        for btn in self.attack_buttons:
            btn.config(state=tk.DISABLED)
        
        # Aplicar ataque
        damage = self.calculate_damage(self.current_player_pokemon, self.current_ai_pokemon, move)
        self.current_ai_pokemon.receive_damage(damage)
        
        # Verificar si el Pokémon de la IA fue derrotado
        if self.current_ai_pokemon.is_fainted():
            self.handle_fainted_pokemon(self.ai_trainer, is_ai=True)
            if self.check_battle_end():
                return
        
        # Turno de la IA
        self.ai_turn()
        
        # Actualizar interfaz
        self.update_battle_display()

    def ai_turn(self):
        """Maneja el turno de la IA"""
        best_move = obtener_mejor_ataque(self.ai_trainer, self.player_trainer)
        if best_move:
            damage = self.calculate_damage(self.current_ai_pokemon, self.current_player_pokemon, best_move)
            self.current_player_pokemon.receive_damage(damage)
            
            # Verificar si el Pokémon del jugador fue derrotado
            if self.current_player_pokemon.is_fainted():
                self.handle_fainted_pokemon(self.player_trainer, is_ai=False)
                self.check_battle_end()

    def calculate_damage(self, attacker, defender, move):
        """Calcula el daño de un ataque"""
        # Implementación básica - puedes mejorarla con tu tabla de tipos
        base_damage = move['power']
        type_multiplier = 1.0  # Aquí deberías implementar tu tabla de tipos
        
        return int(base_damage * type_multiplier)

    def handle_fainted_pokemon(self, trainer, is_ai):
        """Maneja un Pokémon debilitado"""
        if trainer.switch_to_next_available():
            if is_ai:
                self.current_ai_pokemon = trainer.current_pokemon()
            else:
                self.current_player_pokemon = trainer.current_pokemon()
        else:
            # No quedan Pokémon disponibles
            pass

    def check_battle_end(self):
        """Verifica si la batalla ha terminado"""
        if self.player_trainer.has_lost():
            messagebox.showinfo("Batalla terminada", "¡Has perdido la batalla!")
            self.destroy()
            return True
        elif self.ai_trainer.has_lost():
            messagebox.showinfo("Batalla terminada", "¡Has ganado la batalla!")
            self.destroy()
            return True
        return False