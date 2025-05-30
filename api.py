import requests

def is_first_generation(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}")
    if response.status_code == 200:
        data = response.json()
        return data['generation']['name'] == 'generation-i'
    return False

def get_pokemon_data(name):
    if not is_first_generation(name):
        raise ValueError(f"{name} no pertenece a la primera generación.")
    
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
    if response.status_code == 200:
        data = response.json()
        types = [t['type']['name'] for t in data['types']]
        moves = []
        for move in data['moves'][:4]:  # Limita a los primeros 4 movimientos
            move_data = requests.get(move['move']['url']).json()
            if move_data['power'] is not None and move_data['damage_class']['name'] == 'physical':
                moves.append({
                    'name': move_data['name'],
                    'power': move_data['power'],
                    'type': move_data['type']['name']
                })
        return {
            'name': data['name'],
            'hp': data['stats'][0]['base_stat'],
            'types': types,
            'moves': moves
        }
    raise ValueError("Pokémon no encontrado")
