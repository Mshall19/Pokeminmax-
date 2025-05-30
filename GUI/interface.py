import tkinter as tk
from tkinter import messagebox

class PokeMinMaxGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokeminmax - Selección de jugador y Pokémon")
        self.root.geometry("600x600")

        # Nombre del jugador
        tk.Label(self.root, text="Nombre del jugador:").pack(pady=5)
        self.player_name_entry = tk.Entry(self.root)
        self.player_name_entry.pack(pady=5)

        # Botón para confirmar nombre
        self.confirm_name_btn = tk.Button(self.root, text="Confirmar Nombre", command=self.confirm_name)
        self.confirm_name_btn.pack(pady=10)

        # Galería Pokémon (por ahora vacío)
        self.gallery_frame = tk.Frame(self.root)
        self.gallery_frame.pack(pady=10)

        tk.Label(self.gallery_frame, text="Galería de Pokémon (vacía por ahora)").pack()

        # Entrada para añadir Pokémon
        tk.Label(self.root, text="Añadir Pokémon por nombre:").pack(pady=5)
        self.add_pokemon_entry = tk.Entry(self.root)
        self.add_pokemon_entry.pack(pady=5)

        # Botones para añadir y borrar Pokémon
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.add_pokemon_btn = tk.Button(btn_frame, text="Añadir Pokémon", command=self.add_pokemon)
        self.add_pokemon_btn.grid(row=0, column=0, padx=5)

        self.delete_selected_btn = tk.Button(btn_frame, text="Borrar Pokémon seleccionados", command=self.delete_selected)
        self.delete_selected_btn.grid(row=0, column=1, padx=5)

        # Lista para guardar Pokémon añadidos
        self.pokemon_list = []
        self.pokemon_widgets = []  # para guardar referencias visuales

        self.root.mainloop()

    def confirm_name(self):
        name = self.player_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre.")
            return
        messagebox.showinfo("Nombre confirmado", f"Jugador: {name}")

    def add_pokemon(self):
        name = self.add_pokemon_entry.get().strip().lower()
        if not name:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre de Pokémon.")
            return
        if name in self.pokemon_list:
            messagebox.showwarning("Advertencia", "Pokémon ya agregado.")
            return

        # Aquí luego cargaremos imagen y tipo desde la API, por ahora sólo agregamos texto
        self.pokemon_list.append(name)
        label = tk.Label(self.gallery_frame, text=name.capitalize())
        label.pack()
        self.pokemon_widgets.append(label)

    def delete_selected(self):
        # Por ahora no tenemos selección, así que eliminamos todo
        for widget in self.pokemon_widgets:
            widget.destroy()
        self.pokemon_widgets.clear()
        self.pokemon_list.clear()


def launch_gui():
    PokeMinMaxGUI()

if __name__ == "__main__":
    PokeMinMaxGUI()
