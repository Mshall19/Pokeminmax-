from GUI.interface import launch_gui
from trainer import Trainer
from pokemon import crear_pokemon_por_id
from datos.cargar_desde_excel import cargar_pokemones_desde_excel
import random

if __name__ == "__main__":
    pokemones = cargar_pokemones_desde_excel()

    equipo_jugador = [
        crear_pokemon_por_id(1, pokemones),
        crear_pokemon_por_id(4, pokemones),
        crear_pokemon_por_id(7, pokemones)
    ]
    ids_disponibles = [p.id for p in pokemones]
    ids_aleatorios = random.sample(ids_disponibles, 3)
    equipo_ia = [crear_pokemon_por_id(i, pokemones) for i in ids_aleatorios]

    jugador = Trainer("Ash", equipo_jugador, is_ai=False)
    ia = Trainer("IA", equipo_ia, is_ai=True)

    launch_gui(jugador, ia)
