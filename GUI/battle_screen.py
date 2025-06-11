import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

from minimax import obtener_mejor_ataque
from pokemon import crear_pokemon_por_id
from trainer import Entrenador

class BattleScreen:
    def __init__(self, master, nombre_jugador, ids_seleccionados):
        self.master = tk.Toplevel(master)
        self.master.title("¡Batalla Pokémon!")
        self.master.geometry("1000x600")
        self.master.resizable(False, False)

        self.jugador = Entrenador(nombre_jugador, [crear_pokemon_por_id(i) for i in ids_seleccionados])

        enemigos_ids = random.sample(range(1, 10), 3)
        self.rival = Entrenador("IA Rival", [crear_pokemon_por_id(i) for i in enemigos_ids])

        self.pokemon_jugador = self.jugador.pokemones[0]
        self.pokemon_rival = self.rival.pokemones[0]

        self.setup_ui()
        self.actualizar_interface()

    def setup_ui(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20)

        # Sprites
        self.img_jugador_label = tk.Label(self.frame)
        self.img_jugador_label.grid(row=0, column=0, padx=50)

        self.img_rival_label = tk.Label(self.frame)
        self.img_rival_label.grid(row=0, column=2, padx=50)

        # Info nombres y vida
        self.info_jugador = tk.Label(self.frame, font=("Arial", 14))
        self.info_jugador.grid(row=1, column=0)

        self.info_rival = tk.Label(self.frame, font=("Arial", 14))
        self.info_rival.grid(row=1, column=2)

        # Botones de ataque
        self.boton_frame = tk.Frame(self.master)
        self.boton_frame.pack(pady=20)

        self.botones_ataque = []
        for i in range(4):
            btn = tk.Button(self.boton_frame, text=f"Ataque {i+1}", font=("Arial", 12), width=20, command=lambda i=i: self.realizar_turno(i))
            btn.grid(row=i//2, column=i%2, padx=10, pady=5)
            self.botones_ataque.append(btn)

    def actualizar_interface(self):
        # Actualizar sprites
        self.sprite_jugador = self.cargar_sprite(self.pokemon_jugador.id)
        self.sprite_rival = self.cargar_sprite(self.pokemon_rival.id)

        self.img_jugador_label.config(image=self.sprite_jugador)
        self.img_jugador_label.image = self.sprite_jugador

        self.img_rival_label.config(image=self.sprite_rival)
        self.img_rival_label.image = self.sprite_rival

        # Info
        self.info_jugador.config(text=f"{self.pokemon_jugador.nombre} ({self.pokemon_jugador.hp_actual}/{self.pokemon_jugador.hp})")
        self.info_rival.config(text=f"{self.pokemon_rival.nombre} ({self.pokemon_rival.hp_actual}/{self.pokemon_rival.hp})")

        # Botones de ataques
        for i, ataque in enumerate(self.pokemon_jugador.ataques):
            self.botones_ataque[i].config(text=ataque.nombre, state="normal")

    def cargar_sprite(self, poke_id):
        ruta = os.path.join("sprites", f"{poke_id}.png")
        if not os.path.exists(ruta):
            return None
        img = Image.open(ruta).resize((150, 150), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def realizar_turno(self, idx_ataque):
        ataque_jugador = self.pokemon_jugador.ataques[idx_ataque]
        resultado = self.pokemon_jugador.atacar(self.pokemon_rival, ataque_jugador)

        if self.pokemon_rival.hp_actual <= 0:
            messagebox.showinfo("Pokeminmax", f"¡{self.pokemon_rival.nombre} ha sido derrotado!")
            return

        # Turno IA
        mejor_ataque = obtener_mejor_ataque(self.pokemon_rival, self.pokemon_jugador)
        if mejor_ataque:
            self.pokemon_rival.atacar(self.pokemon_jugador, mejor_ataque)

        if self.pokemon_jugador.hp_actual <= 0:
            messagebox.showinfo("Pokeminmax", f"¡{self.pokemon_jugador.nombre} ha sido derrotado!")
            return

        self.actualizar_interface()