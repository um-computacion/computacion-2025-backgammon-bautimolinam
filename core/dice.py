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
    def roll(self) -> Tuple[int, int]:
       
        self.__dice1__ = random.randint(1, 6)
        self.__dice2__ = random.randint(1, 6)
        self.__is_rolled__ = True
        
        # Resetear movimientos
        self.__used_moves__ = []
        
        # Si son dobles, se pueden usar 4 veces
        if self.__dice1__ == self.__dice2__:
            self.__available_moves__ = [self.__dice1__] * 4
        else:
            self.__available_moves__ = [self.__dice1__, self.__dice2__]
        
        return (self.__dice1__, self.__dice2__)
    @property
    def values(self) -> Tuple[int, int]:
        """
        Obtiene los valores actuales de los dados.
        
        Returns:
            Tuple[int, int]: Valores de los dados (dado1, dado2)
        """
    
        return (self.__dice1__, self.__dice2__)
    
    @property
    def available_moves(self) -> List[int]:
        """
        Obtiene los valores de dados disponibles para usar.
        
        Returns:
            List[int]: Lista de valores disponibles para movimientos
        """
        return self.__available_moves__.copy()
    
    @property
    def used_moves(self) -> List[int]:
        
        return self.__used_moves__.copy()
    def use_value(self, value: int) -> bool:
        """
        Marca un valor de dado como utilizado.
        
        Args:
            value (int): Valor del dado a utilizar (1-6)
        
        Returns:
            bool: True si el valor se pudo usar, False si no estaba disponible
        
        Raises:
            InvalidDiceValueException: Si el valor no es válido (1-6)
        """
        if value < 1 or value > 6:
            raise InvalidDiceValueException(value)
        
        if value in self.__available_moves__:
            self.__available_moves__.remove(value)
            self.__used_moves__.append(value)
            return True
        
        return False
    
    def can_use_value(self, value: int) -> bool:
       
        return value in self.__available_moves__
    def has_available_moves(self) -> bool:
        """
        Verifica si quedan movimientos disponibles.
        
        Returns:
            bool: True si hay movimientos disponibles
        """
        return len(self.__available_moves__) > 0
    
    def is_double(self) -> bool:
        """
        Verifica si la última tirada fueron dobles.
        
        Returns:
            bool: True si fueron dobles
        """
        return self.__is_rolled__ and self.__dice1__ == self.__dice2__
    
    def get_max_available_value(self) -> int:
        """
        Obtiene el valor máximo disponible entre los dados.
        
        Returns:
            int: Valor máximo disponible, 0 si no hay movimientos disponibles
        """
        if not self.__available_moves__:
            return 0
        return max(self.__available_moves__)
    