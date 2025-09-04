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
    
   
   


if __name__ == '__main__':
    unittest.main(verbosity=2)