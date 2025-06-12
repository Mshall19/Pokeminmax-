import requests

def is_first_generation(pokemon_name_or_id):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name_or_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["generation"]["name"] == "generation-i"
    except Exception as e:
        print(f"⚠️ Advertencia: no se pudo verificar generación de {pokemon_name_or_id}. Error: {e}")
        return True

def get_pokemon_data(pokemon_id):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not is_first_generation(data["name"]):
            raise ValueError(f"{data['name'].capitalize()} no es de primera generación")

        types = [t["type"]["name"] for t in data["types"]]
        sprite = data["sprites"]["front_default"]

        moves = [
            {"name": "Tackle", "type": "normal", "power": 40},
            {"name": f"{types[0].capitalize()} Move", "type": types[0], "power": 60},
            {"name": "Quick Attack", "type": "normal", "power": 50},
            {"name": f"{types[0].capitalize()} Blast", "type": types[0], "power": 80}
        ]

        return {
            "id": data["id"],
            "name": data["name"].capitalize(),
            "hp": data["stats"][0]["base_stat"],
            "types": types,
            "sprite": sprite,
            "moves": moves
        }

    except Exception as e:
        print(f"❌ Error al obtener datos del Pokémon #{pokemon_id}: {e}")
        return {
            "id": pokemon_id,
            "name": f"Pokémon {pokemon_id}",
            "hp": 50 + pokemon_id % 100,
            "types": ["normal"],
            "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png",
            "moves": [
                {"name": "Tackle", "type": "normal", "power": 40},
                {"name": "Headbutt", "type": "normal", "power": 60},
                {"name": "Slam", "type": "normal", "power": 70},
                {"name": "Mega Punch", "type": "normal", "power": 80}
            ]
        }
