import requests
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2/"
    CACHE_DIR = Path("data/pokemon_cache/")
    
    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_cached_data(self, endpoint: str, identifier: str) -> Optional[dict]:
        cache_file = self.CACHE_DIR / f"{endpoint}_{identifier}.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def _cache_data(self, endpoint: str, identifier: str, data: dict):
        cache_file = self.CACHE_DIR / f"{endpoint}_{identifier}.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    
    def get_pokemon_data(self, pokemon_name: str) -> dict:
        cached_data = self._get_cached_data("pokemon", pokemon_name.lower())
        if cached_data:
            return cached_data
        
        try:
            response = requests.get(f"{self.BASE_URL}pokemon/{pokemon_name.lower()}")
            response.raise_for_status()
            data = response.json()
            self._cache_data("pokemon", pokemon_name.lower(), data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de {pokemon_name}: {e}")
            return {}
    
    def get_move_data(self, move_name: str) -> dict:
        cached_data = self._get_cached_data("move", move_name.lower())
        if cached_data:
            return cached_data
        
        try:
            response = requests.get(f"{self.BASE_URL}move/{move_name.lower()}")
            response.raise_for_status()
            data = response.json()
            self._cache_data("move", move_name.lower(), data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos del movimiento {move_name}: {e}")
            return {}
    
    def create_pokemon_from_api(self, pokemon_name: str) -> Optional['Pokemon']:
        from pokemon import Pokemon, Move
        
        data = self.get_pokemon_data(pokemon_name)
        if not data:
            return None
        
        # Obtener movimientos (limitamos a 4)
        moves = []
        for move_entry in data['moves'][:4]:
            move_data = self.get_move_data(move_entry['move']['name'])
            if move_data and move_data.get('power'):
                moves.append(Move(
                    name=move_data['name'],
                    move_type=move_data['type']['name'],
                    power=move_data['power'],
                    accuracy=move_data['accuracy']
                ))
        
        # Si no hay movimientos con poder, añadimos algunos por defecto
        if not moves:
            moves = [
                Move(name="Tackle", move_type="normal", power=40, accuracy=100),
                Move(name="Quick Attack", move_type="normal", power=40, accuracy=100)
            ]
        
        # Crear el Pokémon
        return Pokemon(
            name=data['name'].capitalize(),
            pokemon_type=data['types'][0]['type']['name'],
            max_hp=data['stats'][0]['base_stat'] * 2,
            current_hp=data['stats'][0]['base_stat'] * 2,
            moves=moves,
            speed=data['stats'][5]['base_stat']
        )