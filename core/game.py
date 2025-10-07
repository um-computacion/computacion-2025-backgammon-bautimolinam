"""
Módulo que define la clase BackgammonGame que coordina el flujo general del juego.

Esta clase actúa como el controlador principal, coordinando las interacciones
entre el tablero, los jugadores, y los dados, aplicando las reglas del juego.
"""

from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
from .board import Board
from .player import Player
from .dice import Dice
from .exception import (
    GameNotStartedException, GameAlreadyFinishedException, 
    InvalidPlayerException, InvalidMoveException
)


class GameState(Enum):
    """Enumeración para los posibles estados del juego."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class BackgammonGame:
    
    
    def __init__(self, player1_name: str = None, player2_name: str = None):
      
        # Componentes del juego
        self.__board__ = Board()
        self.__player1__ = Player(1, player1_name or "Jugador 1")
        self.__player2__ = Player(2, player2_name or "Jugador 2")
        self.__dice__ = Dice()
        
        # Estado del juego
        self.__state__ = GameState.NOT_STARTED
        self.__current_player_id__ = 1
        self.__winner_id__ = None
        
        # Estadísticas básicas
        self.__turn_count__ = 0
        self.__move_history__ = []
    
    def start_game(self) -> None:
    
        if self.__state__ != GameState.NOT_STARTED:
            raise GameAlreadyFinishedException()
        
        # Configurar tablero inicial
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        
        # Cambiar estado
        self.__state__ = GameState.IN_PROGRESS
        
        # Reiniciar contadores
        self.__turn_count__ = 0
        self.__move_history__.clear()
    
    def roll_dice(self) -> Tuple[int, int]:
        
        self._validate_game_in_progress()
        
        if self.__dice__.is_rolled() and self.__dice__.has_available_moves():
            raise InvalidMoveException(-1, -1, "Ya se tiraron los dados y hay movimientos disponibles")
        
        return self.__dice__.roll()
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
      
        if not self.__dice__.is_rolled():
            return []
        
        valid_moves = []
        
        for dice_value in self.__dice__.available_moves:
            moves = self.__board__.get_valid_moves_for_dice(self.__current_player_id__, dice_value)
            valid_moves.extend(moves)
        
        return valid_moves
    
    