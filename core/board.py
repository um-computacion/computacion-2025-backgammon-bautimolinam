"""
Módulo que define la clase Board para representar el tablero de Backgammon.

Este módulo implementa la representación del tablero y todas las operaciones
relacionadas con las posiciones, movimientos válidos y reglas del juego.
"""

from typing import List,  Optional, Tuple
from .checker import Checker
from .player import Player
from .exception import (
    InvalidPointException, InvalidMoveException,  CannotBearOffException
)


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    
    Esta clase encapsula la lógica del tablero, incluyendo la validación
    de movimientos, capturas, y todas las reglas específicas del juego.
    Sigue el principio de responsabilidad única: solo maneja el tablero.
    """
    
    def __init__(self):
        """
        Inicializa un tablero vacío de Backgammon.
        """
        # 24 puntos del tablero (cada uno es una lista de fichas)
        self.__points__ = {i: [] for i in range(24)}
        
        # Barras para fichas capturadas
        self.__bar_player1__ = []
        self.__bar_player2__ = []
        
        # Fichas sacadas del tablero
        self.__borne_off_player1__ = []
        self.__borne_off_player2__ = []
    
    def setup_initial_position(self, player1: Player, player2: Player) -> None:
        """
        Configura el tablero con la posición inicial estándar de Backgammon.
        """
        self.clear()
        
        # Colocar fichas de ambos jugadores en sus posiciones iniciales
        for checker in player1.checkers:
            if checker.position is not None:
                self.__points__[checker.position].append(checker)
        
        for checker in player2.checkers:
            if checker.position is not None:
                self.__points__[checker.position].append(checker)
    
    def clear(self) -> None:
        """
        Limpia completamente el tablero, barras y fichas sacadas.
        """
        for point in self.__points__.values():
            point.clear()
        
        self.__bar_player1__.clear()
        self.__bar_player2__.clear()
        self.__borne_off_player1__.clear()
        self.__borne_off_player2__.clear()
    
    # ===== CONSULTAS SOBRE PUNTOS =====
    
    def get_point_checkers(self, point: int) -> List[Checker]:
        """
        Obtiene las fichas en un punto específico.
        """
        if point < 0 or point > 23:
            raise InvalidPointException(point)
        
        return self.__points__[point].copy()
    
    def get_point_owner(self, point: int) -> Optional[int]:
        """
        Obtiene el propietario de un punto (quien tiene fichas ahí).
        """
        checkers = self.get_point_checkers(point)
        return checkers[0].player_id if checkers else None
    
    def is_point_open(self, point: int, player_id: int) -> bool:
        """
        Verifica si un punto está abierto para un jugador.
        """
        checkers = self.get_point_checkers(point)
        
        if not checkers:
            return True  # Punto vacío
        
        if checkers[0].player_id == player_id:
            return True  # Fichas propias
        
        if len(checkers) == 1:
            return True  # Una ficha del oponente (se puede capturar)
        
        return False  # Dos o más fichas del oponente (bloqueado)
    
    # ===== MOVIMIENTOS NORMALES =====
    
    def can_move_from_to(self, from_point: int, to_point: int, player_id: int) -> bool:
        """
        Verifica si es posible mover una ficha entre dos puntos.
        """
        # Validar rango de puntos
        if from_point < 0 or from_point > 23 or to_point < 0 or to_point > 23:
            return False
        
        # Verificar que haya una ficha del jugador en el origen
        from_checkers = self.get_point_checkers(from_point)
        if not from_checkers or from_checkers[0].player_id != player_id:
            return False
        
        # Verificar que el destino esté abierto
        if not self.is_point_open(to_point, player_id):
            return False
        
        # Verificar dirección correcta
        if player_id == 1 and to_point >= from_point:
            return False  # Jugador 1 va hacia puntos menores
        
        if player_id == 2 and to_point <= from_point:
            return False  # Jugador 2 va hacia puntos mayores
        
        return True
    
    def move_checker(self, from_point: int, to_point: int, player_id: int) -> Optional[Checker]:
        """
        Mueve una ficha de un punto a otro.
        """
        if not self.can_move_from_to(from_point, to_point, player_id):
            raise InvalidMoveException(from_point, to_point, "Movimiento no válido")
        
        # Quitar ficha del origen
        moving_checker = self.__points__[from_point].pop()
        
        # Verificar captura
        captured_checker = None
        to_checkers = self.get_point_checkers(to_point)
        
        if to_checkers and len(to_checkers) == 1 and to_checkers[0].player_id != player_id:
            # Capturar ficha del oponente
            captured_checker = self.__points__[to_point].pop()
            self._move_to_bar(captured_checker)
        
        # Colocar ficha en el destino
        self.__points__[to_point].append(moving_checker)
        moving_checker.move_to(to_point)
        
        return captured_checker
    
    # ===== BARRA (FICHAS CAPTURADAS) =====
    
    def _move_to_bar(self, checker: Checker) -> None:
        """
        Mueve una ficha capturada a la barra
        """
        checker.move_to_bar()
        if checker.player_id == 1:
            self.__bar_player1__.append(checker)
        else:
            self.__bar_player2__.append(checker)
    
    def has_checkers_on_bar(self, player_id: int) -> bool:
        """
        Verifica si un jugador tiene fichas en la barra.
        """
        bar = self.__bar_player1__ if player_id == 1 else self.__bar_player2__
        return len(bar) > 0
    
    def can_enter_from_bar(self, to_point: int, player_id: int) -> bool:
        """
        Verifica si una ficha puede reingresar desde la barra.
        """
        if not self.has_checkers_on_bar(player_id):
            return False
        
        # Verificar rango de reingreso correcto
        if player_id == 1:
            if to_point < 18 or to_point > 23:
                return False
        else:
            if to_point < 0 or to_point > 5:
                return False
        
        return self.is_point_open(to_point, player_id)
    
    def enter_from_bar(self, to_point: int, player_id: int) -> Optional[Checker]:
        """
        Reingresa una ficha desde la barra al tablero.
        """
        if not self.can_enter_from_bar(to_point, player_id):
            raise InvalidMoveException(-1, to_point, "No se puede reingresar desde la barra")
        
        # Sacar ficha de la barra
        bar = self.__bar_player1__ if player_id == 1 else self.__bar_player2__
        entering_checker = bar.pop()
        
        # Verificar captura
        captured_checker = None
        to_checkers = self.get_point_checkers(to_point)
        
        if to_checkers and len(to_checkers) == 1 and to_checkers[0].player_id != player_id:
            captured_checker = self.__points__[to_point].pop()
            self._move_to_bar(captured_checker)
        
        # Colocar ficha en el tablero
        entering_checker.move_from_bar_to(to_point)
        self.__points__[to_point].append(entering_checker)
        
        return captured_checker
    
    # ===== BEAR OFF (SACAR FICHAS) =====
    
    def can_bear_off_from(self, from_point: int, player_id: int, dice_value: int) -> bool:
        """
        Verifica si se puede sacar una ficha desde un punto específico.
        """
        # Verificar que el jugador pueda sacar fichas
        if not self._can_bear_off(player_id):
            return False
        
        # Verificar que haya una ficha del jugador en ese punto
        from_checkers = self.get_point_checkers(from_point)
        if not from_checkers or from_checkers[0].player_id != player_id:
            return False
        
        # Calcular el valor exacto necesario
        if player_id == 1:
            required_value = from_point + 1
        else:
            required_value = 24 - from_point
        
        # Valor exacto: siempre se puede
        if dice_value == required_value:
            return True
        
        # Valor mayor: solo si no hay fichas más alejadas
        if dice_value > required_value:
            return not self._has_checkers_further(player_id, from_point)
        
        return False
    
    def bear_off_checker(self, from_point: int, player_id: int, dice_value: int) -> None:
        """
        Saca una ficha del tablero.
        """
        if not self.can_bear_off_from(from_point, player_id, dice_value):
            raise CannotBearOffException(player_id, f"No se puede sacar desde {from_point}")
        
        # Quitar la ficha del punto
        borne_off_checker = self.__points__[from_point].pop()
        borne_off_checker.bear_off()
        
        # Agregar a la lista de fichas sacadas
        if player_id == 1:
            self.__borne_off_player1__.append(borne_off_checker)
        else:
            self.__borne_off_player2__.append(borne_off_checker)
    
    def _can_bear_off(self, player_id: int) -> bool:
        """
        Verifica si un jugador puede empezar a sacar fichas.
        """
        # No puede sacar si tiene fichas en la barra
        if self.has_checkers_on_bar(player_id):
            return False
        
        # Todas las fichas deben estar en el tablero casa
        home_start, home_end = self._get_home_range(player_id)
        
        for point in range(24):
            checkers = self.get_point_checkers(point)
            for checker in checkers:
                if checker.player_id == player_id:
                    if point < home_start or point > home_end:
                        return False
        
        return True
    
    def _get_home_range(self, player_id: int) -> Tuple[int, int]:
        """
        Obtiene el rango del tablero casa para un jugador.
        """
        return (0, 5) if player_id == 1 else (18, 23)
    
    def _has_checkers_further(self, player_id: int, from_point: int) -> bool:
        """
        Verifica si el jugador tiene fichas más alejadas del objetivo.
        """
        home_start, home_end = self._get_home_range(player_id)
        
        if player_id == 1:
            # Buscar fichas en puntos mayores
            search_range = range(from_point + 1, home_end + 1)
        else:
            # Buscar fichas en puntos menores
            search_range = range(home_start, from_point)
        
        for point in search_range:
            checkers = self.get_point_checkers(point)
            if any(c.player_id == player_id for c in checkers):
                return True
        
        return False
    
    # ===== MOVIMIENTOS VÁLIDOS =====
    
    def get_valid_moves_for_dice(self, player_id: int, dice_value: int) -> List[Tuple[int, int]]:
        """
        Obtiene todos los movimientos válidos para un valor de dado específico.
        """
        valid_moves = []
        
        # Si hay fichas en la barra, deben moverse primero
        if self.has_checkers_on_bar(player_id):
            target = self._calculate_bar_entry_point(player_id, dice_value)
            if target is not None and self.can_enter_from_bar(target, player_id):
                valid_moves.append((-1, target))
        else:
            # Movimientos normales y bear off
            for point in range(24):
                checkers = self.get_point_checkers(point)
                if not checkers or checkers[0].player_id != player_id:
                    continue
                
                # Calcular destino
                target = point - dice_value if player_id == 1 else point + dice_value
                
                # Movimiento normal
                if 0 <= target <= 23 and self.can_move_from_to(point, target, player_id):
                    valid_moves.append((point, target))
                
                # Bear off
                elif self.can_bear_off_from(point, player_id, dice_value):
                    valid_moves.append((point, -1))
        
        return valid_moves
    
    def _calculate_bar_entry_point(self, player_id: int, dice_value: int) -> Optional[int]:
       
        if player_id == 1:
            target = 24 - dice_value
            return target if 18 <= target <= 23 else None
        else:
            target = dice_value - 1
            return target if 0 <= target <= 5 else None
    
    # ===== ESTADO Y VICTORIA =====
    
    def is_game_won(self, player_id: int) -> bool:
       
        borne_off = self.__borne_off_player1__ if player_id == 1 else self.__borne_off_player2__
        return len(borne_off) == 15
    
    def get_borne_off_count(self, player_id: int) -> int:
        
        borne_off = self.__borne_off_player1__ if player_id == 1 else self.__borne_off_player2__
        return len(borne_off)
    
    # ===== REPRESENTACIÓN =====
    
    def __str__(self) -> str:
       
        lines = ["Backgammon Board:", "=" * 50]
        
        # Puntos superiores (12-23)
        upper = []
        for point in range(12, 24):
            checkers = self.get_point_checkers(point)
            if checkers:
                char = 'X' if checkers[0].player_id == 1 else 'O'
                upper.append(f"{point:2d}:{char}({len(checkers)})")
            else:
                upper.append(f"{point:2d}:  ")
        
        lines.append(" ".join(upper))
        lines.append("-" * 50)
        
        # Información central
        bar1 = len(self.__bar_player1__)
        bar2 = len(self.__bar_player2__)
        off1 = len(self.__borne_off_player1__)
        off2 = len(self.__borne_off_player2__)
        lines.append(f"Bar: P1({bar1}) P2({bar2}) | Out: P1({off1}) P2({off2})")
        lines.append("-" * 50)
        
        # Puntos inferiores (11-0)
        lower = []
        for point in range(11, -1, -1):
            checkers = self.get_point_checkers(point)
            if checkers:
                char = 'X' if checkers[0].player_id == 1 else 'O'
                lower.append(f"{point:2d}:{char}({len(checkers)})")
            else:
                lower.append(f"{point:2d}:  ")
        
        lines.append(" ".join(lower))
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
       
        return (f"Board(bar_p1={len(self.__bar_player1__)}, bar_p2={len(self.__bar_player2__)}, "
                f"off_p1={len(self.__borne_off_player1__)}, off_p2={len(self.__borne_off_player2__)})")