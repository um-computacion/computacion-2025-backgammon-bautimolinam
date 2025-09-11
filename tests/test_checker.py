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
    def test_bear_off(self):
        """
        Verifica el proceso de sacar fichas del tablero.
        """
        self.__checker_p1__.bear_off()
        
        self.assertIsNone(self.__checker_p1__.position)
        self.assertFalse(self.__checker_p1__.is_on_bar)
        self.assertTrue(self.__checker_p1__.is_borne_off)
        self.assertFalse(self.__checker_p1__.is_movable())
    
    def test_move_to_valid_position(self):
        """
        Verifica movimientos normales a posiciones válidas.
        """
        original_position = self.__checker_p1__.position
        
        self.__checker_p1__.move_to(8)
        
        self.assertEqual(self.__checker_p1__.position, 8)
        self.assertFalse(self.__checker_p1__.is_on_bar)
        self.assertFalse(self.__checker_p1__.is_borne_off)
        self.assertTrue(self.__checker_p1__.is_movable())
    
    def test_move_to_invalid_position(self):
        """
        Verifica que mover a posición inválida falle.
        """
        with self.assertRaises(ValueError):
            self.__checker_p1__.move_to(-1)
        
        with self.assertRaises(ValueError):
            self.__checker_p1__.move_to(24)
    
    def test_move_borne_off_checker(self):
        """
        Verifica que no se pueda mover una ficha ya sacada.
        """
        self.__checker_p1__.bear_off()
        self.assertTrue(self.__checker_p1__.is_borne_off)
        
        with self.assertRaises(RuntimeError):
            self.__checker_p1__.move_to(5)
    
    def test_is_in_home_board_player1(self):
        """
        Verifica detección del tablero casa para jugador 1.
        """
        # Jugador 1: tablero casa es puntos 0-5
        checker = Checker(1, 3)
        self.assertTrue(checker.is_in_home_board())
        
        checker.position = 0
        self.assertTrue(checker.is_in_home_board())
        
        checker.position = 5
        self.assertTrue(checker.is_in_home_board())
        
        # Fuera del tablero casa
        checker.position = 6
        self.assertFalse(checker.is_in_home_board())
        
        checker.position = 12
        self.assertFalse(checker.is_in_home_board())
    def test_is_in_home_board_player2(self):
        """
        Verifica detección del tablero casa para jugador 2.
        """
        # Jugador 2: tablero casa es puntos 18-23
        checker = Checker(2, 20)
        self.assertTrue(checker.is_in_home_board())
        
        checker.position = 18
        self.assertTrue(checker.is_in_home_board())
        
        checker.position = 23
        self.assertTrue(checker.is_in_home_board())
        
        # Fuera del tablero casa
        checker.position = 17
        self.assertFalse(checker.is_in_home_board())
        
        checker.position = 12
        self.assertFalse(checker.is_in_home_board())
    
    def test_is_in_home_board_no_position(self):
        """
        Verifica que fichas sin posición no estén en tablero casa.
        """
        checker = Checker(1)
        checker.position = None
        self.assertFalse(checker.is_in_home_board())
        
        # Ficha en la barra
        checker.move_to_bar()
        self.assertFalse(checker.is_in_home_board())
        
        # Ficha sacada
        checker = Checker(1, 3)
        checker.bear_off()
        self.assertFalse(checker.is_in_home_board())
    def test_string_representations(self):
        """
        Verifica las representaciones en cadena de las fichas.
        """
        # Ficha normal
        str_repr = str(self.__checker_p1__)
        self.assertIn("Player 1", str_repr)
        self.assertIn("Position 12", str_repr)
        
        # Ficha en la barra
        self.__checker_p1__.move_to_bar()
        str_repr = str(self.__checker_p1__)
        self.assertIn("ON BAR", str_repr)
        
        # Ficha sacada
        checker = Checker(2, 5)
        checker.bear_off()
        str_repr = str(checker)
        self.assertIn("BORNE OFF", str_repr)
    def test_repr(self):
        """
        Verifica la representación técnica de las fichas.
        """
        repr_str = repr(self.__checker_p1__)
        self.assertIn("Checker", repr_str)
        self.assertIn("player_id=1", repr_str)
        self.assertIn("position=12", repr_str)
        self.assertIn("is_on_bar=False", repr_str)
        self.assertIn("is_borne_off=False", repr_str)
    
    def test_equality(self):
        """
        Verifica la comparación de igualdad entre fichas.
        """
        # Fichas idénticas
        checker1 = Checker(1, 12)
        checker2 = Checker(1, 12)
        self.assertEqual(checker1, checker2)
        
        # Fichas diferentes por jugador
        checker3 = Checker(2, 12)
        self.assertNotEqual(checker1, checker3)
        
        # Fichas diferentes por posición
        checker4 = Checker(1, 8)
        self.assertNotEqual(checker1, checker4)
        
        # Fichas con estados diferentes
        checker5 = Checker(1, 12)
        checker5.move_to_bar()
        self.assertNotEqual(checker1, checker5)
        
        # Comparación con objeto de otro tipo
        self.assertNotEqual(checker1, "string")
        self.assertNotEqual(checker1, 12)
        self.assertNotEqual(checker1, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)