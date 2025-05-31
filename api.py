import requests

def is_first_generation(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name_or_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["generation"]["name"] == "generation-i"

def get_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Validar que sea de la primera generación
    name = data["name"]
    if not is_first_generation(name):
        raise ValueError(f"{name.capitalize()} no pertenece a la primera generación.")

    types = [t["type"]["name"] for t in data["types"]]

    # Simular lista de movimientos (por simplicidad)
    moves = [
        {"name": "Tackle", "type": types[0], "power": 40},
        {"name": "Quick Attack", "type": types[0], "power": 50}
    ]

    return {
        "id": data["id"],
        "name": name.capitalize(),
        "hp": data["stats"][0]["base_stat"],
        "types": types,
        "sprite": data["sprites"]["front_default"],
        "moves": moves
    }
