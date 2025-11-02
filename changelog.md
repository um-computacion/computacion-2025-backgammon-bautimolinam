# Changelog

Todos los cambios importantes del proyecto están documentados acá.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2025-11-01

### Agregado
- Interfaz gráfica completa con Pygame funcionando
- Sistema de renderizado del tablero con los 24 puntos triangulares
- Detección de clicks en puntos del tablero y en la barra
- Panel lateral que muestra turno actual, dados, y comandos disponibles
- Log visual de movimientos estilo terminal en el panel
- Resaltado visual de puntos seleccionados y movimientos válidos
- Comandos de teclado: N (nueva), R (roll), M (moves), S (status), SPACE (end turn), Q/ESC (quit)
- Colores estilo terminal/CLI para mantener consistencia
- Visualización de fichas capturadas en la barra lateral
- Indicadores visuales cuando es un destino válido
- Mensajes de error y éxito con colores diferenciados

### Cambiado
- Mejoré la organización de archivos del proyecto
- Optimicé el renderizado para mejor performance
- Ajusté la detección de colisiones del mouse

## [0.9.0] - 2025-10-25

### Agregado
- Tests unitarios completos para Board (11 tests)
- Tests unitarios completos para Checker (15 tests)
- Tests unitarios completos para Dice (10 tests)
- Tests unitarios completos para BackgammonGame (12 tests)
- Tests de integración entre componentes
- Alcancé >90% de cobertura en módulos core
- Configuración de pytest con coverage
- Tests de casos edge y validaciones exhaustivas

### Cambiado
- Refactoricé algunos métodos en Game para facilitar testing
- Mejoré las validaciones de movimientos en Board
- Optimicé el manejo de excepciones

### Corregido
- Bug en movimientos desde la barra que no validaba correctamente
- Error en cálculo de bear off con valores mayores
- Problema con detección de movimientos válidos en algunos casos
- Ajustes en la lógica de cambio de turnos

## [0.7.0] - 2025-10-15

### Agregado
- Interfaz CLI completa y funcional
- Comandos implementados: new, roll, move, moves, board, status, help, quit
- Parser de puntos que acepta números, 'bar', y 'off'
- Sistema de validación de comandos del usuario
- Visualización ASCII del tablero con formato limpio
- Mensajes de ayuda contextuales
- Manejo de errores con mensajes descriptivos
- Confirmación antes de salir si hay partida en curso

### Cambiado
- Mejoré la legibilidad de la visualización del tablero
- Optimicé el sistema de comandos para ser más intuitivo
- Refiné los mensajes de error para ser más claros

### Corregido
- Ajustes en el formato de visualización del tablero
- Correcciones en el parser de comandos

## [0.5.0] - 2025-10-01

### Agregado
- Implementé clase Board completa con los 24 puntos
- Sistema de barra para fichas capturadas (separada por jugador)
- Sistema completo de bear off con todas las reglas
- Validación exhaustiva de movimientos
- Detección y ejecución de capturas
- Implementé clase Checker con todos sus estados
- Estados de ficha: en tablero, en barra, sacada
- Validaciones de transición entre estados
- Implementé clase Dice con lógica de tiradas
- Soporte para tiradas dobles (4 movimientos)
- Sistema de tracking de dados disponibles y usados
- Implementé clase Player con sus 15 fichas
- Configuración de posiciones iniciales estándar
- Consultas sobre estado de fichas del jugador
- Implementé clase BackgammonGame como coordinador
- Sistema completo de flujo de turnos
- Aplicación de todas las reglas del juego
- Estados del juego (NOT_STARTED, IN_PROGRESS, FINISHED)
- Definí todas las excepciones personalizadas:
  - BackgammonException (base)
  - InvalidMoveException
  - GameNotStartedException
  - GameAlreadyFinishedException
  - InvalidPlayerException
  - InvalidDiceValueException
  - NoMovesAvailableException
  - InvalidPointException
  - CheckerNotAvailableException
  - CannotBearOffException

### Cambiado
- Organicé la estructura del proyecto en módulos separados
- Implementé separación completa entre lógica y presentación
- Apliqué principios SOLID en todo el diseño

## [0.1.0] - 2025-09-20

### Agregado
- Estructura inicial del proyecto
- Configuración del repositorio Git
- Archivo .gitignore para Python
- Estructura de directorios:
  - `/core` para lógica del juego
  - `/cli` para interfaz de texto
  - `/pygame_ui` para interfaz gráfica
  - `/tests` para tests unitarios
  - `/assets` para recursos
- Archivo requirements.txt con dependencias
- README inicial
- Configuración del entorno de desarrollo
- Branch protection en main

### Notas
- Inicio del desarrollo del proyecto
- Primer commit en el repositorio

---

## Tipos de cambios

- **Agregado**: nuevas features
- **Cambiado**: cambios en funcionalidad existente
- **Obsoleto**: features que se van a eliminar
- **Eliminado**: features eliminadas
- **Corregido**: bug fixes
- **Seguridad**: fixes de vulnerabilidades