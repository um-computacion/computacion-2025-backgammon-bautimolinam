"""
Tests unitarios para la clase BackgammonGame.

Estos tests verifican el funcionamiento correcto de la lógica principal
del juego, siguiendo las buenas prácticas de testing especificadas
en el documento del proyecto.
"""

import unittest
from unittest.mock import Mock, patch
from core.game import BackgammonGame, GameState, MoveType
from core.exception import (
    GameNotStartedException, GameAlreadyFinishedException,
    InvalidMoveException, InvalidPlayerException
)


class TestBackgammonGame(unittest.TestCase):
    """
    Conjunto de tests para la clase BackgammonGame.
    
    Verifica que el juego coordine correctamente todos los componentes
    y aplique las reglas del Backgammon adecuadamente.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.__game__ = BackgammonGame("Jugador 1", "Jugador 2")
    
    def test_initialization(self):
        """
        Verifica que el juego se inicialice correctamente.
        """
        # Verificar estado inicial
        self.assertEqual(self.__game__.state, GameState.NOT_STARTED)
        self.assertEqual(self.__game__.turn_count, 0)
        self.assertEqual(self.__game__.total_moves, 0)
        self.assertIsNone(self.__game__.winner)
        
        # Verificar jugadores
        player1 = self.__game__.get_player_by_id(1)
        player2 = self.__game__.get_player_by_id(2)
        
        self.assertEqual(player1.name, "Jugador 1")
        self.assertEqual(player2.name, "Jugador 2")
        self.assertEqual(player1.player_id, 1)
        self.assertEqual(player2.player_id, 2)
        
        # Verificar que los jugadores tengan 15 fichas cada uno
        self.assertEqual(len(player1.checkers), 15)
        self.assertEqual(len(player2.checkers), 15)
    
    def test_start_game(self):
        """
        Verifica que el juego inicie correctamente.
        """
        # Antes de iniciar
        self.assertEqual(self.__game__.state, GameState.NOT_STARTED)
        
        # Iniciar juego
        self.__game__.start_game()
        
        # Verificar estado después de iniciar
        self.assertEqual(self.__game__.state, GameState.WAITING_FOR_INITIAL_ROLL)
        
        # No se debería poder iniciar de nuevo
        with self.assertRaises(GameAlreadyFinishedException):
            self.__game__.start_game()
    
    def test_invalid_player_id(self):
        """
        Verifica que se lance excepción con IDs de jugador inválidos.
        """
        with self.assertRaises(InvalidPlayerException):
            self.__game__.get_player_by_id(0)
        
        with self.assertRaises(InvalidPlayerException):
            self.__game__.get_player_by_id(3)
        
        with self.assertRaises(InvalidPlayerException):
            self.__game__.get_player_by_id(-1)
    
    @patch('core.dice.random.randint')
    def test_roll_dice_for_turn_order(self, mock_randint):
        """
        Verifica la tirada inicial para determinar el orden.
        """
        self.__game__.start_game()
        
        # Simular que el jugador 1 gana la tirada inicial
        mock_randint.side_effect = [6, 4, 3, 2]  # P1 gana, luego dados normales
        
        dice1, dice2, starter = self.__game__.roll_dice_for_turn_order()
        
        self.assertEqual(dice1, 6)
        self.assertEqual(dice2, 4)
        self.assertEqual(starter, 1)
        self.assertEqual(self.__game__.state, GameState.IN_PROGRESS)
        self.assertEqual(self.__game__.get_current_player().player_id, 1)
    
    @patch('core.dice.random.randint')
    def test_roll_dice_for_turn_order_tie(self, mock_randint):
        """
        Verifica el comportamiento en caso de empate en la tirada inicial.
        """
        self.__game__.start_game()
        
        # Simular empate
        mock_randint.side_effect = [4, 4]
        
        dice1, dice2, starter = self.__game__.roll_dice_for_turn_order()
        
        self.assertEqual(dice1, 4)
        self.assertEqual(dice2, 4)
        self.assertEqual(starter, 0)  # Empate
        self.assertEqual(self.__game__.state, GameState.WAITING_FOR_INITIAL_ROLL)
    
    def test_operations_before_game_start(self):
        """
        Verifica que las operaciones fallen antes de iniciar el juego.
        """
        # No se pueden tirar dados sin iniciar
        with self.assertRaises(GameNotStartedException):
            self.__game__.roll_dice()
        
        # No se pueden hacer movimientos sin iniciar
        with self.assertRaises(GameNotStartedException):
            self.__game__.make_move(24, 18)
        
        # No se puede terminar turno sin iniciar
        with self.assertRaises(GameNotStartedException):
            self.__game__.end_turn()
    
    @patch('core.dice.random.randint')
    def test_basic_game_flow(self, mock_randint):
        """
        Verifica el flujo básico de una partida.
        """
        # Preparar el juego
        mock_randint.side_effect = [
            6, 4,    # P1 gana orden inicial
            5, 3,    # Dados para el primer turno
            2, 1     # Dados para verificar cambio de turno
        ]
        
        self.__game__.start_game()
        
        # Tirada inicial
        dice1, dice2, starter = self.__game__.roll_dice_for_turn_order()
        self.assertEqual(starter, 1)
        
        # Tirar dados para el turno
        dice1, dice2 = self.__game__.roll_dice()
        self.assertEqual((dice1, dice2), (5, 3))
        
        # Verificar que hay dados disponibles
        available = self.__game__.get_available_dice_values()
        self.assertIn(5, available)
        self.assertIn(3, available)
        
        # Verificar que se pueden obtener movimientos válidos
        valid_moves = self.__game__.get_valid_moves()
        self.assertGreater(len(valid_moves), 0)
    
    def test_game_statistics(self):
        """
        Verifica que las estadísticas del juego se generen correctamente.
        """
        stats = self.__game__.get_game_statistics()
        
        # Verificar estructura básica
        self.assertIn('state', stats)
        self.assertIn('players', stats)
        self.assertIn('dice', stats)
        self.assertIn('board', stats)
        
        # Verificar datos de jugadores
        self.assertIn('player1', stats['players'])
        self.assertIn('player2', stats['players'])
        
        player1_stats = stats['players']['player1']
        self.assertEqual(player1_stats['name'], "Jugador 1")
        self.assertEqual(player1_stats['checkers_borne_off'], 0)
        self.assertEqual(player1_stats['checkers_in_play'], 15)
    
    def test_reset_game(self):
        """
        Verifica que el juego se pueda reiniciar correctamente.
        """
        # Iniciar y modificar el juego
        self.__game__.start_game()
        original_state = self.__game__.state
        
        # Reiniciar
        self.__game__.reset_game()
        
        # Verificar que volvió al estado inicial
        self.assertEqual(self.__game__.state, GameState.NOT_STARTED)
        self.assertEqual(self.__game__.turn_count, 0)
        self.assertEqual(self.__game__.total_moves, 0)
        self.assertEqual(len(self.__game__.get_move_history()), 0)
    
    def test_save_and_load_game_state(self):
        """
        Verifica la funcionalidad de guardar y cargar estado del juego.
        """
        # Configurar un estado específico
        self.__game__.start_game()
        
        # Guardar estado
        saved_state = self.__game__.save_game_state()
        
        # Verificar estructura del estado guardado
        self.assertIn('version', saved_state)
        self.assertIn('state', saved_state)
        self.assertIn('players', saved_state)
        self.assertEqual(saved_state['version'], '1.0')
        
        # Crear un nuevo juego y cargar el estado
        new_game = BackgammonGame()
        success = new_game.load_game_state(saved_state)
        
        # Verificar que se cargó correctamente
        self.assertTrue(success)
        self.assertEqual(new_game.state, self.__game__.state)
        self.assertEqual(new_game.get_player_by_id(1).name, "Jugador 1")
        self.assertEqual(new_game.get_player_by_id(2).name, "Jugador 2")
    
    def test_move_validation(self):
        """
        Verifica la validación básica de movimientos.
        """
        self.__game__.start_game()
        
        # Sin dados tirados, no debería haber movimientos válidos
        self.assertFalse(self.__game__.has_valid_moves())
        
        # Sin dados, cualquier movimiento debería fallar
        self.assertFalse(self.__game__.can_make_move(24, 18))
    
    def test_turn_management(self):
        """
        Verifica el manejo correcto de turnos.
        """
        # Obtener jugador actual inicial
        current_before = self.__game__.get_current_player()
        opponent_before = self.__game__.get_opponent_player()
        
        # Verificar que son diferentes
        self.assertNotEqual(current_before.player_id, opponent_before.player_id)
        
        # Los IDs deben ser 1 y 2
        player_ids = {current_before.player_id, opponent_before.player_id}
        self.assertEqual(player_ids, {1, 2})
    
    def test_pip_count_difference(self):
        """
        Verifica el cálculo de diferencia de pip count.
        """
        # Al inicio, ambos jugadores deberían tener el mismo pip count
        difference = self.__game__.get_pip_count_difference()
        self.assertEqual(difference, 0)
        
        race_status = self.__game__.get_race_status()
        self.assertIsNone(race_status['leader'])  # Empate inicial
    
    def test_string_representations(self):
        """
        Verifica las representaciones en cadena del juego.
        """
        # __str__ debe funcionar sin errores
        str_repr = str(self.__game__)
        self.assertIsInstance(str_repr, str)
        self.assertIn("BACKGAMMON GAME", str_repr)
        
        # __repr__ debe funcionar sin errores
        repr_str = repr(self.__game__)
        self.assertIsInstance(repr_str, str)
        self.assertIn("BackgammonGame", repr_str)


class TestGameIntegration(unittest.TestCase):
    """
    Tests de integración que verifican la interacción entre componentes.
    """
    
    def setUp(self):
        """
        Configuración para tests de integración.
        """
        self.__game__ = BackgammonGame("Tester1", "Tester2")
    
    @patch('core.dice.random.randint')
    def test_complete_game_setup(self, mock_randint):
        """
        Verifica la configuración completa del juego hasta estar listo para jugar.
        """
        # Simular dados para configuración inicial
        mock_randint.side_effect = [5, 3, 6, 1]  # P1 gana, luego dados normales
        
        # Iniciar y configurar juego
        self.__game__.start_game()
        dice1, dice2, starter = self.__game__.roll_dice_for_turn_order()
        
        # Verificar que está listo para jugar
        self.assertEqual(self.__game__.state, GameState.IN_PROGRESS)
        self.assertTrue(starter in [1, 2])
        
        # El tablero debe estar configurado correctamente
        board_stats = self.__game__.board.get_board_representation()
        
        # Verificar que las fichas están en posiciones iniciales
        total_checkers_on_board = sum(
            point['count'] for point in board_stats['points'].values()
        )
        self.assertEqual(total_checkers_on_board, 30)  # 15 fichas por jugador


if __name__ == '__main__':
    # Configurar el runner de tests
    unittest.main(verbosity=2, buffer=True)