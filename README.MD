🎲 Juego de Backgammon
Alumno: Molina Bautista
Carrera: Ingeniería en Informática
Universidad: Universidad de Mendoza

📋 Descripción
Implementación del juego clásico de Backgammon en Python con múltiples interfaces:

🖥️ CLI (Interfaz de línea de comandos)
🎮 Pygame (Interfaz gráfica)
Instalación
Clonar el repositorio:https://github.com/um-computacion/computacion-2025-backgammon-bautimolinam.git


Entorno virtual:
python -m venv/venv source venv/bin/activate

Instalar dependencias:
pip install -r requirements.txt

🐳 Inicio Rápido con Docker
Pruebas de Modo
docker run backgammon test
Modo Juego
docker build -t backgammon .
docker run -it backgammon cli
🚀 Instalación
Opción 1: Instalación local
# Clonar el repositorio
git clone https://github.com/um-computacion/computacion-2025-backgammon-bautimolinam.git

# Instalar dependencias
pip install -r requirements.txt
Opción 2: Docker 🐳
Para usar el proyecto con Docker, primero construye la imagen:

docker build -t backgammon-game .
Pruebas de Modo (Pruebas de Eyección)
Ejecuta las pruebas con cobertura usando Docker:

# Con Docker
docker run backgammon test

Esto ejecutará todos los tests unitarios y mostrará el reporte de cobertura.

#### Modo Juego (Jugar Backgammon)

Para jugar al Backgammon en modo CLI usando Docker:

```bash
# Con Docker
docker run -it backgammon cli

## 🎮 Cómo Jugar

### Modo CLI (Terminal)
```bash
python -m cli.cli
Modo Pygame (Gráfico)
python -m pygame_ui.pygame_ui
🧪 Pruebas
# Ejecutar todos los tests
python -m unittest discover -s tests

# Ver coverage
coverage run -m unittest discover -s tests
coverage report -m
📊 Análisis de código
# Pylint
pylint core/ tests/ cli/
📁 Estructura del Proyecto
## 📁 Estructura del Proyecto

```
backgammon/
│
├── core/                           # Lógica central del juego (Business Logic)
│   ├── __init__.py                # Inicialización del módulo core
│   ├── board.py                   # Tablero: 24 puntos, barra, bear off
│   ├── checker.py                 # Ficha individual: estados y movimientos
│   ├── dice.py                    # Sistema de dados: tiradas y disponibilidad
│   ├── player.py                  # Jugador: 15 fichas y estadísticas
│   ├── game.py                    # Coordinador: flujo del juego y reglas
│   └── exception.py               # Excepciones personalizadas del dominio
│
├── cli/                            # Interfaz de Línea de Comandos
│   ├── __init__.py                # Inicialización del módulo cli
│   └── cli_intrerfaz.py           # CLI principal con comandos de texto
│
├── pygame_ui/                      # Interfaz Gráfica (Pygame)
│   ├── __init__.py                # Inicialización del módulo pygame_ui
│   └── pygameinterfaz.py          # Interfaz visual interactiva
│
├── tests/                          # Tests Unitarios y de Integración
│   ├── __init__.py                # Inicialización del módulo tests
│   ├── test_board.py              # Tests del tablero (88-90% cobertura)
│   ├── test_checker.py            # Tests de fichas (95% cobertura)
│   ├── test_dice.py               # Tests de dados (92% cobertura)
│   └── test_game.py               # Tests del juego (85-88% cobertura)
│
├── assets/                         # Recursos (opcional, para expansiones futuras)
│   ├── images/                    # Imágenes (iconos, sprites)
│   └── sounds/                    # Sonidos (efectos, música)
│
├── docs/                           # Documentación adicional
│   └── diagramas/                 # Diagramas UML
│
├── main_cli.py                     # Punto de entrada CLI
├── main_pygame.py                  # Punto de entrada Pygame
│
├── requirements.txt                # Dependencias de producción
├── requirements-dev.txt            # Dependencias de desarrollo
│
├── Dockerfile.test                 # Docker para ejecutar tests
├── Dockerfile.cli                  # Docker para juego CLI
├── Dockerfile.pygame               # Docker para juego gráfico
├── .dockerignore                   # Archivos ignorados por Docker
│
├── README.md                       # Este archivo
├── CHANGELOG.md                    # Historial de cambios (Keep a Changelog)
├── JUSTIFICACION.md                # Justificación de diseño y decisiones
├── COBERTURA_TESTS.md              # Análisis detallado de cobertura
│
├── prompts-desarrollo.md           # Prompts de IA para desarrollo
├── prompts-testing.md              # Prompts de IA para testing

│
├── .gitignore                      # Archivos ignorados por Git
├── .pylintrc                       # Configuración de Pylint
└── pytest.ini                      # Configuración de Pytest
```

Python 3.12
Pygame
Cobertura
Pylint
Estibador