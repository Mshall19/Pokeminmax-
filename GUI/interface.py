import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datos.cargar_desde_excel import cargar_pokemones_desde_excel
from GUI.battle_screen import BattleScreen
from pokemon import crear_pokemon_por_id
import random
from trainer import Trainer
from pokemon import crear_pokemon_por_id

TYPE_EMOJIS = {
    "grass": "🌿", "fire": "🔥", "water": "💧", "electric": "⚡",
    "bug": "🐛", "normal": "🔘", "poison": "☠️", "ground": "🌍",
    "fighting": "🥊", "psychic": "🧠", "rock": "🪨", "ghost": "👻",
    "ice": "❄️", "dragon": "🐉", "fairy": "🧚", "flying": "🕊️"
}

MAX_SELECCIONADOS = 3
TOTAL_POKEMONS = 151


class PokeMinMaxGUI:
    def __init__(self, root, player_trainer, ai_trainer):
        self.root = root
        self.player_trainer = player_trainer
        self.ai_trainer = ai_trainer

        # ✅ Inicializar estructuras internas
        self.selected_pokemon_ids = set()
        self.pokemon_photos = {}
        self.pokemon_data = {}
        self.checkbox_vars = {}
        self.pokemon_cards = {}

    def setup_interface(self):
        # Nombre jugador
        name_frame = tk.Frame(self.root)
        name_frame.pack(pady=10)
        tk.Label(name_frame, text="Nombre del jugador:", font=("Arial", 14)).pack(side="left", padx=5)
        self.player_name_entry = tk.Entry(name_frame, font=("Arial", 14), width=30)
        self.player_name_entry.pack(side="left")

        # Buscador de Pokémon
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Buscar Pokémon:", font=("Arial", 12)).pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filtrar_pokemones)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        self.search_entry.pack(side="left")

        # Contenedor galería con scroll
        self.gallery_canvas = tk.Canvas(self.root, height=450)
        self.gallery_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.gallery_canvas.yview)
        self.scrollbar.pack(side="left", fill="y", pady=10)

        self.gallery_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.gallery_frame = tk.Frame(self.gallery_canvas)
        self.gallery_canvas.create_window((0, 0), window=self.gallery_frame, anchor="nw")
        self.gallery_frame.bind("<Configure>", lambda e: self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all")))

        # Botones
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10, fill="x")
        tk.Button(btn_frame, text="Borrar selección", font=("Arial", 12), command=self.clear_selection).pack()

        self.battle_button = tk.Button(self.root, text="¡Iniciar batalla!", font=("Arial", 16), command=self.launch_battle, state="disabled")
        self.battle_button.pack(pady=10)

        # ✅ Cargar Pokémon al final de la interfaz
        self.cargar_todos_pokemones()

    def cargar_todos_pokemones(self):
        self.todos_los_pokemones = cargar_pokemones_desde_excel()

        for p in self.todos_los_pokemones[:TOTAL_POKEMONS]:
            try:
                sprite_response = requests.get(p.sprite_url)
                image = Image.open(BytesIO(sprite_response.content)).resize((96, 96), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.pokemon_photos[p.id] = photo

                self.pokemon_data[p.id] = {
                    "name": p.name,
                    "type_display": " ".join(TYPE_EMOJIS.get(t, "") for t in p.types),
                    "photo": photo
                }
            except Exception as e:
                print(f"❌ Error cargando sprite de {p.name}: {e}")

        self.mostrar_pokemones_filtrados()

    def mostrar_pokemones_filtrados(self):
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()
        self.pokemon_cards.clear()

        filtro = self.search_var.get().strip().lower()

        columnas = 4
        fila = 0
        columna = 0

        for pid, pdata in self.pokemon_data.items():
            if filtro in pdata["name"].lower():
                card = tk.Frame(self.gallery_frame, relief="ridge", borderwidth=2, padx=50, pady=5)
                card.grid(row=fila, column=columna, padx=20, pady=10, sticky="nsew")

                # Imagen
                label_img = tk.Label(card, image=pdata["photo"])
                label_img.image = pdata["photo"]  # ✅ mantener referencia
                label_img.pack(padx=10)

                # Nombre y tipo
                tk.Label(card, text=f"{pdata['name']} {pdata['type_display']}", font=("Arial", 14)).pack(pady=5)

                var = tk.IntVar(value=1 if pid in self.selected_pokemon_ids else 0)
                self.checkbox_vars[pid] = var

                def on_toggle(pid=pid, v=var):
                    if v.get() == 1:
                        if len(self.selected_pokemon_ids) >= MAX_SELECCIONADOS:
                            messagebox.showwarning("Pokeminmax", f"Solo puedes seleccionar {MAX_SELECCIONADOS} Pokémon.")
                            v.set(0)
                            return
                        self.selected_pokemon_ids.add(pid)
                    else:
                        self.selected_pokemon_ids.discard(pid)
                    self.update_battle_button()

                cb = tk.Checkbutton(card, variable=var, command=on_toggle)
                cb.pack(pady=5)

                self.pokemon_cards[pid] = card

                columna += 1
                if columna == columnas:
                    columna = 0
                    fila += 1

    def update_battle_button(self):
        if len(self.selected_pokemon_ids) == MAX_SELECCIONADOS:
            self.battle_button.config(state="normal")
        else:
            self.battle_button.config(state="disabled")

    def clear_selection(self):
        self.selected_pokemon_ids.clear()
        for var in self.checkbox_vars.values():
            var.set(0)
        self.update_battle_button()
        messagebox.showinfo("Pokeminmax", "Selección de Pokémon borrada.")

    def filtrar_pokemones(self, *args):
        self.mostrar_pokemones_filtrados()

    def launch_battle(self):
        from trainer import Trainer
        from pokemon import crear_pokemon_por_id

        selected_ids = list(self.selected_pokemon_ids)

        # Crear nuevos Pokémon del jugador
        equipo_jugador = [crear_pokemon_por_id(pid, self.todos_los_pokemones) for pid in selected_ids]
        player_trainer = Trainer("Jugador", equipo_jugador, is_ai=False)

        # Crear nuevos Pokémon aleatorios para la IA
        pokemons_disponibles = [p.id for p in self.todos_los_pokemones]
        equipo_ia_ids = random.sample(pokemons_disponibles, 3)
        equipo_ia = [crear_pokemon_por_id(pid, self.todos_los_pokemones) for pid in equipo_ia_ids]
        ai_trainer = Trainer("IA", equipo_ia, is_ai=True)

        # Lanzar batalla
        battle_window = tk.Toplevel(self.root)
        BattleScreen(battle_window, player_trainer, ai_trainer)



def launch_gui(player_trainer, ai_trainer):
    root = tk.Tk()
    root.geometry("1400x800")
    app = PokeMinMaxGUI(root, player_trainer, ai_trainer)
    app.setup_interface()
    root.mainloop()
