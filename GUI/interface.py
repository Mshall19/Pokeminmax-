import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from .battle_screen import BattleScreen


TYPE_EMOJIS = {
    "grass": "🌿", "fire": "🔥", "water": "💧", "electric": "⚡",
    "bug": "🐛", "normal": "🔘", "poison": "☠️", "ground": "🌍",
    "fighting": "🥊", "psychic": "🧠", "rock": "🪨", "ghost": "👻",
    "ice": "❄️", "dragon": "🐉", "fairy": "🧚", "flying": "🕊️"
}

class PokeMinMaxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokeminmax")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.pokemon_thumbnails = []
        self.selected_pokemon_ids = []
        self.pokemon_cards = {}

        self.setup_interface()
        self.root.mainloop()

    def setup_interface(self):
        name_frame = tk.Frame(self.root)
        name_frame.pack(pady=10)

        tk.Label(name_frame, text="Nombre del jugador:", font=("Arial", 14)).pack(side="left", padx=5)
        self.player_name_entry = tk.Entry(name_frame, font=("Arial", 14), width=30)
        self.player_name_entry.pack(side="left")

        self.gallery_container = tk.Frame(self.root)
        self.gallery_container.pack(pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.gallery_container, height=400)
        scrollbar = tk.Scrollbar(self.gallery_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_pokemon_gallery()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Añadir Pokémon:", font=("Arial", 14)).pack(side="left", padx=5)
        self.add_entry = tk.Entry(control_frame, font=("Arial", 14), width=20)
        self.add_entry.pack(side="left", padx=5)

        tk.Button(control_frame, text="Borrar selección", font=("Arial", 12), command=self.clear_selection).pack(side="left", padx=5)

        self.battle_button = tk.Button(self.root, text="¡Iniciar batalla!", font=("Arial", 16), command=self.launch_battle, state="disabled")
        self.battle_button.pack(pady=10)

    def load_pokemon_gallery(self):
        columns = 2
        for index, pokemon_id in enumerate(range(1, 10)):  # ID 1 a 9
            try:
                url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
                response = requests.get(url)
                data = response.json()

                name = data["name"].capitalize()
                sprite_url = data["sprites"]["front_default"]
                types = [TYPE_EMOJIS.get(t["type"]["name"], "") for t in data["types"]]
                type_display = " ".join(types)

                sprite_response = requests.get(sprite_url)
                image = Image.open(BytesIO(sprite_response.content)).resize((96, 96), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(image)
                self.pokemon_thumbnails.append(photo)

                card = tk.Frame(self.scrollable_frame, relief="ridge", borderwidth=2, padx=5, pady=5)

                tk.Label(card, image=photo).pack(side="left", padx=10)
                tk.Label(card, text=f"{name} {type_display}", font=("Arial", 16)).pack(side="left")

                row = index // columns
                col = index % columns
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nw")

                def toggle_selection(pokemon_id=pokemon_id):
                    if pokemon_id in self.selected_pokemon_ids:
                        self.selected_pokemon_ids.remove(pokemon_id)
                        self.pokemon_cards[pokemon_id].config(bg="SystemButtonFace")
                    elif len(self.selected_pokemon_ids) < 3:
                        self.selected_pokemon_ids.append(pokemon_id)
                        self.pokemon_cards[pokemon_id].config(bg="lightgreen")

                    if len(self.selected_pokemon_ids) == 3:
                        self.battle_button.config(state="normal")
                    else:
                        self.battle_button.config(state="disabled")

                card.bind("<Button-1>", lambda e, pid=pokemon_id: toggle_selection(pid))
                self.pokemon_cards[pokemon_id] = card

            except Exception as e:
                print(f"Error cargando Pokémon #{pokemon_id}: {e}")

    def clear_selection(self):
        for pid in self.selected_pokemon_ids:
            if pid in self.pokemon_cards:
                self.pokemon_cards[pid].config(bg="SystemButtonFace")
        self.selected_pokemon_ids.clear()
        self.battle_button.config(state="disabled")
        self.add_entry.delete(0, tk.END)
        messagebox.showinfo("Pokeminmax", "Selección de Pokémon borrada.")

    def launch_battle(self):
        player_name = self.player_name_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Pokeminmax", "¡Debes ingresar tu nombre!")
            return

        BattleScreen(self.root, player_name, self.selected_pokemon_ids)

# Punto de entrada
if __name__ == "__main__":
    PokeMinMaxGUI()

# Para integrarlo desde main.py
def launch_gui():
    PokeMinMaxGUI()
