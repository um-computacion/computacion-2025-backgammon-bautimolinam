"""
Tests unitarios para la clase Dice.

Estos tests verifican el comportamiento correcto de los dados del juego
de Backgammon, incluyendo tiradas, dobles, y uso de valores.
"""

import unittest
from unittest.mock import patch
from core.dice import Dice
from core.exceptions import InvalidDiceValueException


class TestDice(unittest.TestCase):
    """
    Tests para la clase Dice que maneja las tiradas de dados.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.__dice__ = Dice(seed=42)  # Seed fijo para tests reproducibles
    
    def test_initialization(self):
        """
        Verifica la inicialización correcta de los dados.
        """
        self.assertEqual(self.__dice__.values, (0, 0))
        self.assertEqual(self.__dice__.available_moves, [])
        self.assertEqual(self.__dice__.used_moves, [])
        self.assertFalse(self.__dice__.is_rolled())
        self.assertFalse(self.__dice__.is_double())
        self.assertFalse(self.__dice__.has_available_moves())
    
    @patch('core.dice.random.randint')
    def test_roll_normal_dice(self, mock_randint):
        """
        Verifica tirada normal de dados (no dobles).
        """
        mock_randint.side_effect = [4, 6]
        
        result = self.__dice__.roll()
        
        self.assertEqual(result, (4, 6))
        self.assertEqual(self.__dice__.values, (4, 6))
        self.assertTrue(self.__dice__.is_rolled())
        self.assertFalse(self.__dice__.is_double())
        self.assertEqual(set(self.__dice__.available_moves), {4, 6})
        self.assertEqual(self.__dice__.used_moves, [])
        self.assertTrue(self.__dice__.has_available_moves())
    
    @patch('core.dice.random.randint')
    def test_roll_double_dice(self, mock_randint):
        """
        Verifica tirada de dados dobles.
        """
        mock_randint.side_effect = [5, 5]
        
        result = self.__dice__.roll()
        
        self.assertEqual(result, (5, 5))
        self.assertEqual(self.__dice__.values, (5, 5))
        self.assertTrue(self.__dice__.is_rolled())
        self.assertTrue(self.__dice__.is_double())
        self.assertEqual(self.__dice__.available_moves, [5, 5, 5, 5])
        self.assertEqual(len(self.__dice__.available_moves), 4)
        self.assertTrue(self.__dice__.has_available_moves())
    


if __name__ == '__main__':
    unittest.main(verbosity=2)