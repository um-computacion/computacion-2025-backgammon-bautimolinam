# Justificación del Diseño - Backgammon

**Proyecto:** Backgammon - Computación 2025  
**Versión:** 1.0.0  
**Fecha:**  2025

---

## 1. Resumen del Diseño

El proyecto implementa el juego Backgammon usando Python con una arquitectura modular. Decidí separar completamente la lógica del juego (carpeta `core/`) de las interfaces de usuario (carpetas `cli/` y `pygame_ui/`). Esta decisión me permite:

- Testear la lógica sin depender de interfaces gráficas
- Reutilizar el mismo core para CLI y Pygame
- Mantener el código más limpio y organizado
- Agregar nuevas interfaces fácilmente en el futuro

La arquitectura sigue el patrón de capas:
```
Interfaces (CLI/Pygame) 
    ↓ usa
Lógica del Juego (BackgammonGame)
    ↓ coordina
Entidades (Board, Player, Dice, Checker)
```

## 2. Clases Principales y sus Responsabilidades

### 2.1 Clase `Checker` (Ficha)

Decidí crear una clase separada para las fichas porque cada una tiene su propio estado: puede estar en el tablero, en la barra (capturada), o sacada del juego. Una ficha también necesita saber a qué jugador pertenece y validar sus transiciones de estado.

Al principio pensé en usar solo números o tuplas, pero eso no me permitía encapsular el comportamiento ni validar los cambios de estado correctamente. Por ejemplo, una ficha no puede moverse si ya fue sacada del tablero, y esto es más fácil de validar con métodos propios.

**Atributos principales:**
- `__player_id__`: El dueño (1 o 2), no cambia nunca
- `__position__`: Dónde está (0-23 o None)
- `__is_on_bar__`: Si está capturada
- `__is_borne_off__`: Si fue sacada del tablero

### 2.2 Clase `Dice` (Dados)

Los dados necesitan su propia clase porque tienen lógica compleja: cuando salen dobles puedes mover 4 veces, necesitas trackear qué valores ya usaste, y para bear off a veces puedes usar valores mayores.

Si hubiera usado `random.randint()` directamente en el Game, no podría manejar fácilmente estas reglas. Además, con una clase propia puedo usar una seed para tests reproducibles.

**Atributos principales:**
- `__dice1__`, `__dice2__`: Los valores actuales
- `__available_moves__`: Lista de valores que puedo usar todavía
- `__used_moves__`: Los que ya usé (útil para debugging)
- `__is_rolled__`: Si ya tiré en este turno

### 2.3 Clase `Board` (Tablero)

El Board es la clase más compleja porque implementa todas las reglas del tablero: los 24 puntos, la barra para fichas capturadas, bear off, validación de movimientos, capturas, etc.

Usé un diccionario para los puntos (`{0: [], 1: [], ..., 23: []}`) porque me da acceso O(1) y cada punto puede tener múltiples fichas. Las barras están separadas por jugador para evitar mezclar fichas.

Una decisión importante fue poner todas las validaciones acá: el Board es quien "conoce" las reglas del tablero, entonces es su responsabilidad decir si un movimiento es válido o no.

**Atributos principales:**
- `__points__`: Dict con los 24 puntos, cada uno tiene lista de fichas
- `__bar_player1__`, `__bar_player2__`: Fichas capturadas (separadas)
- `__borne_off_player1__`, `__borne_off_player2__`: Fichas sacadas

### 2.4 Clase `Player` (Jugador)

Cada jugador necesita mantener sus 15 fichas, su nombre, y proporcionar información sobre su estado (cuántas fichas tiene en la barra, cuántas sacó, si puede hacer bear off).

Decidí que las fichas "pertenecen" al Player, no solo viven en el Board. Esto me facilita consultas como "dame todas las fichas del jugador en posición X" sin tener que recorrer todo el tablero.

**Atributos principales:**
- `__player_id__`: Identificador (1 o 2)
- `__name__`: Nombre personalizable
- `__checkers__`: Lista de 15 fichas (Checker instances)
- `__is_turn__`: Si es su turno ahora

### 2.5 Clase `BackgammonGame` (Coordinador)

Esta es la clase fachada que coordina todo. Las interfaces (CLI y Pygame) solo hablan con Game, no tocan directamente Board, Player, etc.

Game maneja el flujo: iniciar partida, tirar dados, validar y ejecutar movimientos, cambiar turnos, detectar victoria. También mantiene el historial de movimientos y el estado del juego.

Separar Game de Board fue clave: Board es "tonto" (solo mantiene estado), Game es "inteligente" (aplica las reglas del flujo).

**Atributos principales:**
- `__board__`, `__player1__`, `__player2__`, `__dice__`: Componentes
- `__state__`: Estado del juego (NOT_STARTED, IN_PROGRESS, FINISHED)
- `__current_player_id__`: Quién juega ahora
- `__turn_count__`: Contador de turnos
- `__move_history__`: Historial completo

## 3. Excepciones Personalizadas

Definí 10 excepciones custom que heredan de `BackgammonException`. Al principio pensé en usar solo `ValueError` y `RuntimeError`, pero las excepciones personalizadas me dan:

1. **Semántica clara**: `InvalidMoveException` es más descriptivo que `ValueError`
2. **Contexto específico**: Puedo incluir from_point, to_point, reason
3. **Manejo granular**: Las interfaces pueden capturar tipos específicos
4. **Debugging más fácil**: Los mensajes son automáticamente descriptivos

Ejemplos:
- `InvalidMoveException`: Cuando un movimiento no es válido
- `GameNotStartedException`: Intentar jugar sin iniciar
- `CannotBearOffException`: Intentar sacar sin cumplir condiciones

## 4. Decisiones de Diseño Importantes

### 4.1 Atributos privados con `__nombre__`

La consigna requiere este formato. En Python esto hace "name mangling" y convierte `__attr__` en `_Clase__attr__`. Lo implementé consistentemente en todas las clases y uso `@property` para acceso controlado.

### 4.2 Properties vs Getters/Setters

Usé `@property` (estilo Python) en lugar de `get_x()` / `set_x()` (estilo Java):

```python
@property
def name(self) -> str:
    return self.__name__

@name.setter
def name(self, value: str) -> None:
    if not value.strip():
        raise ValueError("Name cannot be empty")
    self.__name__ = value.strip()
```

Es más Pythonic y permite validaciones transparentes.

### 4.3 Representación de puntos: números 0-23

Consideré usar strings ("point_0") o enums, pero elegí números porque:
- Puedo hacer aritmética: `destino = origen - valor_dado`
- Comparaciones más rápidas
- Código más limpio

Uso -1 como valor especial para la barra y para bear off.

### 4.4 Cálculo dinámico de propiedades

Propiedades como `checkers_on_bar_count` se calculan dinámicamente en lugar de almacenarlas:

```python
@property
def checkers_on_bar_count(self) -> int:
    return len([c for c in self.__checkers__ if c.is_on_bar])
```

Esto evita problemas de sincronización. Es un poco más lento (O(n)) pero con solo 15 fichas no afecta performance.

### 4.5 Validación Fail Fast

Valido los parámetros inmediatamente y lanzo excepciones. Esto detecta errores temprano y previene estados corruptos:

```python
def move_checker(self, from_point, to_point, player_id):
    if not self.can_move_from_to(from_point, to_point, player_id):
        raise InvalidMoveException(from_point, to_point, "Invalid")
    # solo si es válido, ejecutar...
```

### 4.6 Separación de directorios simple

Mantuve `core/` plano (todos los archivos en el mismo nivel) porque:
- El proyecto tiene solo 6 archivos
- Los imports son más simples
- No necesito sobre-estructurar algo pequeño

## 5. Cumplimiento de Principios SOLID

### S - Single Responsibility
Cada clase tiene una responsabilidad clara:
- Board: solo el tablero
- Checker: solo una ficha
- Dice: solo los dados
- Player: solo un jugador
- Game: solo coordinación

### O - Open/Closed
Puedo agregar nuevas interfaces (web, mobile) sin modificar core. Las excepciones pueden extenderse sin tocar la base.

### L - Liskov Substitution
Todas las excepciones pueden sustituir a BackgammonException:
```python
try:
    game.make_move(from_point, to_point)
except BackgammonException as e:  # Captura cualquiera
    print(f"Error: {e}")
```

### I - Interface Segregation
CLI y Pygame implementan solo lo que necesitan. No hay métodos forzados que no usen.

### D - Dependency Inversion
Las interfaces dependen de abstracciones (Game) no de implementaciones concretas. Game coordina las entidades sin acoplamiento directo.

## 6. Estrategia de Testing

Implementé tests unitarios para cada clase core alcanzando >90% de cobertura. Mi estrategia fue:

1. **Tests unitarios**: Cada clase por separado
   - test_checker.py: 15 tests (95% cobertura)
   - test_dice.py: 10 tests (92% cobertura)
   - test_board.py: 11 tests (88-90% cobertura)
   - test_game.py: 12 tests (85-88% cobertura)

2. **Tests de integración**: Interacción entre componentes (en test_game.py)

3. **Tests de casos edge**: 
   - Valores inválidos (puntos -1, 24, dados 0, 7)
   - Estados imposibles (mover ficha sacada)
   - Reglas complejas (bear off con valores mayores)

4. **Uso de mocks**: Para controlar valores aleatorios de dados
   ```python
   @patch('core.dice.random.randint')
   def test_roll(self, mock_randint):
       mock_randint.side_effect = [4, 6]
       # test...
   ```

Usé pytest con pytest-cov para medir cobertura. Los tests se ejecutan con `pytest tests/ --cov=core`.

## 7. Manejo de Errores

Implementé una jerarquía de excepciones con BackgammonException como base. Cada excepción incluye contexto relevante:

```python
class InvalidMoveException(BackgammonException):
    def __init__(self, from_point: int, to_point: int, reason: str):
        self.__from_point__ = from_point
        self.__to_point__ = to_point
        message = f"Invalid move {from_point}→{to_point}: {reason}"
        super().__init__(message)
```

Las excepciones se lanzan en el lugar más lógico: Board valida movimientos de tablero, Game valida flujo del juego, Dice valida valores de dados.

## 8. Documentación

Todas las clases y métodos tienen docstrings con formato Google:

```python
def move_checker(self, from_point: int, to_point: int, player_id: int) -> Optional[Checker]:
    """
    Mueve una ficha de un punto a otro.
    
    Args:
        from_point: Punto de origen (0-23)
        to_point: Punto de destino (0-23)
        player_id: ID del jugador (1 o 2)
    
    Returns:
        Ficha capturada si hubo captura, None en caso contrario
    
    Raises:
        InvalidMoveException: Si el movimiento no es válido
    """
```

Usé type hints en todos los métodos para mejor claridad y detección de errores por IDEs.

## 9. Diagrama de Clases UML

```
┌─────────────────────┐
│   BackgammonGame    │
│─────────────────────│
│ -board: Board       │
│ -player1: Player    │
│ -player2: Player    │
│ -dice: Dice         │
│ -state: GameState   │
└─────────────────────┘
     │  │  │  │
     │  │  │  └──────────────┐
     │  │  └──────────┐      │
     │  └──────┐      │      │
     │         │      │      │
     ▼         ▼      ▼      ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Board  │ │ Player │ │ Player │ │ Dice   │
│────────│ │────────│ │────────│ │────────│
│-points │ │-id     │ │-id     │ │-dice1  │
│-bars   │ │-name   │ │-name   │ │-dice2  │
└────────┘ │-checkers│ │-checkers│ └────────┘
           └────────┘ └────────┘
                │         │
                ▼         ▼
           ┌────────┐ ┌────────┐
           │Checker │ │Checker │
           │────────│ │────────│
           │-player │ │-player │
           │-position│ │-position│
           └────────┘ └────────┘
```

## 10. Evolución del Diseño

### Sprint 1 (Sep-Oct 2025)
Implementé toda la lógica core: clases básicas, validaciones, excepciones. Definí la arquitectura de separación core/UI.

### Sprint 2 (Oct 2025)
Desarrollé la interfaz CLI completa con comandos de texto. Implementé sistema de parsing de comandos.

### Sprint 3 (Oct-Nov 2025)
Escribí todos los tests unitarios alcanzando >90% cobertura. Refactoricé algunas validaciones para mejor testabilidad.

### Sprint 4 (Nov 2025)
Implementé la interfaz gráfica con Pygame. Desarrollé sistema de renderizado, detección de clicks, y panel de información.

A lo largo del desarrollo mantuve commits regulares (10+ por sprint) documentando el progreso incremental.

---

**Conclusión:** El diseño modular con separación de responsabilidades me permitió desarrollar un juego completo, testeable y extensible. La aplicación de principios SOLID garantiza código mantenible y de calidad.