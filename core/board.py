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
    def move_checker(self, from_point: int, to_point: int, player_id: int) -> Optional[Checker]:
       
        # Validar el movimiento
        if not self.can_move_from_to(from_point, to_point, player_id):
            raise InvalidMoveException(from_point, to_point, "Movimiento no válido")
        
        # Obtener la ficha del punto de origen
        from_checkers = self.get_point_checkers(from_point)
        if not from_checkers or from_checkers[0].player_id != player_id:
            raise CheckerNotAvailableException(from_point, player_id)
        
        # Quitar la ficha del punto de origen
        moving_checker = self.__points__[from_point].pop()
        
        # Verificar si hay que capturar una ficha
        captured_checker = None
        to_checkers = self.get_point_checkers(to_point)
        
        if to_checkers and len(to_checkers) == 1 and to_checkers[0].player_id != player_id:
            # Capturar la ficha del oponente
            captured_checker = self.__points__[to_point].pop()
            self._move_checker_to_bar(captured_checker)
        
        # Colocar la ficha en el punto de destino
        self.__points__[to_point].append(moving_checker)
        moving_checker.move_to(to_point)
        
        return captured_checker
    
    def _move_checker_to_bar(self, checker: Checker) -> None:
        
        checker.move_to_bar()
        if checker.player_id == 1:
            self.__bar_player1__.append(checker)
        else:
            self.__bar_player2__.append(checker)
    
    def get_bar_checkers(self, player_id: int) -> List[Checker]:
       
        if player_id == 1:
            return self.__bar_player1__.copy()
        else:
            return self.__bar_player2__.copy()
    
    def has_checkers_on_bar(self, player_id: int) -> bool:
       
        return len(self.get_bar_checkers(player_id)) > 0
    
    def can_enter_from_bar(self, to_point: int, player_id: int) -> bool:
        
        # Verificar que el jugador tenga fichas en la barra
        if not self.has_checkers_on_bar(player_id):
            return False
        
        # Verificar que el punto esté en el rango correcto para reingreso
        if player_id == 1:
            # Jugador 1 reingresa en puntos 18-23
            if to_point < 18 or to_point > 23:
                return False
        else:
            # Jugador 2 reingresa en puntos 0-5
            if to_point < 0 or to_point > 5:
                return False
        
        # Verificar que el punto esté abierto
        return self.is_point_open(to_point, player_id)
    
    def enter_from_bar(self, to_point: int, player_id: int) -> Optional[Checker]:
      
        if not self.can_enter_from_bar(to_point, player_id):
            raise InvalidMoveException(-1, to_point, "No se puede reingresar desde la barra")
        
        # Sacar ficha de la barra
        if player_id == 1:
            entering_checker = self.__bar_player1__.pop()
        else:
            entering_checker = self.__bar_player2__.pop()
        
        # Verificar si hay que capturar
        captured_checker = None
        to_checkers = self.get_point_checkers(to_point)
        
        if to_checkers and len(to_checkers) == 1 and to_checkers[0].player_id != player_id:
            captured_checker = self.__points__[to_point].pop()
            self._move_checker_to_bar(captured_checker)
        
        # Colocar la ficha en el tablero
        entering_checker.move_from_bar_to(to_point)
        self.__points__[to_point].append(entering_checker)
        
        return captured_checker
    
    def can_bear_off_from(self, from_point: int, player_id: int, dice_value: int) -> bool:
       
        # Verificar que el jugador pueda sacar fichas
        if not self._can_player_bear_off(player_id):
            return False
        
        # Verificar que haya una ficha del jugador en ese punto
        from_checkers = self.get_point_checkers(from_point)
        if not from_checkers or from_checkers[0].player_id != player_id:
            return False
        
        # Calcular el valor necesario para sacar desde ese punto
        if player_id == 1:
            required_value = from_point + 1  # Punto 0 necesita dado 1, etc.
        else:
            required_value = 24 - from_point  # Punto 23 necesita dado 1, etc.
        
        # Se puede usar valor exacto
        if dice_value == required_value:
            return True
        
        # Se puede usar valor mayor si no hay fichas en puntos más alejados
        if dice_value > required_value:
            return not self._has_checkers_further_out(player_id, from_point)
        
        return False
    def _can_player_bear_off(self, player_id: int) -> bool:
       
        # No puede sacar si tiene fichas en la barra
        if self.has_checkers_on_bar(player_id):
            return False
        
        # Verificar que todas las fichas estén en el tablero casa
        home_range = self._get_home_board_range(player_id)
        
        for point in range(24):
            checkers = self.get_point_checkers(point)
            for checker in checkers:
                if (checker.player_id == player_id and 
                    (point < home_range[0] or point > home_range[1])):
                    return False
        
        return True
    
    def _get_home_board_range(self, player_id: int) -> Tuple[int, int]:
      
        if player_id == 1:
            return (0, 5)
        else:
            return (18, 23)
    
    def _has_checkers_further_out(self, player_id: int, from_point: int) -> bool:
       
        home_range = self._get_home_board_range(player_id)
        
        if player_id == 1:
            # Para jugador 1, buscar fichas en puntos mayores dentro del home
            for point in range(from_point + 1, home_range[1] + 1):
                checkers = self.get_point_checkers(point)
                if any(c.player_id == player_id for c in checkers):
                    return True
        else:
            # Para jugador 2, buscar fichas en puntos menores dentro del home
            for point in range(home_range[0], from_point):
                checkers = self.get_point_checkers(point)
                if any(c.player_id == player_id for c in checkers):
                    return True
        
        return False
    
    def bear_off_checker(self, from_point: int, player_id: int, dice_value: int) -> None:
        
        if not self.can_bear_off_from(from_point, player_id, dice_value):
            raise CannotBearOffException(player_id, f"No se puede sacar desde el punto {from_point}")
        
        # Quitar la ficha del punto
        from_checkers = self.get_point_checkers(from_point)
        if not from_checkers or from_checkers[0].player_id != player_id:
            raise CheckerNotAvailableException(from_point, player_id)
        
        borne_off_checker = self.__points__[from_point].pop()
        borne_off_checker.bear_off()
        
        # Agregar a la lista de fichas sacadas
        if player_id == 1:
            self.__borne_off_player1__.append(borne_off_checker)
        else:
            self.__borne_off_player2__.append(borne_off_checker)
    
    def get_borne_off_checkers(self, player_id: int) -> List[Checker]:
       
        if player_id == 1:
            return self.__borne_off_player1__.copy()
        else:
            return self.__borne_off_player2__.copy()
    
    def get_borne_off_count(self, player_id: int) -> int:
        
        return len(self.get_borne_off_checkers(player_id))
    
    def is_game_won(self, player_id: int) -> bool:
       
        return self.get_borne_off_count(player_id) == 15
    
    def get_valid_moves_for_dice(self, player_id: int, dice_value: int) -> List[Tuple[int, int]]:
       
        valid_moves = []
        
        # Si el jugador tiene fichas en la barra, debe moverlas primero
        if self.has_checkers_on_bar(player_id):
            entry_range = self._get_bar_entry_range(player_id)
            
            if player_id == 1:
                target_point = entry_range[1] - dice_value + 1  # 24 - dice_value
            else:
                target_point = entry_range[0] + dice_value - 1  # dice_value - 1
            
            if (entry_range[0] <= target_point <= entry_range[1] and
                self.can_enter_from_bar(target_point, player_id)):
                valid_moves.append((-1, target_point))
        
        else:
            # Movimientos normales y bear off
            for point in range(24):
                checkers = self.get_point_checkers(point)
                if not checkers or checkers[0].player_id != player_id:
                    continue
                
                # Calcular punto de destino
                if player_id == 1:
                    target_point = point - dice_value
                else:
                    target_point = point + dice_value
                
                # Movimiento normal
                if 0 <= target_point <= 23:
                    if self.can_move_from_to(point, target_point, player_id):
                        valid_moves.append((point, target_point))
                
                # Bear off
                elif self.can_bear_off_from(point, player_id, dice_value):
                    valid_moves.append((point, -1))
        
        return valid_moves
    def _get_bar_entry_range(self, player_id: int) -> Tuple[int, int]:
       
        if player_id == 1:
            return (18, 23)  # Jugador 1 reingresa en tablero casa del jugador 2
        else:
            return (0, 5)    # Jugador 2 reingresa en tablero casa del jugador 1
    
    def get_pip_count(self, player_id: int) -> int:
        
      
        pip_count = 0
        
        # Fichas en el tablero
        for point in range(24):
            checkers = self.get_point_checkers(point)
            player_checkers_count = sum(1 for c in checkers if c.player_id == player_id)
            
            if player_checkers_count > 0:
                if player_id == 1:
                    # Jugador 1: distancia desde punto 0
                    distance = point + 1
                else:
                    # Jugador 2: distancia hasta punto 23
                    distance = 24 - point
                
                pip_count += player_checkers_count * distance
        
        # Fichas en la barra (distancia máxima + 1)
        bar_checkers_count = len(self.get_bar_checkers(player_id))
        pip_count += bar_checkers_count * 25
        
        return pip_count
    
    def get_board_representation(self) -> Dict[str, any]:
       
        representation = {
            'points': {},
            'bar': {
                'player1': len(self.__bar_player1__),
                'player2': len(self.__bar_player2__)
            },
            'borne_off': {
                'player1': len(self.__borne_off_player1__),
                'player2': len(self.__borne_off_player2__)
            },
            'pip_count': {
                'player1': self.get_pip_count(1),
                'player2': self.get_pip_count(2)
            }
        }
        
        # Estado de cada punto
        for point in range(24):
            checkers = self.get_point_checkers(point)
            if checkers:
                representation['points'][point] = {
                    'player_id': checkers[0].player_id,
                    'count': len(checkers)
                }
            else:
                representation['points'][point] = {
                    'player_id': None,
                    'count': 0
                }
        
        return representation
    
    def is_blocked_point_sequence(self, start_point: int, length: int, player_id: int) -> bool:
       
        if start_point < 0 or start_point + length > 24:
            return False
        
        for i in range(length):
            point = start_point + i
            checkers = self.get_point_checkers(point)
            
            if len(checkers) < 2 or checkers[0].player_id != player_id:
                return False
        
        return True
    
   