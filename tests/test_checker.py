"""
Tests unitarios para la clase Checker.

Estos tests verifican el comportamiento correcto de las fichas individuales
del juego de Backgammon, incluyendo estados, movimientos y transiciones.
"""

import unittest
from core.checker import Checker


class TestChecker(unittest.TestCase):
    """
    Tests para la clase Checker que representa fichas individuales.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.__checker_p1__ = Checker(1, 12)
        self.__checker_p2__ = Checker(2, 5)
    
    def test_initialization_valid(self):
        """
        Verifica la inicialización correcta de fichas válidas.
        """
        # Ficha del jugador 1 en posición 12
        self.assertEqual(self.__checker_p1__.player_id, 1)
        self.assertEqual(self.__checker_p1__.position, 12)
        self.assertFalse(self.__checker_p1__.is_on_bar)
        self.assertFalse(self.__checker_p1__.is_borne_off)
        self.assertTrue(self.__checker_p1__.is_movable())
        
        # Ficha del jugador 2 en posición 5
        self.assertEqual(self.__checker_p2__.player_id, 2)
        self.assertEqual(self.__checker_p2__.position, 5)
        self.assertFalse(self.__checker_p2__.is_on_bar)
        self.assertFalse(self.__checker_p2__.is_borne_off)
        self.assertTrue(self.__checker_p2__.is_movable())
    
    def test_initialization_without_position(self):
        """
        Verifica la inicialización de fichas sin posición inicial.
        """
        checker = Checker(1)
        
        self.assertEqual(checker.player_id, 1)
        self.assertIsNone(checker.position)
        self.assertFalse(checker.is_on_bar)
        self.assertFalse(checker.is_borne_off)
        self.assertTrue(checker.is_movable())
    
    def test_initialization_invalid_player_id(self):
        """
        Verifica que se lance excepción con player_id inválido.
        """
        with self.assertRaises(ValueError):
            Checker(0)
        
        with self.assertRaises(ValueError):
            Checker(3)
        
        with self.assertRaises(ValueError):
            Checker(-1)
    def test_position_setter_valid(self):
        """
        Verifica el setter de posición con valores válidos.
        """
        checker = Checker(1)
        
        # Posiciones válidas
        for pos in [0, 5, 12, 23]:
            checker.position = pos
            self.assertEqual(checker.position, pos)
        
        # None es válido
        checker.position = None
        self.assertIsNone(checker.position)
    
    def test_position_setter_invalid(self):
        """
        Verifica que el setter de posición rechace valores inválidos.
        """
        checker = Checker(1)
        
        with self.assertRaises(ValueError):
            checker.position = -1
        
        with self.assertRaises(ValueError):
            checker.position = 24
        
        with self.assertRaises(ValueError):
            checker.position = 100    
    def test_move_to_bar(self):
        """
        Verifica el movimiento de fichas a la barra.
        """
        # Mover a la barra
        self.__checker_p1__.move_to_bar()
        
        self.assertIsNone(self.__checker_p1__.position)
        self.assertTrue(self.__checker_p1__.is_on_bar)
        self.assertFalse(self.__checker_p1__.is_borne_off)
        self.assertTrue(self.__checker_p1__.is_movable())
    
    def test_move_from_bar_to_valid_position(self):
        """
        Verifica el movimiento desde la barra a posición válida.
        """
        # Primero mover a la barra
        self.__checker_p1__.move_to_bar()
        self.assertTrue(self.__checker_p1__.is_on_bar)
        
        # Mover desde la barra al punto 18
        self.__checker_p1__.move_from_bar_to(18)
        
        self.assertEqual(self.__checker_p1__.position, 18)
        self.assertFalse(self.__checker_p1__.is_on_bar)
        self.assertFalse(self.__checker_p1__.is_borne_off)
        self.assertTrue(self.__checker_p1__.is_movable())
    
    def test_move_from_bar_invalid_position(self):
        """
        Verifica que mover desde la barra a posición inválida falle.
        """
        self.__checker_p1__.move_to_bar()
        
        with self.assertRaises(ValueError):
            self.__checker_p1__.move_from_bar_to(-1)
        
        with self.assertRaises(ValueError):
            self.__checker_p1__.move_from_bar_to(24)
    
    def test_move_from_bar_when_not_on_bar(self):
        """
        Verifica que falle mover desde la barra si no está en la barra.
        """
        # La ficha no está en la barra
        self.assertFalse(self.__checker_p1__.is_on_bar)
        
        with self.assertRaises(RuntimeError):
            self.__checker_p1__.move_from_bar_to(18)


if __name__ == '__main__':
    unittest.main(verbosity=2)