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
    def get_min_available_value(self) -> int:
        """
        Obtiene el valor mínimo disponible entre los dados.
        
        Returns:
            int: Valor mínimo disponible, 0 si no hay movimientos disponibles
        """
        if not self.__available_moves__:
            return 0
        return min(self.__available_moves__)
    
    def can_use_exact_value(self, value: int) -> bool:
      
        return value in self.__available_moves__
    
    def can_use_value_or_higher(self, min_value: int) -> bool:
        """
        Verifica si hay algún valor disponible igual o mayor al especificado.
       """
        return any(value >= min_value for value in self.__available_moves__)
    
    def get_usable_value_for_bear_off(self, required_value: int) -> int:
        """
        Obtiene un valor utilizable para bear off.
        
        """
        # Primero intentar el valor exacto
        if required_value in self.__available_moves__:
            return required_value
        
        # Si no está disponible, buscar el menor valor mayor
        available_higher = [v for v in self.__available_moves__ if v > required_value]
        if available_higher:
            return min(available_higher)
        
        return 0
    def reset(self) -> None:
        """
        Reinicia el estado de los dados.
        
        Limpia todos los valores y marca como no tirados.
        """
        self.__dice1__ = 0
        self.__dice2__ = 0
        self.__available_moves__ = []
        self.__used_moves__ = []
        self.__is_rolled__ = False
    
    def is_rolled(self) -> bool:
        """
        Verifica si ya se realizó una tirada.
        
        Returns:
            bool: True si ya se tiró
        """
        return self.__is_rolled__
    
    def __str__(self) -> str:
        """
        Representación en cadena de los dados.
        
        Returns:
            str: Representación textual de los dados
        """
        if not self.__is_rolled__:
            return "Dice(Not rolled)"
        
        double_text = " (DOUBLES)" if self.is_double() else ""
        available_text = f", Available: {self.__available_moves__}" if self.__available_moves__ else ""
        used_text = f", Used: {self.__used_moves__}" if self.__used_moves__ else ""
        
        return f"Dice({self.__dice1__}, {self.__dice2__}){double_text}{available_text}{used_text}"
    
    def __repr__(self) -> str:
        """
        Representación técnica de los dados.
        
        Returns:
            str: Representación para debugging
        """
        return (f"Dice(dice1={self.__dice1__}, dice2={self.__dice2__}, "
                f"available_moves={self.__available_moves__}, used_moves={self.__used_moves__}, "
                f"is_rolled={self.__is_rolled__})")
    
    def get_min_available_value(self) -> int:
        """
        Obtiene el valor mínimo disponible entre los dados.
        
        Returns:
            int: Valor mínimo disponible, 0 si no hay movimientos disponibles
        """
        if not self.__available_moves__:
            return 0
        return min(self.__available_moves__)
    
    def can_use_exact_value(self, value: int) -> bool:
        """
        Verifica si se puede usar exactamente un valor específico.
        

        """
        return value in self.__available_moves__
    
    def can_use_value_or_higher(self, min_value: int) -> bool:
        """
        Verifica si hay algún valor disponible igual o mayor al especificado.
        
        Útil para bear off cuando se puede usar un valor mayor.
        
        Args:
            min_value (int): Valor mínimo requerido
        
        Returns:
            bool: True si hay un valor >= min_value disponible
        """
        return any(value >= min_value for value in self.__available_moves__)
    def get_usable_value_for_bear_off(self, required_value: int) -> int:
        """
        Obtiene un valor utilizable para bear off.
        
        En bear off, se puede usar un valor mayor si el requerido no está disponible.
        
        Args:
            required_value (int): Valor exacto necesario
        
        Returns:
            int: Valor que se puede usar, 0 si ninguno está disponible
        """
        # Primero intentar el valor exacto
        if required_value in self.__available_moves__:
            return required_value
        
        # Si no está disponible, buscar el menor valor mayor
        available_higher = [v for v in self.__available_moves__ if v > required_value]
        if available_higher:
            return min(available_higher)
        
        return 0
    
    def reset(self) -> None:
        """
        Reinicia el estado de los dados.
        
        Limpia todos los valores y marca como no tirados.
        """
        self.__dice1__ = 0
        self.__dice2__ = 0
        self.__available_moves__ = []
        self.__used_moves__ = []
        self.__is_rolled__ = False
    
    def is_rolled(self) -> bool:
        """
        Verifica si ya se realizó una tirada.
        
        Returns:
            bool: True si ya se tiró
        """
        return self.__is_rolled__
    
    def __str__(self) -> str:
        """
        Representación en cadena de los dados.
        
        Returns:
            str: Representación textual de los dados
        """
        if not self.__is_rolled__:
            return "Dice(Not rolled)"
        
        double_text = " (DOUBLES)" if self.is_double() else ""
        available_text = f", Available: {self.__available_moves__}" if self.__available_moves__ else ""
        used_text = f", Used: {self.__used_moves__}" if self.__used_moves__ else ""
        
        return f"Dice({self.__dice1__}, {self.__dice2__}){double_text}{available_text}{used_text}"
    
    def __repr__(self) -> str:
        """
        Representación técnica de los dados.
        
        Returns:
            str: Representación para debugging
        """
        return (f"Dice(dice1={self.__dice1__}, dice2={self.__dice2__}, "
                f"available_moves={self.__available_moves__}, used_moves={self.__used_moves__}, "
                f"is_rolled={self.__is_rolled__})")