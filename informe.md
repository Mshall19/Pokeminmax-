


---

## Flujo de Trabajo

1. **Carga de Datos**  
   - Los datos de los Pokémon se obtienen desde la API de PokeAPI y se exportan a un Excel ([`datos/exportar_pokemon_excel.py`](datos/exportar_pokemon_excel.py)).
   - Los Pokémon se cargan desde el Excel usando [`datos/cargar_desde_excel.py`](datos/cargar_desde_excel.py).

2. **Ejecución Principal**  
   - El archivo principal es [`main.py`](main.py).
   - Se inicializan los equipos del jugador y la IA.
   - Se lanza la interfaz gráfica con [`GUI/interface.py`](GUI/interface.py).

3. **Interfaz Gráfica**  
   - Permite seleccionar Pokémon y lanzar la batalla.
   - La batalla se desarrolla en [`GUI/battle_screen.py`](GUI/battle_screen.py).

4. **Batalla y Lógica**  
   - La lógica de batalla y cálculo de daño está en [`battle.py`](battle.py).
   - La IA utiliza el algoritmo Minimax implementado en [`minimax.py`](minimax.py).

---

## Archivos y Funciones Destacables

### [`main.py`](main.py)
- **Función principal:**  
  Inicializa los equipos y lanza la GUI con `launch_gui(jugador, ia)`.

### [`GUI/interface.py`](GUI/interface.py)
- **Clase `PokeMinMaxGUI`:**  
  - Permite seleccionar el equipo del jugador.
  - Muestra sprites y tipos.
  - Lanza la pantalla de batalla con `BattleScreen`.

### [`GUI/battle_screen.py`](GUI/battle_screen.py)
- **Clase `BattleScreen`:**  
  - Muestra la batalla entre los equipos.
  - Permite seleccionar ataques.
  - Actualiza sprites, barras de vida y mensajes.
  - Llama a la IA para que responda el turno.
  - Funciones destacadas:
    - `player_attack`: Ejecuta el ataque del jugador.
    - `ai_turn`: Ejecuta el ataque de la IA usando Minimax.
    - `update_battle_display`: Refresca la interfaz tras cada acción.

### [`battle.py`](battle.py)
- **Funciones:**
  - `get_type_multiplier`: Calcula el multiplicador de tipo.
  - `calculate_damage`: Calcula el daño de un ataque.
  - `apply_move`: Aplica el daño a un Pokémon.

### [`minimax.py`](minimax.py)
- **Algoritmo Minimax:**  
  - `minimax`: Implementa el algoritmo para decidir el mejor ataque de la IA.
  - `obtener_mejor_ataque`: Devuelve el mejor movimiento para la IA.

### [`pokemon.py`](pokemon.py)
- **Clase `Pokemon`:**  
  - Representa un Pokémon, sus stats, tipos y movimientos.
  - Métodos para r
Pokeminmax-/ │ ├── battle.py ├── main.py ├── minimax.py ├── pokemon.py ├── trainer.py ├── requirements.txt ├── README.md │ ├── datos/ │ ├── api.py │ ├── cargar_desde_excel.py │ ├── exportar_pokemon_excel.py │ └── pokemon_primera_gen.xlsx │ ├── GUI/ │ ├── interface.py │ ├── battle_screen.py │ └── bg.jpg │ ├── sprite/ │ └── descargar_sprites.py │ └── sprites/ └── (sprites descargados)


---

## Flujo de Trabajo

1. **Carga de Datos**  
   - Los datos de los Pokémon se obtienen desde la API de PokeAPI y se exportan a un Excel ([`datos/exportar_pokemon_excel.py`](datos/exportar_pokemon_excel.py)).
   - Los Pokémon se cargan desde el Excel usando [`datos/cargar_desde_excel.py`](datos/cargar_desde_excel.py).

2. **Ejecución Principal**  
   - El archivo principal es [`main.py`](main.py).
   - Se inicializan los equipos del jugador y la IA.
   - Se lanza la interfaz gráfica con [`GUI/interface.py`](GUI/interface.py).

3. **Interfaz Gráfica**  
   - Permite seleccionar Pokémon y lanzar la batalla.
   - La batalla se desarrolla en [`GUI/battle_screen.py`](GUI/battle_screen.py).

4. **Batalla y Lógica**  
   - La lógica de batalla y cálculo de daño está en [`battle.py`](battle.py).
   - La IA utiliza el algoritmo Minimax implementado en [`minimax.py`](minimax.py).

---

## Archivos y Funciones Destacables

### [`main.py`](main.py)
- **Función principal:**  
  Inicializa los equipos y lanza la GUI con `launch_gui(jugador, ia)`.

### [`GUI/interface.py`](GUI/interface.py)
- **Clase `PokeMinMaxGUI`:**  
  - Permite seleccionar el equipo del jugador.
  - Muestra sprites y tipos.
  - Lanza la pantalla de batalla con `BattleScreen`.

### [`GUI/battle_screen.py`](GUI/battle_screen.py)
- **Clase `BattleScreen`:**  
  - Muestra la batalla entre los equipos.
  - Permite seleccionar ataques.
  - Actualiza sprites, barras de vida y mensajes.
  - Llama a la IA para que responda el turno.
  - Funciones destacadas:
    - `player_attack`: Ejecuta el ataque del jugador.
    - `ai_turn`: Ejecuta el ataque de la IA usando Minimax.
    - `update_battle_display`: Refresca la interfaz tras cada acción.

### [`battle.py`](battle.py)
- **Funciones:**
  - `get_type_multiplier`: Calcula el multiplicador de tipo.
  - `calculate_damage`: Calcula el daño de un ataque.
  - `apply_move`: Aplica el daño a un Pokémon.

### [`minimax.py`](minimax.py)
- **Algoritmo Minimax:**  
  - `minimax`: Implementa el algoritmo para decidir el mejor ataque de la IA.
  - `obtener_mejor_ataque`: Devuelve el mejor movimiento para la IA.

### [`pokemon.py`](pokemon.py)
- **Clase `Pokemon`:**  
  - Representa un Pokémon, sus stats, tipos y movimientos.
  - Métodos para recibir daño y comprobar si está debilitado.

### [`trainer.py`](trainer.py)
- **Clase `Trainer`:**  
  - Representa a un entrenador y su equipo.
  - Métodos para cambiar de Pokémon y comprobar si ha perdido.

### [`datos/api.py`](datos/api.py)
- **Funciones para obtener datos de la PokeAPI** y filtrar solo Pokémon de primera generación.

### [`sprite/descargar_sprites.py`](sprite/descargar_sprites.py)
- Descarga los sprites de los Pokémon y los guarda en la carpeta `sprites/`.

---

## Requisitos

- Python 3.x
- Paquetes: pandas, openpyxl, requests, pillow

Instala dependencias con:

```sh
pip install -r [requirements.txt](http://_vscodecontentref_/13)
Ejecución
Asegúrate de tener el archivo Excel de Pokémon generado.
Ejecuta el proyecto con:
python [main.py](http://_vscodecontentref_/14)
Notas
Los sprites deben estar descargados en la carpeta sprites/.
Si falta el Excel, ejecuta datos/exportar_pokemon_excel.py.
La IA utiliza Minimax para elegir el mejor ataque en cada turno.ecibir daño y comprobar si está debilitado.

### [`trainer.py`](trainer.py)
- **Clase `Trainer`:**  
  - Representa a un entrenador y su equipo.
  - Métodos para cambiar de Pokémon y comprobar si ha perdido.

### [`datos/api.py`](datos/api.py)
- **Funciones para obtener datos de la PokeAPI** y filtrar solo Pokémon de primera generación.

### [`sprite/descargar_sprites.py`](sprite/descargar_sprites.py)
- Descarga los sprites de los Pokémon y los guarda en la carpeta `sprites/`.

---

## Requisitos

- Python 3.x
- Paquetes: pandas, openpyxl, requests, pillow

Instala dependencias con:

```sh
pip install -r [requirements.txt](http://_vscodecontentref_/13)
Ejecución
Asegúrate de tener el archivo Excel de Pokémon generado.
Ejecuta el proyecto con:
python [main.py](http://_vscodecontentref_/14)
Notas
Los sprites deben estar descargados en la carpeta sprites/.
Si falta el Excel, ejecuta datos/exportar_pokemon_excel.py.
La IA utiliza Minimax para elegir el mejor ataque en cada turno.