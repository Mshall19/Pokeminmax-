def choose_move(pokemon):
    print(f"Selecciona un ataque para {pokemon.name}:")
    for i, move in enumerate(pokemon.moves):
        print(f"{i+1}. {move['name']} (Tipo: {move['type']}, Poder: {move['power']})")
    choice = int(input("Opción: ")) - 1
    return pokemon.moves[choice]

def choose_pokemon(trainer):
    print(f"{trainer.name}, elige un Pokémon:")
    for i, p in enumerate(trainer.pokemons):
        status = " (debilitado)" if p.is_fainted() else ""
        print(f"{i+1}. {p.name} - HP: {p.hp}{status}")
    while True:
        idx = int(input("Número: ")) - 1
        if 0 <= idx < len(trainer.pokemons) and not trainer.pokemons[idx].is_fainted():
            trainer.active_index = idx
            break
        else:
            print("Elige un Pokémon válido.")
