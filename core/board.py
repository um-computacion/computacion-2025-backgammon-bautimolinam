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
    def get_point_checker_count(self, point: int) -> int:
       
        return len(self.get_point_checkers(point))
    
    def is_point_blocked(self, point: int, player_id: int) -> bool:
       
        checkers = self.get_point_checkers(point)
        if len(checkers) >= 2:
            # Está bloqueado si las fichas son del oponente
            return checkers[0].player_id != player_id
        return False
    
    def is_point_open(self, point: int, player_id: int) -> bool:
       
        checkers = self.get_point_checkers(point)
        
        # Punto vacío
        if not checkers:
            return True
        
        # Fichas propias
        if checkers[0].player_id == player_id:
            return True
        
        # Solo una ficha del oponente (se puede capturar)
        if len(checkers) == 1:
            return True
        
        # Dos o más fichas del oponente (bloqueado)
        return False
    
    def can_move_from_to(self, from_point: int, to_point: int, player_id: int) -> bool:
       
        try:
            # Verificar que los puntos sean válidos
            if from_point < 0 or from_point > 23 or to_point < 0 or to_point > 23:
                return False
            
            # Verificar que haya una ficha del jugador en el punto de origen
            from_checkers = self.get_point_checkers(from_point)
            if not from_checkers or from_checkers[0].player_id != player_id:
                return False
            
            # Verificar que el punto de destino esté abierto
            if not self.is_point_open(to_point, player_id):
                return False
            
            # Verificar dirección de movimiento
            if player_id == 1:
                # Jugador 1 se mueve hacia posiciones menores
                if to_point >= from_point:
                    return False
            else:
                # Jugador 2 se mueve hacia posiciones mayores
                if to_point <= from_point:
                    return False
            
            return True
            
        except InvalidPointException:
            return False
    