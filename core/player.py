"""
Módulo que define la clase Player para representar a los jugadores de Backgammon.

Este módulo implementa la representación de un jugador siguiendo el principio
de responsabilidad única, encapsulando los datos y comportamientos específicos
de cada jugador.
"""

from typing import List
from .checker import Checker


class Player:
   
    
    def __init__(self, player_id: int, name: str = None):
       
        if player_id not in [1, 2]:
            raise ValueError("player_id debe ser 1 o 2")
        
        self.__player_id__ = player_id
        self.__name__ = name or f"Jugador {player_id}"
        
        # Crear las 15 fichas del jugador
        self.__checkers__ = [Checker(player_id) for _ in range(15)]
        
        # Estadísticas del jugador
        self.__checkers_on_bar__ = 0
        self.__checkers_borne_off__ = 0
        
        # Estado del juego
        self.__is_turn__ = False
        
        # Inicializar posiciones estándar
        self._initialize_starting_positions()
    
    def _initialize_starting_positions(self) -> None:
        
        checker_index = 0
        
        if self.__player_id__ == 1:
            # 2 fichas en punto 23
            for _ in range(2):
                self.__checkers__[checker_index].position = 23
                checker_index += 1
            
            # 5 fichas en punto 12
            for _ in range(5):
                self.__checkers__[checker_index].position = 12
                checker_index += 1
            
            # 3 fichas en punto 7
            for _ in range(3):
                self.__checkers__[checker_index].position = 7
                checker_index += 1
            
            # 5 fichas en punto 5
            for _ in range(5):
                self.__checkers__[checker_index].position = 5
                checker_index += 1
        
        else:  # player_id == 2
            # 2 fichas en punto 0
            for _ in range(2):
                self.__checkers__[checker_index].position = 0
                checker_index += 1
            
            # 5 fichas en punto 11
            for _ in range(5):
                self.__checkers__[checker_index].position = 11
                checker_index += 1
            
            # 3 fichas en punto 16
            for _ in range(3):
                self.__checkers__[checker_index].position = 16
                checker_index += 1
            
            # 5 fichas en punto 18
            for _ in range(5):
                self.__checkers__[checker_index].position = 18
                checker_index += 1
    
    @property
    def player_id(self) -> int:
       
        return self.__player_id__
    
    @property
    def name(self) -> str:
       
        return self.__name__
    
    @name.setter
    def name(self, new_name: str) -> None:
       
        if not new_name or not new_name.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.__name__ = new_name.strip()
    
    @property
    def checkers(self) -> List[Checker]:
       
        return self.__checkers__.copy()
    
    def get_checkers_at_position(self, position: int) -> List[Checker]:
       
        return [checker for checker in self.__checkers__ 
                if checker.position == position and not checker.is_borne_off]
    
    def get_checkers_on_bar(self) -> List[Checker]:
       
        return [checker for checker in self.__checkers__ if checker.is_on_bar]
    
    def get_checkers_borne_off(self) -> List[Checker]:
        
        return [checker for checker in self.__checkers__ if checker.is_borne_off]
    
    @property
    def checkers_on_bar_count(self) -> int:
       
        return len(self.get_checkers_on_bar())
    
    @property
    def checkers_borne_off_count(self) -> int:
        
        return len(self.get_checkers_borne_off())
    
    @property
    def checkers_in_play_count(self) -> int:
        
        return 15 - self.checkers_borne_off_count
    
    def has_checkers_on_bar(self) -> bool:
        
        return self.checkers_on_bar_count > 0
    
    def can_bear_off(self) -> bool:
        
        # No puede sacar si tiene fichas en la barra
        if self.has_checkers_on_bar():
            return False
        
        # Verificar que todas las fichas estén en el tablero casa
        for checker in self.__checkers__:
            if not checker.is_borne_off and not checker.is_in_home_board():
                return False
        
        return True
    
    def has_won(self) -> bool:
       
        return self.checkers_borne_off_count == 15
    
    def get_home_board_range(self) -> tuple[int, int]:
       
        if self.__player_id__ == 1:
            return (0, 5)  # Puntos 0-5 para jugador 1
        else:
            return (18, 23)  # Puntos 18-23 para jugador 2
    
    def get_direction(self) -> int:
       
        return -1 if self.__player_id__ == 1 else 1
    
   