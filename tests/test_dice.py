"""
Tests unitarios para la clase Dice.

Estos tests verifican el comportamiento correcto de los dados del juego
de Backgammon, incluyendo tiradas, dobles, y uso de valores.
"""

import unittest
from unittest.mock import patch
from core.dice import Dice
from core.exception import InvalidDiceValueException


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
    def test_use_value_valid(self):
        """
        Verifica el uso correcto de valores de dados disponibles.
        """
        # Simular tirada de 3, 6
        self.__dice__._Dice__dice1__ = 3
        self.__dice__._Dice__dice2__ = 6
        self.__dice__._Dice__available_moves__ = [3, 6]
        self.__dice__._Dice__is_rolled__ = True
        
        # Usar el 3
        result = self.__dice__.use_value(3)
        
        self.assertTrue(result)
        self.assertEqual(self.__dice__.available_moves, [6])
        self.assertEqual(self.__dice__.used_moves, [3])
        self.assertTrue(self.__dice__.has_available_moves())
        
        # Usar el 6
        result = self.__dice__.use_value(6)
        
        self.assertTrue(result)
        self.assertEqual(self.__dice__.available_moves, [])
        self.assertEqual(self.__dice__.used_moves, [3, 6])
        self.assertFalse(self.__dice__.has_available_moves())
    def test_use_value_unavailable(self):
        """
        Verifica que no se pueda usar un valor no disponible.
        """
        # Simular tirada de 2, 4
        self.__dice__._Dice__dice1__ = 2
        self.__dice__._Dice__dice2__ = 4
        self.__dice__._Dice__available_moves__ = [2, 4]
        self.__dice__._Dice__is_rolled__ = True
        
        # Intentar usar valor no disponible
        result = self.__dice__.use_value(6)
        
        self.assertFalse(result)
        self.assertEqual(self.__dice__.available_moves, [2, 4])
        self.assertEqual(self.__dice__.used_moves, [])
    
    def test_use_value_invalid_range(self):
        """
        Verifica que se lance excepción con valores fuera de rango.
        """
        with self.assertRaises(InvalidDiceValueException):
            self.__dice__.use_value(0)
        
        with self.assertRaises(InvalidDiceValueException):
            self.__dice__.use_value(7)
        
        with self.assertRaises(InvalidDiceValueException):
            self.__dice__.use_value(-1)
    
    def test_use_double_values(self):
        """
        Verifica el uso de valores en tirada doble.
        """
        # Simular dobles de 4
        self.__dice__._Dice__dice1__ = 4
        self.__dice__._Dice__dice2__ = 4
        self.__dice__._Dice__available_moves__ = [4, 4, 4, 4]
        self.__dice__._Dice__is_rolled__ = True
        
        # Usar los cuatro valores de 4
        for i in range(4):
            result = self.__dice__.use_value(4)
            self.assertTrue(result)
            self.assertEqual(len(self.__dice__.available_moves), 3 - i)
            self.assertEqual(len(self.__dice__.used_moves), i + 1)
        
        # Ya no quedan valores disponibles
        self.assertFalse(self.__dice__.has_available_moves())
        result = self.__dice__.use_value(4)
        self.assertFalse(result)
    def test_can_use_value(self):
        """
        Verifica la función de verificación de valores disponibles.
        """
        # Sin tirar dados
        self.assertFalse(self.__dice__.can_use_value(3))
        
        # Con dados tirados
        self.__dice__._Dice__available_moves__ = [2, 5]
        
        self.assertTrue(self.__dice__.can_use_value(2))
        self.assertTrue(self.__dice__.can_use_value(5))
        self.assertFalse(self.__dice__.can_use_value(3))
        self.assertFalse(self.__dice__.can_use_value(6))
    
    def test_get_max_available_value(self):
        """
        Verifica la obtención del valor máximo disponible.
        """
        # Sin dados disponibles
        self.assertEqual(self.__dice__.get_max_available_value(), 0)
        
        # Con dados disponibles
        self.__dice__._Dice__available_moves__ = [2, 6, 3]
        self.assertEqual(self.__dice__.get_max_available_value(), 6)
        
        # Con un solo dado
        self.__dice__._Dice__available_moves__ = [4]
        self.assertEqual(self.__dice__.get_max_available_value(), 4)
    
    def test_get_min_available_value(self):
        """
        Verifica la obtención del valor mínimo disponible.
        """
        # Sin dados disponibles
        self.assertEqual(self.__dice__.get_min_available_value(), 0)
        
        # Con dados disponibles
        self.__dice__._Dice__available_moves__ = [2, 6, 3]
        self.assertEqual(self.__dice__.get_min_available_value(), 2)
        
        # Con un solo dado
        self.__dice__._Dice__available_moves__ = [5]
        self.assertEqual(self.__dice__.get_min_available_value(), 5)
    
    def test_can_use_exact_value(self):
        """
        Verifica la función para valores exactos.
        """
        self.__dice__._Dice__available_moves__ = [1, 3, 6]
        
        self.assertTrue(self.__dice__.can_use_exact_value(1))
        self.assertTrue(self.__dice__.can_use_exact_value(3))
        self.assertTrue(self.__dice__.can_use_exact_value(6))
        self.assertFalse(self.__dice__.can_use_exact_value(2))
        self.assertFalse(self.__dice__.can_use_exact_value(5))

if __name__ == '__main__':
    unittest.main(verbosity=2)