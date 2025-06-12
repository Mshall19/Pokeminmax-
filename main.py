from GUI.interface import launch_gui
from trainer import Trainer
from pokemon import crear_pokemon_por_id
from datos.cargar_desde_excel import cargar_pokemones_desde_excel

if __name__ == "__main__":
    # Cargar todos los Pokémon desde el Excel
    pokemones = cargar_pokemones_desde_excel()

    # Crear Pokémon por ID (puedes cambiar los IDs por los que prefieras)
    equipo_jugador = [
        crear_pokemon_por_id(1, pokemones),  # Bulbasaur
        crear_pokemon_por_id(4, pokemones),  # Charmander
        crear_pokemon_por_id(7, pokemones)   # Squirtle
    ]
    equipo_ia = [
        crear_pokemon_por_id(3, pokemones),   # Venusaur
        crear_pokemon_por_id(150, pokemones)  # Mewtwo
    ]

    # Crear entrenadores
    jugador = Trainer("Ash", equipo_jugador, is_ai=False)
    ia = Trainer("IA", equipo_ia, is_ai=True)

    # Lanzar la GUI
    launch_gui(jugador, ia)
