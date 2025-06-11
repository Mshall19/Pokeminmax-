import pandas as pd
from pokemon import Pokemon

def cargar_pokemones_desde_excel(path_excel="datos/pokemon_primera_gen.xlsx"):
    df = pd.read_excel(path_excel)
    pokemones = []

    for _, row in df.iterrows():
        tipos = [tipo.strip() for tipo in row["Tipos"].split(",")]

        movimientos = []
        for col in ["Movimiento 1", "Movimiento 2"]:
            nombre, resto = row[col].split(" (")
            tipo, poder = resto.strip(")").split(", ")
            movimientos.append({
                "name": nombre,
                "type": tipo,
                "power": int(poder)
            })

        p = Pokemon(
            name=row["Nombre"],
            hp=row["PS"],
            types=tipos,
            moves=movimientos,
            sprite_url=row["Sprite URL"]
        )
        p.id = row["ID"]  # IMPORTANTE: Añadir el ID
        pokemones.append(p)

    return pokemones
