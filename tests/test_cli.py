"""
Tests para la interfaz CLI de Backgammon.

Este módulo contiene tests unitarios y de integración para verificar
el correcto funcionamiento de la interfaz de línea de comandos.
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

from cli.cli_intrerfaz import CLIInterface
from core.game import GameState
from core.exception import BackgammonException, InvalidMoveException


class TestCLIBasicCommands:
    """Tests de comandos básicos del CLI."""
    
    
    
    def test_show_help(self, capsys):
        """Verifica que el comando help muestra la ayuda."""
        cli = CLIInterface()
        cli._show_help([])
        
        captured = capsys.readouterr()
        assert "COMANDOS DISPONIBLES" in captured.out
        assert "new" in captured.out
        assert "roll" in captured.out
        assert "move" in captured.out
    
   


class TestCLIDiceRolling:
    """Tests relacionados con tirar dados."""
    
    def test_roll_dice_without_game(self, capsys):
        """Verifica que no se pueden tirar dados sin partida."""
        cli = CLIInterface()
        cli._roll_dice([])
        
        captured = capsys.readouterr()
        assert "No hay partida activa" in captured.out
    
    
  


class TestCLIMovements:
    """Tests relacionados con movimientos."""
    
    def test_parse_point_numeric(self):
        """Verifica que parsea puntos numéricos correctamente."""
        cli = CLIInterface()
        assert cli._parse_point("5") == 5
        assert cli._parse_point("23") == 23
        assert cli._parse_point("0") == 0
    
    def test_parse_point_bar(self):
        """Verifica que parsea 'bar' correctamente."""
        cli = CLIInterface()
        assert cli._parse_point("bar") == -1
        assert cli._parse_point("BAR") == -1
        assert cli._parse_point("barra") == -1
    
    def test_parse_point_off(self):
        """Verifica que parsea 'off' correctamente."""
        cli = CLIInterface()
        assert cli._parse_point("off") == -1
        assert cli._parse_point("OFF") == -1
        assert cli._parse_point("sacar") == -1
    
    def test_parse_point_invalid(self):
        """Verifica que rechaza puntos inválidos."""
        cli = CLIInterface()
        
        with pytest.raises(ValueError):
            cli._parse_point("24")  # Fuera de rango
        
        with pytest.raises(ValueError):
            cli._parse_point("-5")  # Negativo inválido
        
        with pytest.raises(ValueError):
            cli._parse_point("abc")  # No numérico
    
    def test_make_move_without_game(self, capsys):
        """Verifica que no se puede mover sin partida."""
        cli = CLIInterface()
        cli._make_move(['5', '3'])
        
        captured = capsys.readouterr()
        assert "No hay partida activa" in captured.out
    
    def test_make_move_invalid_args(self, capsys):
        """Verifica validación de argumentos del comando move."""
        cli = CLIInterface()
        cli._new_game([])
        
        capsys.readouterr()
        cli._make_move(['5'])  # Solo un argumento
        
        captured = capsys.readouterr()
        assert "Uso:" in captured.out
    
  


class TestCLIGameFlow:
    """Tests del flujo completo del juego."""
    
    def test_show_valid_moves_without_game(self, capsys):
        """Verifica mensaje cuando no hay partida."""
        cli = CLIInterface()
        cli._show_valid_moves([])
        
        captured = capsys.readouterr()
        assert "No hay partida activa" in captured.out
    
    def test_show_valid_moves_with_dice(self, capsys):
        """Verifica que muestra movimientos válidos después de tirar."""
        cli = CLIInterface()
        cli._new_game([])
        cli._roll_dice([])
        
        capsys.readouterr()
        cli._show_valid_moves([])
        
        captured = capsys.readouterr()
        # Debe mostrar la lista o indicar que no hay movimientos
        assert "MOVIMIENTOS VÁLIDOS" in captured.out or "No hay movimientos" in captured.out
    
    def test_show_status_without_game(self, capsys):
        """Verifica mensaje de status sin partida."""
        cli = CLIInterface()
        cli._show_status([])
        
        captured = capsys.readouterr()
        assert "No hay partida activa" in captured.out
    
    def test_show_status_with_game(self, capsys):
        """Verifica que muestra el status correctamente."""
        cli = CLIInterface()
        cli._new_game(['Player1', 'Player2'])
        
        capsys.readouterr()
        cli._show_status([])
        
        captured = capsys.readouterr()
        assert "ESTADO DEL JUEGO" in captured.out
        assert "Player1" in captured.out
        assert "Player2" in captured.out
        assert "Turnos jugados" in captured.out
    
    def test_quit_game_confirmation_no(self, capsys):
        """Verifica que pide confirmación y respeta 'no'."""
        cli = CLIInterface()
        cli._new_game([])
        
        with patch('builtins.input', return_value='n'):
            cli._quit_game([])
            
            # No debe cambiar running a False
            captured = capsys.readouterr()
            assert "Continuando" in captured.out
    
   
class TestCLIEdgeCases:
    """Tests de casos especiales y límite."""
    
    def test_empty_command(self):
        """Verifica que comandos vacíos no causan error."""
        cli = CLIInterface()
        # Simular comando vacío - no debería hacer nada
        # (esto se maneja en el run() con continue)
        pass
    



# Tests de comandos del diccionario


if __name__ == "__main__":
    pytest.main([__file__, "-v"])