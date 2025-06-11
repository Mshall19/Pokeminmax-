# exportar_pokemon_excel.py

import pandas as pd
from api import get_pokemon_data, is_first_generation

def exportar_pokemon_primera_generacion(path_excel="pokemon_primera_gen.xlsx"):
    datos_pokemones = []

    for pokemon_id in range(1, 152):
        try:
            if not is_first_generation(pokemon_id):
                continue
            datos = get_pokemon_data(pokemon_id)
            tipos = ", ".join(datos["types"])
            movs = datos["moves"]
            datos_pokemones.append({
                "ID": datos["id"],
                "Nombre": datos["name"],
                "Tipos": tipos,
                "PS": datos["hp"],
                "Movimiento 1": f'{movs[0]["name"]} ({movs[0]["type"]}, {movs[0]["power"]})',
                "Movimiento 2": f'{movs[1]["name"]} ({movs[1]["type"]}, {movs[1]["power"]})',
                "Sprite URL": datos["sprite"]
            })
            print(f"Agregado: {datos['name']}")
        except Exception as e:
            print(f"Error con ID {pokemon_id}: {e}")

    df = pd.DataFrame(datos_pokemones)
    df.to_excel(path_excel, index=False)
    print(f"\n✅ Archivo Excel generado: {path_excel}")

if __name__ == "__main__":
    exportar_pokemon_primera_generacion()
