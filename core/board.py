"""
Módulo que define la clase Board para representar el tablero de Backgammon.

Este módulo implementa la representación del tablero y todas las operaciones
relacionadas con las posiciones, movimientos válidos y reglas del juego.
"""

from typing import List, Dict, Optional, Tuple
from .checker import Checker
from .player import Player
from .exception import (
    InvalidPointException, InvalidMoveException, 
    CheckerNotAvailableException, CannotBearOffException
)


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    
    Esta clase encapsula la lógica del tablero, incluyendo la validación
    de movimientos, capturas, y todas las reglas específicas del juego.
    """
    
    def __init__(self):
        
        self.__points__ = {i: [] for i in range(24)}
        
       
        self.__bar_player1__ = []  # Fichas del jugador 1 en la barra
        self.__bar_player2__ = []  # Fichas del jugador 2 en la barra
        
        # Fichas sacadas del tablero
        self.__borne_off_player1__ = []
        self.__borne_off_player2__ = []
    
    def setup_initial_position(self, player1: Player, player2: Player) -> None:
       
        # Limpiar el tablero
        self.clear()
        
        # Colocar fichas del jugador 1 en posiciones iniciales
        for checker in player1.checkers:
            if checker.position is not None:
                self.__points__[checker.position].append(checker)
        
        # Colocar fichas del jugador 2 en posiciones iniciales
        for checker in player2.checkers:
            if checker.position is not None:
                self.__points__[checker.position].append(checker)
    
    def clear(self) -> None:
        
        for point in self.__points__.values():
            point.clear()
        
        self.__bar_player1__.clear()
        self.__bar_player2__.clear()
        self.__borne_off_player1__.clear()
        self.__borne_off_player2__.clear()
    def get_point_checkers(self, point: int) -> List[Checker]:
       
        if point < 0 or point > 23:
            raise InvalidPointException(point)
        
        return self.__points__[point].copy()
    
    def get_point_owner(self, point: int) -> Optional[int]:
       
        checkers = self.get_point_checkers(point)
        if not checkers:
            return None
        return checkers[0].player_id
   