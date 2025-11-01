"""
Tests unitarios para la clase Player.

Estos tests verifican el comportamiento correcto de los jugadores
del juego de Backgammon, incluyendo fichas, movimientos y estadísticas.
"""

import unittest
from core.player import Player
from core.checker import Checker


class TestPlayer(unittest.TestCase):
    """
    Tests para la clase Player que representa a los jugadores.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.__player1__ = Player(1, "Alice")
        self.__player2__ = Player(2, "Bob")
    
    def test_initialization_with_name(self):
        """
        Verifica la inicialización correcta con nombre personalizado.
        """
        self.assertEqual(self.__player1__.player_id, 1)
        self.assertEqual(self.__player1__.name, "Alice")
        self.assertEqual(len(self.__player1__.checkers), 15)
        self.assertFalse(self.__player1__.is_turn)
        
        # Verificar que todas las fichas pertenecen al jugador
        for checker in self.__player1__.checkers:
            self.assertEqual(checker.player_id, 1)
    
    def test_initialization_without_name(self):
        """
        Verifica la inicialización con nombre por defecto.
        """
        player = Player(1)
        self.assertEqual(player.name, "Jugador 1")
        
        player2 = Player(2)
        self.assertEqual(player2.name, "Jugador 2")
    
    def test_invalid_player_id(self):
        """
        Verifica que se rechacen IDs de jugador inválidos.
        """
        with self.assertRaises(ValueError):
            Player(0)
        
        with self.assertRaises(ValueError):
            Player(3)
        
        with self.assertRaises(ValueError):
            Player(-1)
    
    def test_name_setter_valid(self):
        """
        Verifica el cambio de nombre válido.
        """
        self.__player1__.name = "NewName"
        self.assertEqual(self.__player1__.name, "NewName")
        
        # Con espacios que se deberían limpiar
        self.__player1__.name = "  Spaced Name  "
        self.assertEqual(self.__player1__.name, "Spaced Name")
    
    def test_name_setter_invalid(self):
        """
        Verifica que se rechacen nombres inválidos.
        """
        with self.assertRaises(ValueError):
            self.__player1__.name = ""
        
        with self.assertRaises(ValueError):
            self.__player1__.name = "   "
        
        with self.assertRaises(ValueError):
            self.__player1__.name = None
    
    def test_initial_positions_player1(self):
        """
        Verifica las posiciones iniciales del jugador 1.
        """
        position_counts = {}
        
        for checker in self.__player1__.checkers:
            pos = checker.position
            position_counts[pos] = position_counts.get(pos, 0) + 1
        
        # Verificar distribución inicial del jugador 1
        expected_positions = {
            23: 2,  # 2 fichas en punto 23
            12: 5,  # 5 fichas en punto 12
            7: 3,   # 3 fichas en punto 7
            5: 5    # 5 fichas en punto 5
        }
        
        self.assertEqual(position_counts, expected_positions)
    
    def test_initial_positions_player2(self):
        """
        Verifica las posiciones iniciales del jugador 2.
        """
        position_counts = {}
        
        for checker in self.__player2__.checkers:
            pos = checker.position
            position_counts[pos] = position_counts.get(pos, 0) + 1
        
        # Verificar distribución inicial del jugador 2
        expected_positions = {
            0: 2,   # 2 fichas en punto 0
            11: 5,  # 5 fichas en punto 11
            16: 3,  # 3 fichas en punto 16
            18: 5   # 5 fichas en punto 18
        }
        
        self.assertEqual(position_counts, expected_positions)
    
    def test_get_checkers_at_position(self):
        """
        Verifica la obtención de fichas en posiciones específicas.
        """
        # Jugador 1 debería tener 2 fichas en punto 23
        checkers_at_23 = self.__player1__.get_checkers_at_position(23)
        self.assertEqual(len(checkers_at_23), 2)
        
        for checker in checkers_at_23:
            self.assertEqual(checker.position, 23)
            self.assertEqual(checker.player_id, 1)
        
        # Posición vacía debería retornar lista vacía
        checkers_empty = self.__player1__.get_checkers_at_position(10)
        self.assertEqual(len(checkers_empty), 0)
    
    def test_checkers_on_bar_operations(self):
        """
        Verifica las operaciones con fichas en la barra.
        """
        # Inicialmente no hay fichas en la barra
        self.assertEqual(self.__player1__.checkers_on_bar_count, 0)
        self.assertFalse(self.__player1__.has_checkers_on_bar())
        self.assertEqual(len(self.__player1__.get_checkers_on_bar()), 0)
        
        # Mover una ficha a la barra
        checker = self.__player1__.checkers[0]
        success = self.__player1__.move_checker_to_bar(checker)
        
        self.assertTrue(success)
        self.assertEqual(self.__player1__.checkers_on_bar_count, 1)
        self.assertTrue(self.__player1__.has_checkers_on_bar())
        self.assertTrue(checker.is_on_bar)
        
        # Verificar lista de fichas en la barra
        bar_checkers = self.__player1__.get_checkers_on_bar()
        self.assertEqual(len(bar_checkers), 1)
        self.assertEqual(bar_checkers[0], checker)
    
    def test_move_checker_from_bar(self):
        """
        Verifica el movimiento de fichas desde la barra.
        """
        # Mover una ficha a la barra primero
        checker = self.__player1__.checkers[0]
        self.__player1__.move_checker_to_bar(checker)
        
        # Mover desde la barra a una posición
        success = self.__player1__.move_checker_from_bar_to(18)
        
        self.assertTrue(success)
        self.assertEqual(self.__player1__.checkers_on_bar_count, 0)
        self.assertFalse(self.__player1__.has_checkers_on_bar())
        self.assertEqual(checker.position, 18)
        self.assertFalse(checker.is_on_bar)
    
    def test_move_checker_from_bar_when_none_available(self):
        """
        Verifica que falle mover desde la barra cuando no hay fichas.
        """
        # No hay fichas en la barra
        success = self.__player1__.move_checker_from_bar_to(18)
        self.assertFalse(success)
    
    def test_bear_off_operations(self):
        """
        Verifica las operaciones de sacar fichas.
        """
        # Inicialmente no hay fichas sacadas
        self.assertEqual(self.__player1__.checkers_borne_off_count, 0)
        self.assertEqual(len(self.__player1__.get_checkers_borne_off()), 0)
        
        # Sacar una ficha del punto 5 (debe estar en tablero casa)
        success = self.__player1__.bear_off_checker_at(5)
        
        # Esto debería fallar porque no puede sacar si no todas las fichas están en casa
        # (el jugador 1 tiene fichas en puntos 7, 12, 23 que no están en casa)
        self.assertFalse(success)
    
    def test_can_bear_off_conditions(self):
        """
        Verifica las condiciones para poder sacar fichas.
        """
        # Inicialmente no puede sacar (fichas fuera del tablero casa)
        self.assertFalse(self.__player1__.can_bear_off())
        
        # Mover todas las fichas al tablero casa para testing
        for checker in self.__player1__.checkers:
            if checker.position > 5:
                checker.move_to(5)  # Mover todas a punto 5 (tablero casa)
        
        # Ahora sí debería poder sacar
        self.assertTrue(self.__player1__.can_bear_off())
        
        # Si hay fichas en la barra, no puede sacar
        self.__player1__.move_checker_to_bar(self.__player1__.checkers[0])
        self.assertFalse(self.__player1__.can_bear_off())
    
    def test_bear_off_when_allowed(self):
        """
        Verifica sacar fichas cuando está permitido.
        """
        # Configurar todas las fichas en el tablero casa
        for i, checker in enumerate(self.__player1__.checkers):
            checker.move_to(i % 6)  # Distribuir en puntos 0-5
        
        # Ahora debería poder sacar
        self.assertTrue(self.__player1__.can_bear_off())
        
        # Sacar una ficha del punto 3
        initial_count = self.__player1__.checkers_borne_off_count
        success = self.__player1__.bear_off_checker_at(3)
        
        self.assertTrue(success)
        self.assertEqual(self.__player1__.checkers_borne_off_count, initial_count + 1)
        
        # Verificar que la ficha fue efectivamente sacada
        borne_off = self.__player1__.get_checkers_borne_off()
        self.assertEqual(len(borne_off), 1)
        self.assertTrue(borne_off[0].is_borne_off)
    
    def test_has_won(self):
        """
        Verifica la condición de victoria.
        """
        # Inicialmente no ha ganado
        self.assertFalse(self.__player1__.has_won())
        
        # Sacar todas las fichas manualmente para testing
        for checker in self.__player1__.checkers:
            checker.bear_off()
        
        # Ahora debería haber ganado
        self.assertTrue(self.__player1__.has_won())
        self.assertEqual(self.__player1__.checkers_borne_off_count, 15)
        self.assertEqual(self.__player1__.checkers_in_play_count, 0)
    
    def test_checkers_in_play_count(self):
        """
        Verifica el conteo de fichas en juego.
        """
        # Inicialmente todas las fichas están en juego
        self.assertEqual(self.__player1__.checkers_in_play_count, 15)
        
        # Sacar algunas fichas
        for i in range(3):
            self.__player1__.checkers[i].bear_off()
        
        self.assertEqual(self.__player1__.checkers_in_play_count, 12)
        self.assertEqual(self.__player1__.checkers_borne_off_count, 3)
    
    def test_get_home_board_range(self):
        """
        Verifica el rango del tablero casa para cada jugador.
        """
        # Jugador 1: puntos 0-5
        range_p1 = self.__player1__.get_home_board_range()
        self.assertEqual(range_p1, (0, 5))
        
        # Jugador 2: puntos 18-23
        range_p2 = self.__player2__.get_home_board_range()
        self.assertEqual(range_p2, (18, 23))
    
    def test_get_direction(self):
        """
        Verifica la dirección de movimiento para cada jugador.
        """
        # Jugador 1 se mueve hacia posiciones menores
        self.assertEqual(self.__player1__.get_direction(), -1)
        
        # Jugador 2 se mueve hacia posiciones mayores
        self.assertEqual(self.__player2__.get_direction(), 1)
    
    def test_get_bar_entry_range(self):
        """
        Verifica el rango de reingreso desde la barra.
        """
        # Jugador 1 reingresa en puntos 18-23 (tablero casa del oponente)
        range_p1 = self.__player1__.get_bar_entry_range()
        self.assertEqual(range_p1, (18, 23))
        
        # Jugador 2 reingresa en puntos 0-5 (tablero casa del oponente)
        range_p2 = self.__player2__.get_bar_entry_range()
        self.assertEqual(range_p2, (0, 5))
    
    def test_turn_management(self):
        """
        Verifica el manejo de turnos.
        """
        # Inicialmente no es turno de nadie
        self.assertFalse(self.__player1__.is_turn)
        self.assertFalse(self.__player2__.is_turn)
        
        # Iniciar turno del jugador 1
        self.__player1__.start_turn()
        self.assertTrue(self.__player1__.is_turn)
        
        # Terminar turno del jugador 1
        self.__player1__.end_turn()
        self.assertFalse(self.__player1__.is_turn)
    
    def test_move_checker_between_positions(self):
        """
        Verifica el movimiento de fichas entre posiciones.
        """
        # El jugador 1 tiene fichas en punto 23
        initial_count_23 = len(self.__player1__.get_checkers_at_position(23))
        self.assertEqual(initial_count_23, 2)
        
        # Mover una ficha de punto 23 a punto 18
        success = self.__player1__.move_checker(23, 18)
        self.assertTrue(success)
        
        # Verificar que se movió correctamente
        self.assertEqual(len(self.__player1__.get_checkers_at_position(23)), 1)
        self.assertEqual(len(self.__player1__.get_checkers_at_position(18)), 1)
    
    def test_move_checker_from_empty_position(self):
        """
        Verifica que falle mover desde posición vacía.
        """
        # El punto 10 debería estar vacío para el jugador 1
        success = self.__player1__.move_checker(10, 8)
        self.assertFalse(success)
    
    def test_reset_to_starting_position(self):
        """
        Verifica el reinicio a posición inicial.
        """
        # Modificar el estado del jugador
        self.__player1__.start_turn()
        checker = self.__player1__.checkers[0]
        checker.bear_off()
        
        # Reiniciar
        self.__player1__.reset_to_starting_position()
        
        # Verificar que volvió al estado inicial
        self.assertFalse(self.__player1__.is_turn)
        
        # Verificar posiciones iniciales
        position_counts = {}
        for checker in self.__player1__.checkers:
            pos = checker.position
            position_counts[pos] = position_counts.get(pos, 0) + 1
            self.assertFalse(checker.is_borne_off)
            self.assertFalse(checker.is_on_bar)
        
        expected_positions = {23: 2, 12: 5, 7: 3, 5: 5}
        self.assertEqual(position_counts, expected_positions)
    
    def test_string_representations(self):
        """
        Verifica las representaciones en cadena.
        """
        # __str__
        str_repr = str(self.__player1__)
        self.assertIn("Alice", str_repr)
        self.assertIn("ID: 1", str_repr)
        self.assertIn("En juego: 15", str_repr)
        self.assertIn("En barra: 0", str_repr)
        self.assertIn("Sacadas: 0", str_repr)
        
        # __repr__
        repr_str = repr(self.__player1__)
        self.assertIn("Player", repr_str)
        self.assertIn("player_id=1", repr_str)
        self.assertIn("name='Alice'", repr_str)
        self.assertIn("checkers_count=15", repr_str)
    
    def test_equality(self):
        """
        Verifica la comparación de igualdad entre jugadores.
        """
        # Jugadores con mismo ID son iguales
        player1_copy = Player(1, "Different Name")
        self.assertEqual(self.__player1__, player1_copy)
        
        # Jugadores con diferente ID no son iguales
        self.assertNotEqual(self.__player1__, self.__player2__)
        
        # Comparación con objeto de otro tipo
        self.assertNotEqual(self.__player1__, "string")
        self.assertNotEqual(self.__player1__, 1)


class TestPlayerComplexScenarios(unittest.TestCase):
    """
    Tests para escenarios complejos y casos edge.
    """
    
    def setUp(self):
        """
        Configuración para tests complejos.
        """
        self.__player__ = Player(1, "TestPlayer")
    
    def test_complete_game_lifecycle(self):
        """
        Verifica el ciclo de vida completo de un jugador en una partida.
        """
        # Estado inicial
        self.assertEqual(self.__player__.checkers_in_play_count, 15)
        self.assertEqual(self.__player__.checkers_borne_off_count, 0)
        self.assertEqual(self.__player__.checkers_on_bar_count, 0)
        self.assertFalse(self.__player__.can_bear_off())
        self.assertFalse(self.__player__.has_won())
        
        # Simular captura: mover ficha a la barra
        checker_to_capture = self.__player__.checkers[0]
        self.__player__.move_checker_to_bar(checker_to_capture)
        
        self.assertTrue(self.__player__.has_checkers_on_bar())
        self.assertEqual(self.__player__.checkers_on_bar_count, 1)
        self.assertFalse(self.__player__.can_bear_off())  # No puede sacar con fichas en barra
        
        # Reingreso desde la barra
        self.__player__.move_checker_from_bar_to(20)
        
        self.assertFalse(self.__player__.has_checkers_on_bar())
        self.assertEqual(self.__player__.checkers_on_bar_count, 0)
        
        # Mover todas las fichas al tablero casa
        for checker in self.__player__.checkers:
            if checker.position is None or checker.position > 5:
                checker.move_to(3)  # Mover al tablero casa
        
        # Ahora puede sacar fichas
        self.assertTrue(self.__player__.can_bear_off())
        
        # Sacar todas las fichas
        for _ in range(15):
            success = self.__player__.bear_off_checker_at(3)
            self.assertTrue(success)
        
        # Verificar victoria
        self.assertTrue(self.__player__.has_won())
        self.assertEqual(self.__player__.checkers_borne_off_count, 15)
        self.assertEqual(self.__player__.checkers_in_play_count, 0)
    
    def test_mixed_checker_states(self):
        """
        Verifica escenarios con fichas en diferentes estados.
        """
        # Configurar fichas en diferentes estados
        checkers = self.__player__.checkers
        
        # 5 fichas en la barra
        for i in range(5):
            checkers[i].move_to_bar()
        
        # 5 fichas sacadas
        for i in range(5, 10):
            checkers[i].bear_off()
        
        # 5 fichas en el tablero (mantener las que están en posiciones iniciales)
        # Las fichas restantes (10-14) ya están en el tablero
        
        # Verificar conteos
        self.assertEqual(self.__player__.checkers_on_bar_count, 5)
        self.assertEqual(self.__player__.checkers_borne_off_count, 5)
        self.assertEqual(self.__player__.checkers_in_play_count, 10)  # 15 - 5 sacadas
        
        # No puede sacar mientras tenga fichas en la barra
        self.assertFalse(self.__player__.can_bear_off())
        
        # Mover fichas de la barra al tablero casa
        bar_checkers = self.__player__.get_checkers_on_bar()
        for i, checker in enumerate(bar_checkers):
            self.__player__.move_checker_from_bar_to(i)  # Posiciones 0-4
        
        # Mover las fichas del tablero al tablero casa
        for checker in self.__player__.checkers:
            if not checker.is_borne_off and not checker.is_on_bar and checker.position > 5:
                checker.move_to(1)
        
        # Ahora debería poder sacar
        self.assertTrue(self.__player__.can_bear_off())
    
    def test_edge_cases_bear_off(self):
        """
        Verifica casos edge del bear off.
        """
        # Mover todas las fichas al tablero casa excepto una
        for checker in self.__player__.checkers[:-1]:
            checker.move_to(3)
        
        # Dejar una ficha fuera del tablero casa
        self.__player__.checkers[-1].move_to(10)
        
        # No debería poder sacar
        self.assertFalse(self.__player__.can_bear_off())
        
        # Mover la última ficha al tablero casa
        self.__player__.checkers[-1].move_to(2)
        
        # Ahora sí puede sacar
        self.assertTrue(self.__player__.can_bear_off())
    
    def test_bear_off_from_empty_position(self):
        """
        Verifica que no se pueda sacar desde posición vacía.
        """
        # Configurar para poder sacar
        for checker in self.__player__.checkers:
            checker.move_to(0)  # Todas en punto 0
        
        self.assertTrue(self.__player__.can_bear_off())
        
        # Intentar sacar desde posición vacía
        success = self.__player__.bear_off_checker_at(5)  # Punto 5 está vacío
        self.assertFalse(success)
        
        # Sacar desde posición ocupada debería funcionar
        success = self.__player__.bear_off_checker_at(0)
        self.assertTrue(success)
    
    def test_invalid_move_operations(self):
        """
        Verifica operaciones de movimiento inválidas.
        """
        # Mover ficha que no existe en esa posición
        success = self.__player__.move_checker(0, 3)  # Punto 0 vacío inicialmente
        self.assertFalse(success)
        
        # Mover checker que no pertenece al jugador (simulado)
        foreign_checker = Checker(2, 10)  # Ficha del jugador 2
        success = self.__player__.move_checker_to_bar(foreign_checker)
        self.assertFalse(success)
    
    def test_checker_distribution_accuracy(self):
        """
        Verifica que la distribución de fichas sea exacta.
        """
        # Contar fichas por posición
        position_distribution = {}
        total_checkers = 0
        
        for checker in self.__player__.checkers:
            pos = checker.position
            if pos is not None:
                position_distribution[pos] = position_distribution.get(pos, 0) + 1
                total_checkers += 1
        
        # Verificar que son exactamente 15 fichas
        self.assertEqual(total_checkers, 15)
        
        # Verificar distribución inicial específica para jugador 1
        expected = {23: 2, 12: 5, 7: 3, 5: 5}
        self.assertEqual(position_distribution, expected)
        
        # Verificar que la suma de fichas por posición es 15
        self.assertEqual(sum(position_distribution.values()), 15)


if __name__ == '__main__':
    unittest.main(verbosity=2)