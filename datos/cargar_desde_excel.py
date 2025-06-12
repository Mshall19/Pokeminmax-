import pandas as pd
from pokemon import Pokemon

def parse_move(move_str):
    try:
        nombre, resto = move_str.split(" (")
        tipo, poder = resto.strip(")").split(", ")
        return {
            "name": nombre.strip(),
            "type": tipo.strip().lower(),
            "power": int(poder.strip())
        }
    except Exception as e:
        raise ValueError(f"Movimiento mal formateado: '{move_str}'. Error: {e}")

def cargar_pokemones_desde_excel(path_excel="datos/pokemon_primera_gen.xlsx"):
    try:
        df = pd.read_excel(path_excel)

        required_cols = ["ID", "Nombre", "Tipos", "PS", "Movimiento 1", "Movimiento 2", "Movimiento 3", "Movimiento 4", "Sprite URL"]
        if not all(col in df.columns for col in required_cols):
            raise Exception("❌ El archivo Excel no contiene todas las columnas requeridas.")

        pokemones = []

        for _, row in df.iterrows():
            movimientos = [
                parse_move(row["Movimiento 1"]),
                parse_move(row["Movimiento 2"]),
                parse_move(row["Movimiento 3"]),
                parse_move(row["Movimiento 4"]),
            ]

            p = Pokemon(
                name=row["Nombre"],
                hp=row["PS"],
                types=[t.strip() for t in row["Tipos"].split(",")],
                moves=movimientos,
                sprite_url=row["Sprite URL"],
                pokemon_id=row["ID"]
            )
            pokemones.append(p)

        return pokemones

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo Excel en {path_excel}. Ejecuta primero exportar_pokemon_excel.py")
    except Exception as e:
        raise Exception(f"Error al cargar Pokémon desde Excel: {str(e)}")
