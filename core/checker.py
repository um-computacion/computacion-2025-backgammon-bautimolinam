"""
Módulo que define la clase Checker para representar las fichas del juego de Backgammon.

Este módulo implementa la representación de una ficha individual siguiendo
el principio de responsabilidad única, encapsulando únicamente los datos
y comportamientos específicos de una ficha.
"""

from typing import Optional


class Checker:
    """
    Representa una ficha individual en el juego de Backgammon.
    
    Esta clase encapsula la información básica de una ficha, incluyendo
    su propietario y posición actual en el tablero.
    """
    
    def __init__(self, player_id: int, position: Optional[int] = None):
        """
        Inicializa una nueva ficha.
        
        Args:
            player_id (int): ID del jugador propietario de la ficha (1 o 2)
            position (Optional[int]): Posición inicial de la ficha en el tablero.
                                    None si la ficha está fuera del tablero.
        
        Raises:
            ValueError: Si player_id no es 1 o 2
        """
        if player_id not in [1, 2]:
            raise ValueError("player_id debe ser 1 o 2")
        
        self.__player_id__ = player_id
        self.__position__ = position
        self.__is_on_bar__ = False
        self.__is_borne_off__ = False
    
    @property
    def player_id(self) -> int:
        """
        Obtiene el ID del jugador propietario de la ficha.
        
        Returns:
            int: ID del jugador (1 o 2)
        """
        return self.__player_id__
    
    @property
    def position(self) -> Optional[int]:
        """
        Obtiene la posición actual de la ficha en el tablero.
        
        Returns:
            Optional[int]: Posición actual (0-23) o None si está fuera del tablero
        """
        return self.__position__
    
    @position.setter
    def position(self, new_position: Optional[int]) -> None:
        """
        Establece una nueva posición para la ficha.
        
        Args:
            new_position (Optional[int]): Nueva posición (0-23) o None
        """
        if new_position is not None and (new_position < 0 or new_position > 23):
            raise ValueError("La posición debe estar entre 0 y 23")
        
        self.__position__ = new_position
    
    @property
    def is_on_bar(self) -> bool:
        """
        Verifica si la ficha está en la barra (capturada).
        
        Returns:
            bool: True si la ficha está en la barra
        """
        return self.__is_on_bar__
    
    def move_to_bar(self) -> None:
        """
        Mueve la ficha a la barra (marca como capturada).
        
        La ficha se considera fuera del tablero cuando está en la barra.
        """
        self.__position__ = None
        self.__is_on_bar__ = True
        self.__is_borne_off__ = False
    
    def move_from_bar_to(self, position: int) -> None:
        """
        Mueve la ficha desde la barra a una posición específica del tablero.
        
        Args:
            position (int): Posición de destino (0-23)
        
        Raises:
            ValueError: Si la posición no es válida
            RuntimeError: Si la ficha no está en la barra
        """
        if not self.__is_on_bar__:
            raise RuntimeError("La ficha no está en la barra")
        
        if position < 0 or position > 23:
            raise ValueError("La posición debe estar entre 0 y 23")
        
        self.__position__ = position
        self.__is_on_bar__ = False
    
    @property
    def is_borne_off(self) -> bool:
        """
        Verifica si la ficha ha sido sacada del tablero.
        
        Returns:
            bool: True si la ficha ha sido sacada
        """
        return self.__is_borne_off__
    
    def bear_off(self) -> None:
        """
        Saca la ficha del tablero (bear off).
        
        Una vez sacada, la ficha no puede volver al juego.
        """
        self.__position__ = None
        self.__is_on_bar__ = False
        self.__is_borne_off__ = True
    
    def move_to(self, new_position: int) -> None:
        """
        Mueve la ficha a una nueva posición en el tablero.
        
        Args:
            new_position (int): Nueva posición (0-23)
        
        Raises:
            ValueError: Si la posición no es válida
            RuntimeError: Si la ficha no está disponible para mover
        """
        if self.__is_borne_off__:
            raise RuntimeError("No se puede mover una ficha que ya fue sacada")
        
        if new_position < 0 or new_position > 23:
            raise ValueError("La posición debe estar entre 0 y 23")
        
        self.__position__ = new_position
        self.__is_on_bar__ = False
    
    def is_movable(self) -> bool:
        """
        Verifica si la ficha puede ser movida.
        
        Returns:
            bool: True si la ficha puede moverse
        """
        return not self.__is_borne_off__
    
    def is_in_home_board(self) -> bool:
        """
        Verifica si la ficha está en el tablero casa del jugador.
        
        Para el jugador 1: puntos 0-5
        Para el jugador 2: puntos 18-23
        
        Returns:
            bool: True si la ficha está en su tablero casa
        """
        if self.__position__ is None:
            return False
        
        if self.__player_id__ == 1:
            return 0 <= self.__position__ <= 5
        else:  # player_id == 2
            return 18 <= self.__position__ <= 23
    
    def __str__(self) -> str:
        """
        Representación en cadena de la ficha.
        
        Returns:
            str: Representación textual de la ficha
        """
        if self.__is_borne_off__:
            return f"Checker(Player {self.__player_id__}, BORNE OFF)"
        elif self.__is_on_bar__:
            return f"Checker(Player {self.__player_id__}, ON BAR)"
        else:
            return f"Checker(Player {self.__player_id__}, Position {self.__position__})"
    
    def __repr__(self) -> str:
        """
        Representación técnica de la ficha.
        
        Returns:
            str: Representación para debugging
        """
        return (f"Checker(player_id={self.__player_id__}, position={self.__position__}, "
                f"is_on_bar={self.__is_on_bar__}, is_borne_off={self.__is_borne_off__})")
    
    def __eq__(self, other) -> bool:
        """
        Compara dos fichas por igualdad.
        
        Args:
            other: Otra ficha a comparar
        
        Returns:
            bool: True si las fichas son iguales
        """
        if not isinstance(other, Checker):
            return False
        
        return (self.__player_id__ == other.__player_id__ and
                self.__position__ == other.__position__ and
                self.__is_on_bar__ == other.__is_on_bar__ and
                self.__is_borne_off__ == other.__is_borne_off__)