class Pokemon:
    def __init__(self, name, hp, types, moves, sprite_url, pokemon_id=None):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.types = types
        self.moves = moves
        self.sprite_url = sprite_url
        self.id = pokemon_id

    def receive_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self):
        return self.current_hp == 0

    @staticmethod
    def from_excel_data(data):
        return Pokemon(
            name=data["Nombre"],
            hp=data["PS"],
            types=[t.strip() for t in data["Tipos"].split(",")],
            moves=data["moves"],
            sprite_url=data["Sprite URL"],
            pokemon_id=data["ID"]
        )

def crear_pokemon_por_id(pokemon_id, lista_pokemones):
    try:
        for pokemon in lista_pokemones:
            if pokemon.id == pokemon_id:
                return pokemon
        raise ValueError(f"No se encontró Pokémon con ID {pokemon_id}")
    except AttributeError:
        raise AttributeError("La lista de Pokémon no tiene el formato correcto")