import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datos.cargar_desde_excel import cargar_pokemones_desde_excel
from GUI.battle_screen import BattleScreen

TYPE_EMOJIS = {
    "grass": "🌿", "fire": "🔥", "water": "💧", "electric": "⚡",
    "bug": "🐛", "normal": "🔘", "poison": "☠️", "ground": "🌍",
    "fighting": "🥊", "psychic": "🧠", "rock": "🪨", "ghost": "👻",
    "ice": "❄️", "dragon": "🐉", "fairy": "🧚", "flying": "🕊️"
}

MAX_SELECCIONADOS = 3
TOTAL_POKEMONS = 50 # Desde ID 1 hasta 9


class PokeMinMaxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokeminmax")
        self.root.geometry("850x700")
        self.root.resizable(False, False)

        self.pokemon_photos = {}     # id -> PhotoImage
        self.checkbox_vars = {}      # id -> tk.IntVar()
        self.selected_pokemon_ids = set()
        self.pokemon_cards = {}      # id -> Frame (para cambiar estilo)
        self.pokemon_data = {}       # id -> datos para filtro

        self.setup_interface()
        self.cargar_todos_pokemones()

        self.root.mainloop()

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

        # Contenedor galería con scroll vertical
        self.gallery_canvas = tk.Canvas(self.root, height=450)
        self.gallery_canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.gallery_canvas.yview)
        self.scrollbar.pack(side="left", fill="y", pady=10)

        self.gallery_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.gallery_frame = tk.Frame(self.gallery_canvas)
        self.gallery_canvas.create_window((0, 0), window=self.gallery_frame, anchor="nw")

        self.gallery_frame.bind("<Configure>", lambda e: self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all")))

        # Botón limpiar selección
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10, fill="x")
        tk.Button(btn_frame, text="Borrar selección", font=("Arial", 12), command=self.clear_selection).pack()

        # Botón iniciar batalla
        self.battle_button = tk.Button(self.root, text="¡Iniciar batalla!", font=("Arial", 16), command=self.launch_battle, state="disabled")
        self.battle_button.pack(pady=10)

    def cargar_todos_pokemones(self):
        self.todos_los_pokemones = cargar_pokemones_desde_excel()

        for p in self.todos_los_pokemones[:TOTAL_POKEMONS]:  # Limita a los primeros 50 si quieres
            sprite_response = requests.get(p.sprite_url)
            image = Image.open(BytesIO(sprite_response.content)).resize((96, 96), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.pokemon_photos[p.id] = photo

            self.pokemon_data[p.id] = {
                "name": p.name,
                "type_display": " ".join(TYPE_EMOJIS.get(t, "") for t in p.types),
                "photo": photo
            }

        self.mostrar_pokemones_filtrados()
    def mostrar_pokemones_filtrados(self):
        # Limpia la galería
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()
        self.pokemon_cards.clear()

        filtro = self.search_var.get().strip().lower()

        # Muestra todos los pokémon cuyo nombre contenga el filtro
        for pid, pdata in self.pokemon_data.items():
            if filtro in pdata["name"].lower():
                card = tk.Frame(self.gallery_frame, relief="ridge", borderwidth=2, padx=5, pady=5)
                card.pack(padx=10, pady=5, fill="x")

                tk.Label(card, image=pdata["photo"]).pack(side="left", padx=50)
                tk.Label(card, text=f"{pdata['name']} {pdata['type_display']}", font=("Arial", 16)).pack(side="left", padx=10)

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
                        if pid in self.selected_pokemon_ids:
                            self.selected_pokemon_ids.remove(pid)
                    self.update_battle_button()

                cb = tk.Checkbutton(card, variable=var, command=on_toggle)
                cb.pack(side="right", padx=10)

                self.pokemon_cards[pid] = card

        self.update_battle_button()

    def filtrar_pokemones(self, *args):
        self.mostrar_pokemones_filtrados()

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

    def launch_battle(self):
        player_name = self.player_name_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Pokeminmax", "¡Debes ingresar tu nombre!")
            return
        if len(self.selected_pokemon_ids) != MAX_SELECCIONADOS:
            messagebox.showwarning("Pokeminmax", f"Debes seleccionar exactamente {MAX_SELECCIONADOS} Pokémon.")
            return

        # Lanza la batalla
        BattleScreen(self.root, player_name, list(self.selected_pokemon_ids))



def launch_gui():
    PokeMinMaxGUI()


if __name__ == "__main__":
    launch_gui()
