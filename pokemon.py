class Pokemon:
    def __init__(self, name, hp, types, moves, sprite_url):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.types = types
        self.moves = moves
        self.sprite_url = sprite_url

    def receive_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    @staticmethod
    def from_api_data(data):
        return Pokemon(
            name=data["name"],
            hp=data["hp"],
            types=data["types"],
            moves=data["moves"],
            sprite_url=data["sprite"]
        )