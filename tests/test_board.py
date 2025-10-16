"""
Tests unitarios para la clase Board.

Estos tests verifican el comportamiento correcto del tablero de Backgammon,
incluyendo movimientos, validaciones, capturas y bear off.
"""

import unittest
from core.board import Board
from core.player import Player
from core.checker import Checker
from core.exception import (
    InvalidPointException, InvalidMoveException,
    CheckerNotAvailableException, CannotBearOffException
)


class TestBoard(unittest.TestCase):
    """
    Tests para la clase Board que representa el tablero de juego.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.__board__ = Board()
        self.__player1__ = Player(1, "Alice")
        self.__player2__ = Player(2, "Bob")
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
    
    def test_initialization(self):
        """
        Verifica la inicialización correcta del tablero.
        """
        empty_board = Board()
        
        # Tablero vacío debe tener 24 puntos vacíos
        for i in range(24):
            checkers = empty_board.get_point_checkers(i)
            self.assertEqual(len(checkers), 0)
    
    def test_setup_initial_position(self):
        """
        Verifica la configuración de la posición inicial estándar.
        """
        # Verificar posiciones del jugador 1
        self.assertEqual(len(self.__board__.get_point_checkers(23)), 2)
        self.assertEqual(len(self.__board__.get_point_checkers(12)), 5)
        self.assertEqual(len(self.__board__.get_point_checkers(7)), 3)
        self.assertEqual(len(self.__board__.get_point_checkers(5)), 5)
        
        # Verificar posiciones del jugador 2
        self.assertEqual(len(self.__board__.get_point_checkers(0)), 2)
        self.assertEqual(len(self.__board__.get_point_checkers(11)), 5)
        self.assertEqual(len(self.__board__.get_point_checkers(16)), 3)
        self.assertEqual(len(self.__board__.get_point_checkers(18)), 5)
        
        # Verificar propietarios
        self.assertEqual(self.__board__.get_point_owner(23), 1)
        self.assertEqual(self.__board__.get_point_owner(0), 2)
    
    def test_get_point_checkers_invalid(self):
        """
        Verifica que se lance excepción con puntos inválidos.
        """
        with self.assertRaises(InvalidPointException):
            self.__board__.get_point_checkers(-1)
        
        with self.assertRaises(InvalidPointException):
            self.__board__.get_point_checkers(24)
    
    def test_is_point_open(self):
        """
        Verifica la detección de puntos abiertos.
        """
        # Punto vacío está abierto
        self.assertTrue(self.__board__.is_point_open(1, 1))
        self.assertTrue(self.__board__.is_point_open(1, 2))
        
        # Punto con fichas propias está abierto
        self.assertTrue(self.__board__.is_point_open(23, 1))
        
        # Punto con 2+ fichas del oponente está bloqueado
        self.assertFalse(self.__board__.is_point_open(23, 2))
    
    def test_can_move_from_to_valid(self):
        """
        Verifica movimientos válidos básicos.
        """
        # Jugador 1 puede mover de 23 a 20
        self.assertTrue(self.__board__.can_move_from_to(23, 20, 1))
        
        # Jugador 2 puede mover de 0 a 3
        self.assertTrue(self.__board__.can_move_from_to(0, 3, 2))
    
    def test_can_move_from_to_invalid(self):
        """
        Verifica que se rechacen movimientos inválidos.
        """
        # Dirección incorrecta
        self.assertFalse(self.__board__.can_move_from_to(23, 24, 1))
        
        # Desde punto sin fichas propias
        self.assertFalse(self.__board__.can_move_from_to(1, 4, 1))
        
        # A punto bloqueado
        self.assertFalse(self.__board__.can_move_from_to(0, 23, 2))
    
    def test_move_checker_normal(self):
        """
        Verifica movimientos normales sin captura.
        """
        # Mover de 23 a 20
        captured = self.__board__.move_checker(23, 20, 1)
        
        self.assertIsNone(captured)
        self.assertEqual(len(self.__board__.get_point_checkers(23)), 1)
        self.assertEqual(len(self.__board__.get_point_checkers(20)), 1)
    
    def test_move_checker_with_capture(self):
        """
        Verifica movimientos con captura.
        """
        # Colocar ficha solitaria del jugador 2 en punto 20
        lone_checker = Checker(2, 20)
        self.__board__._Board__points__[20] = [lone_checker]
        
        # Mover ficha del jugador 1 a punto 20 (captura)
        captured = self.__board__.move_checker(23, 20, 1)
        
        self.assertIsNotNone(captured)
        self.assertEqual(captured.player_id, 2)
        self.assertTrue(captured.is_on_bar)
        self.assertTrue(self.__board__.has_checkers_on_bar(2))
    
    def test_move_checker_invalid(self):
        """
        Verifica que se lancen excepciones en movimientos inválidos.
        """
        with self.assertRaises(InvalidMoveException):
            self.__board__.move_checker(1, 4, 1)  # Punto vacío
    
    def test_bar_operations(self):
        """
        Verifica operaciones con la barra.
        """
        # Inicialmente no hay fichas en la barra
        self.assertFalse(self.__board__.has_checkers_on_bar(1))
        self.assertFalse(self.__board__.has_checkers_on_bar(2))
        
        # Crear captura
        checker = Checker(1, 20)
        self.__board__._move_to_bar(checker)
        
        self.assertTrue(self.__board__.has_checkers_on_bar(1))
        self.assertTrue(checker.is_on_bar)
    
    def test_can_enter_from_bar(self):
        """
        Verifica la validación de reingreso desde la barra.
        """
        # Mover ficha a la barra
        checker = self.__player1__.checkers[0]
        checker.move_to_bar()
        self.__board__._Board__bar_player1__.append(checker)
        
        # Verificar reingreso válido (puntos 18-23 para jugador 1)
        self.assertTrue(self.__board__.can_enter_from_bar(20, 1))
        
        # Reingreso inválido (fuera de rango)
        self.assertFalse(self.__board__.can_enter_from_bar(10, 1))
    
    def test_enter_from_bar(self):
        """
        Verifica el reingreso desde la barra.
        """
        # Colocar ficha en la barra
        checker = Checker(1)
        checker.move_to_bar()
        self.__board__._Board__bar_player1__.append(checker)
        
        # Reingresar en punto 20
        captured = self.__board__.enter_from_bar(20, 1)
        
        self.assertIsNone(captured)
        self.assertFalse(self.__board__.has_checkers_on_bar(1))
        self.assertEqual(len(self.__board__.get_point_checkers(20)), 1)
    



if __name__ == '__main__':
    unittest.main(verbosity=2)