"""
Tests unitarios para la clase Dice - Corregido.
"""

import unittest
from unittest.mock import patch
from core.dice import Dice
from core.exception import InvalidDiceValueException


class TestDice(unittest.TestCase):
    """Tests para la clase Dice."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.__dice__ = Dice(seed=42)
    
    def test_initialization(self):
        """Verifica la inicialización correcta de los dados."""
        self.assertEqual(self.__dice__.values, (0, 0))
        self.assertEqual(self.__dice__.available_moves, [])
        self.assertEqual(self.__dice__.used_moves, [])
        self.assertFalse(self.__dice__.is_rolled())
        self.assertFalse(self.__dice__.is_double())
        self.assertFalse(self.__dice__.has_available_moves())
    
    @patch('core.dice.random.randint')
    def test_roll_normal_dice(self, mock_randint):
        """Verifica tirada normal de dados (no dobles)."""
        mock_randint.side_effect = [4, 6]
        
        result = self.__dice__.roll()
        
        self.assertEqual(result, (4, 6))
        self.assertEqual(self.__dice__.values, (4, 6))
        self.assertTrue(self.__dice__.is_rolled())
        self.assertFalse(self.__dice__.is_double())
        self.assertTrue(self.__dice__.has_available_moves())
    
    @patch('core.dice.random.randint')
    def test_roll_double_dice(self, mock_randint):
        """Verifica tirada de dados dobles."""
        mock_randint.side_effect = [5, 5]
        
        result = self.__dice__.roll()
        
        self.assertEqual(result, (5, 5))
        self.assertEqual(self.__dice__.values, (5, 5))
        self.assertTrue(self.__dice__.is_rolled())
        self.assertTrue(self.__dice__.is_double())
        self.assertEqual(len(self.__dice__.available_moves), 4)
    
    @patch('core.dice.random.randint')
    def test_use_value_valid(self, mock_randint):
        """Verifica el uso correcto de valores de dados disponibles."""
        mock_randint.side_effect = [3, 6]
        self.__dice__.roll()
        
        # Usar el 3
        result = self.__dice__.use_value(3)
        self.assertTrue(result)
        self.assertIn(6, self.__dice__.available_moves)
        self.assertIn(3, self.__dice__.used_moves)
        
        # Usar el 6
        result = self.__dice__.use_value(6)
        self.assertTrue(result)
        self.assertFalse(self.__dice__.has_available_moves())
    
    @patch('core.dice.random.randint')
    def test_use_value_unavailable(self, mock_randint):
        """Verifica que no se pueda usar un valor no disponible."""
        mock_randint.side_effect = [2, 4]
        self.__dice__.roll()
        
        # Intentar usar valor no disponible
        result = self.__dice__.use_value(6)
        self.assertFalse(result)
    
    def test_use_value_invalid_range(self):
        """Verifica que se lance excepción con valores fuera de rango."""
        with self.assertRaises(InvalidDiceValueException):
            self.__dice__.use_value(0)
        
        with self.assertRaises(InvalidDiceValueException):
            self.__dice__.use_value(7)
    
    @patch('core.dice.random.randint')
    def test_use_double_values(self, mock_randint):
        """Verifica el uso de valores en tirada doble."""
        mock_randint.side_effect = [4, 4]
        self.__dice__.roll()
        
        # Usar los cuatro valores de 4
        for i in range(4):
            result = self.__dice__.use_value(4)
            self.assertTrue(result)
        
        # Ya no quedan valores disponibles
        self.assertFalse(self.__dice__.has_available_moves())
    
    @patch('core.dice.random.randint')
    def test_can_use_value(self, mock_randint):
        """Verifica la función de verificación de valores disponibles."""
        # Sin tirar dados
        self.assertFalse(self.__dice__.can_use_value(3))
        
        # Con dados tirados
        mock_randint.side_effect = [2, 5]
        self.__dice__.roll()
        
        self.assertTrue(self.__dice__.can_use_value(2))
        self.assertTrue(self.__dice__.can_use_value(5))
        self.assertFalse(self.__dice__.can_use_value(3))
    
    @patch('core.dice.random.randint')
    def test_get_max_available_value(self, mock_randint):
        """Verifica la obtención del valor máximo disponible."""
        # Sin dados disponibles
        self.assertEqual(self.__dice__.get_max_available_value(), 0)
        
        # Con dados disponibles
        mock_randint.side_effect = [2, 6]
        self.__dice__.roll()
        self.assertEqual(self.__dice__.get_max_available_value(), 6)
    
    @patch('core.dice.random.randint')
    def test_get_min_available_value(self, mock_randint):
        """Verifica la obtención del valor mínimo disponible."""
        # Sin dados disponibles
        self.assertEqual(self.__dice__.get_min_available_value(), 0)
        
        # Con dados disponibles
        mock_randint.side_effect = [2, 6]
        self.__dice__.roll()
        self.assertEqual(self.__dice__.get_min_available_value(), 2)
    
    @patch('core.dice.random.randint')
    def test_can_use_exact_value(self, mock_randint):
        """Verifica la función para valores exactos."""
        mock_randint.side_effect = [1, 3]
        self.__dice__.roll()
        
        self.assertTrue(self.__dice__.can_use_exact_value(1))
        self.assertTrue(self.__dice__.can_use_exact_value(3))
        self.assertFalse(self.__dice__.can_use_exact_value(2))


if __name__ == '__main__':
    unittest.main(verbosity=2)