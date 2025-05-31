import os
import requests

# Crear carpeta si no existe
os.makedirs("sprites", exist_ok=True)

# Descargar los sprites de los 151 Pokémon
for pokemon_id in range(1, 152):
    filename = f"{pokemon_id}.png"
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
    path = os.path.join("sprites", filename)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Descargado: {filename}")
    except Exception as e:
        print(f"Error con {filename}: {e}")
