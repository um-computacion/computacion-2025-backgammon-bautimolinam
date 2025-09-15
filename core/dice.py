"""
Módulo que define la clase Dice para manejar las tiradas de dados en Backgammon.

Este módulo implementa la lógica de los dados siguiendo el principio de
responsabilidad única, manejando únicamente las tiradas y los valores disponibles.
"""

import random
from typing import List, Tuple
from .exception import InvalidDiceValueException


class Dice:
    """
    Representa los dados utilizados en el juego de Backgammon.
    
    Esta clase maneja las tiradas de dados, incluyendo las tiradas dobles,
    y mantiene el seguimiento de los valores disponibles para usar.
    """
    
    def __init__(self, seed: int = None):
        """
        Inicializa los dados.
        
        Args:
            seed (int, optional): Semilla para el generador de números aleatorios.
                                 Útil para testing reproducible.
        """
        if seed is not None:
            random.seed(seed)
        
        self.__dice1__ = 0
        self.__dice2__ = 0
        self.__available_moves__ = []
        self.__used_moves__ = []
        self.__is_rolled__ = False