#!/usr/bin/env python3
"""
Punto de entrada principal para la interfaz de línea de comandos del juego de Backgammon.

Este script inicia la aplicación CLI que permite jugar Backgammon desde la consola.
Sigue las especificaciones del documento de desarrollo del proyecto.
"""

import sys
import os

# Agregar el directorio del proyecto al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.cli_intrerfaz import main as cli_main


def main():
    """
    Función principal que inicia la interfaz CLI del Backgammon.
    """
    print("Iniciando Backgammon - Interfaz de Línea de Comandos")
    print("Desarrollado según especificaciones del curso de Computación 2025")
    print()
    
    try:
        cli_main()
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\nError fatal: {e}")
        print("Por favor, reporta este error si persiste.")
        sys.exit(1)


if __name__ == "__main__":
    main()