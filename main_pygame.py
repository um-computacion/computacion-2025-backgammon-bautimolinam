#!/usr/bin/env python3
"""
Punto de entrada principal para el juego de Backgammon (Interfaz Pygame).

Este script inicia la aplicación gráfica con Pygame que permite jugar Backgammon
con una interfaz visual completa.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pygame
except ImportError:
    print("ERROR: Pygame no está instalado")
    print("Por favor ejecuta: pip install pygame")
    sys.exit(1)

from pygame_ui.pygameinterfaz import main as pygame_main


def main():
    """
    Función principal que inicia la interfaz gráfica de Backgammon con Pygame.
    """
    print("Iniciando Backgammon - Interfaz Gráfica con Pygame")
    print("Desarrollado según especificaciones del curso de Computación 2025")
    print()
    print("Controles:")
    print("  N - Nueva partida")
    print("  R - Tirar dados")
    print("  H - Mostrar/ocultar ayuda")
    print("  ESC - Salir")
    print()
    print("Iniciando ventana gráfica...")
    print()
    
    try:
        pygame_main()
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\nError fatal: {e}")
        print("Por favor, reporta este error si persiste.")
        sys.exit(1)


if __name__ == "__main__":
    main()