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
    def make_move(self, from_point: int, to_point: int) -> bool:
       
        self._validate_game_in_progress()
        
        # Calcular el valor de dado necesario
        dice_value = self._calculate_dice_value(from_point, to_point)
        
        if dice_value == 0 or not self.__dice__.can_use_value(dice_value):
            raise InvalidMoveException(from_point, to_point, "Movimiento no válido o dado no disponible")
        
        # Realizar el movimiento según el tipo
        try:
            if from_point == -1:
                # Entrada desde la barra
                self.__board__.enter_from_bar(to_point, self.__current_player_id__)
            elif to_point == -1:
                # Bear off
                self.__board__.bear_off_checker(from_point, self.__current_player_id__, dice_value)
            else:
                # Movimiento normal
                self.__board__.move_checker(from_point, to_point, self.__current_player_id__)
            
            # Marcar el dado como usado
            self.__dice__.use_value(dice_value)
            
            # Registrar el movimiento
            self.__move_history__.append({
                'from': from_point,
                'to': to_point,
                'player': self.__current_player_id__,
                'dice': dice_value
            })
            
            # Verificar condición de victoria
            if self.__board__.is_game_won(self.__current_player_id__):
                self.__winner_id__ = self.__current_player_id__
                self.__state__ = GameState.FINISHED
            
            return True
            
        except Exception as e:
            raise InvalidMoveException(from_point, to_point, str(e))
    
    def end_turn(self) -> None:
        
        self._validate_game_in_progress()
        
        # Cambiar de jugador
        self.__current_player_id__ = 2 if self.__current_player_id__ == 1 else 1
        
        # Reiniciar dados
        self.__dice__.reset()
        
        # Incrementar contador de turnos
        self.__turn_count__ += 1
    
    def _calculate_dice_value(self, from_point: int, to_point: int) -> int:
       
        if from_point == -1:
            # Entrada desde la barra
            if self.__current_player_id__ == 1:
                return 24 - to_point
            else:
                return to_point + 1
        elif to_point == -1:
            # Bear off
            if self.__current_player_id__ == 1:
                return from_point + 1
            else:
                return 24 - from_point
        else:
            # Movimiento normal
            return abs(to_point - from_point)
    
    def get_current_player(self) -> Player:
       
        return self.__player1__ if self.__current_player_id__ == 1 else self.__player2__
    
    def get_player_by_id(self, player_id: int) -> Player:
       
        if player_id == 1:
            return self.__player1__
        elif player_id == 2:
            return self.__player2__
        else:
            raise InvalidPlayerException(player_id)
    
    @property
    def board(self) -> Board:
       
        return self.__board__
    
    @property
    def dice(self) -> Dice:
       
        return self.__dice__
    
    @property
    def state(self) -> GameState:
        
        return self.__state__
    
    @property
    def winner(self) -> Optional[Player]:
       
        if self.__winner_id__:
            return self.get_player_by_id(self.__winner_id__)
        return None
    
    @property
    def turn_count(self) -> int:
       
        return self.__turn_count__
    
    def get_game_status(self) -> Dict[str, Any]:
       
        return {
            'state': self.__state__.value,
            'current_player': self.get_current_player().name,
            'turn_count': self.__turn_count__,
            'dice_rolled': self.__dice__.is_rolled(),
            'dice_values': self.__dice__.values if self.__dice__.is_rolled() else None,
            'available_moves': len(self.get_valid_moves()),
            'player1': {
                'name': self.__player1__.name,
                'borne_off': self.__player1__.checkers_borne_off_count,
                'on_bar': self.__player1__.checkers_on_bar_count
            },
            'player2': {
                'name': self.__player2__.name,
                'borne_off': self.__player2__.checkers_borne_off_count,
                'on_bar': self.__player2__.checkers_on_bar_count
            },
            'winner': self.winner.name if self.winner else None
        }
    
    def reset_game(self) -> None:
        
        # Reiniciar componentes
        self.__board__ = Board()
        self.__player1__.reset_to_starting_position()
        self.__player2__.reset_to_starting_position()
        self.__dice__.reset()
        
        # Reiniciar estado
        self.__state__ = GameState.NOT_STARTED
        self.__current_player_id__ = 1
        self.__winner_id__ = None
        
        # Reiniciar estadísticas
        self.__turn_count__ = 0
        self.__move_history__.clear()
    
    def _validate_game_in_progress(self) -> None:
       
        if self.__state__ == GameState.NOT_STARTED:
            raise GameNotStartedException()
        elif self.__state__ == GameState.FINISHED:
            raise GameAlreadyFinishedException()
    
    def __str__(self) -> str:
        
        lines = []
        lines.append("=== BACKGAMMON GAME ===")
        lines.append(f"Estado: {self.__state__.value}")
        
        if self.__state__ == GameState.IN_PROGRESS:
            lines.append(f"Turno: {self.get_current_player().name}")
            if self.__dice__.is_rolled():
                lines.append(f"Dados: {self.__dice__.values}")
            lines.append(f"Movimientos válidos: {len(self.get_valid_moves())}")
        
        lines.append(f"Turnos: {self.__turn_count__}")
        
        if self.__winner_id__:
            lines.append(f"Ganador: {self.winner.name}")
        
        lines.append("")
        lines.append(str(self.__board__))
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
       
        return (f"BackgammonGame(state={self.__state__.value}, "
                f"current_player={self.__current_player_id__}, "
                f"turn_count={self.__turn_count__})")
    