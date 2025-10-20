

"""
Módulo que implementa la interfaz de línea de comandos para el juego de Backgammon.

Esta interfaz permite a los jugadores interactuar con el juego a través de
comandos de texto, proporcionando una experiencia completa de juego en consola.
"""

import sys
from typing import List, Tuple, Optional


from core.game import BackgammonGame, GameState
from core.exception import (
    BackgammonException, InvalidMoveException, 
    GameNotStartedException, GameAlreadyFinishedException
)


class CLIInterface:
    """
    Interfaz de línea de comandos para el juego de Backgammon.
    
    Esta clase proporciona una interfaz de texto completa que permite
    a los jugadores jugar Backgammon desde la consola.
    """
    
    def __init__(self):
        """
        Inicializa la interfaz CLI.
        """
        self.__game__ = None
        self.__running__ = False
        
        # Comandos disponibles
        self.__commands__ = {
            'help': self._show_help,
            'new': self._new_game,
            'roll': self._roll_dice,
            'move': self._make_move,
            'moves': self._show_valid_moves,
            'board': self._show_board,
            'status': self._show_status,
            'quit': self._quit_game,
            'exit': self._quit_game
        }
    
    def run(self) -> None:
        """
        Ejecuta la interfaz CLI principal.
        """
        self.__running__ = True
        
        print("=" * 60)
        print("       BIENVENIDO AL BACKGAMMON")
        print("=" * 60)
        print("Escribe 'help' para ver los comandos disponibles")
        print("Escribe 'new' para comenzar una nueva partida")
        print("")
        
        while self.__running__:
            try:
                command = input("backgammon> ").strip().lower()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                
                if cmd in self.__commands__:
                    self.__commands__[cmd](args)
                else:
                    print(f"Comando desconocido: {cmd}")
                    print("Escribe 'help' para ver los comandos disponibles")
                
            except KeyboardInterrupt:
                print("\n\nSaliendo del juego...")
                break
            except EOFError:
                print("\n\nSaliendo del juego...")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
    
    def _show_help(self, args: List[str]) -> None:
        """Muestra la ayuda con todos los comandos disponibles."""
        help_text = """
COMANDOS DISPONIBLES:

JUEGO:
  new [jugador1] [jugador2]  - Inicia una nueva partida
  roll                       - Tira los dados
  move <desde> <hasta>       - Realiza un movimiento
                              (usa 'bar' para barra, 'off' para sacar)
  
INFORMACIÓN:
  board                      - Muestra el tablero actual
  moves                      - Muestra movimientos válidos
  status                     - Muestra estado del juego

SISTEMA:
  help                       - Muestra esta ayuda
  quit/exit                  - Sale del juego

EJEMPLOS:
  move 24 18                 - Mueve ficha del punto 24 al 18
  move bar 6                 - Entra desde la barra al punto 6
  move 3 off                 - Saca ficha del punto 3

NOTAS:
- Los puntos van del 0 al 23
- 'bar' representa la barra (fichas capturadas)
- 'off' representa sacar fichas del tablero
"""
        print(help_text)
    
    def _new_game(self, args: List[str]) -> None:
        """Inicia una nueva partida."""
        player1_name = args[0] if len(args) > 0 else None
        player2_name = args[1] if len(args) > 1 else None
        
        self.__game__ = BackgammonGame(player1_name, player2_name)
        
        print("=" * 50)
        print("NUEVA PARTIDA INICIADA")
        print("=" * 50)
        print(f"Jugador 1: {self.__game__.get_player_by_id(1).name}")
        print(f"Jugador 2: {self.__game__.get_player_by_id(2).name}")
        print("")
        
        # Iniciar el juego
        self.__game__.start_game()
        
        self._show_board([])
        print(f"\nEs el turno de {self.__game__.get_current_player().name}")
        print("Escribe 'roll' para tirar los dados")
    
    def _roll_dice(self, args: List[str]) -> None:
        """Tira los dados para el turno actual."""
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        try:
            dice1, dice2 = self.__game__.roll_dice()
            current_player = self.__game__.get_current_player()
            
            print(f"{current_player.name} tiró: {dice1}, {dice2}")
            
            if dice1 == dice2:
                print(f"¡Dobles! Puedes usar el {dice1} cuatro veces.")
            
            available_moves = self.__game__.dice.available_moves
            print(f"Valores disponibles: {available_moves}")
            
            # Mostrar movimientos válidos automáticamente
            valid_moves = self.__game__.get_valid_moves()
            if valid_moves:
                print(f"\nTienes {len(valid_moves)} movimientos válidos")
                print("Escribe 'moves' para verlos todos")
            else:
                print("\n¡No hay movimientos válidos disponibles!")
                print("El turno pasa automáticamente al siguiente jugador.")
                self.__game__.end_turn()
                next_player = self.__game__.get_current_player()
                print(f"\nAhora es el turno de {next_player.name}")
                print("Escribe 'roll' para tirar los dados")
        
        except GameNotStartedException:
            print("El juego no ha comenzado. Usa 'new' para crear una partida.")
        except InvalidMoveException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error al tirar dados: {e}")
    
    def _make_move(self, args: List[str]) -> None:
        """Realiza un movimiento."""
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        if len(args) != 2:
            print("Uso: move <desde> <hasta>")
            print("Ejemplo: move 24 18, move bar 6, move 3 off")
            return
        
        try:
            # Parsear puntos de origen y destino
            from_point = self._parse_point(args[0])
            to_point = self._parse_point(args[1])
            
            # Realizar el movimiento
            success = self.__game__.make_move(from_point, to_point)
            
            if success:
                print(f"✓ Movimiento realizado: {args[0]} → {args[1]}")
                
                # Mostrar tablero
                self._show_board([])
                
                # Verificar si el juego terminó
                if self.__game__.state == GameState.FINISHED:
                    winner = self.__game__.winner
                    print(f"\n🎉 ¡{winner.name} ha ganado el juego! 🎉")
                    print(f"Turnos jugados: {self.__game__.turn_count}")
                    return
                
                # Verificar si quedan movimientos
                if not self.__game__.dice.has_available_moves():
                    self.__game__.end_turn()
                    next_player = self.__game__.get_current_player()
                    print(f"\nTurno terminado. Ahora juega {next_player.name}")
                    print("Escribe 'roll' para tirar los dados")
                else:
                    available = self.__game__.dice.available_moves
                    print(f"\nValores de dados disponibles: {available}")
                    
                    valid_moves = self.__game__.get_valid_moves()
                    if not valid_moves:
                        print("No hay más movimientos válidos. El turno termina.")
                        self.__game__.end_turn()
                        next_player = self.__game__.get_current_player()
                        print(f"Ahora juega {next_player.name}")
        
        except ValueError as e:
            print(f"Error en el formato: {e}")
        except BackgammonException as e:
            print(f"Movimiento inválido: {e}")
        except Exception as e:
            print(f"Error al realizar movimiento: {e}")
    
    def _parse_point(self, point_str: str) -> int:
        """Parsea una cadena de punto a número."""
        point_str = point_str.lower().strip()
        
        if point_str in ['bar', 'barra']:
            return -1
        elif point_str in ['off', 'sacar', 'out']:
            return -1
        else:
            try:
                point = int(point_str)
                if point < 0 or point > 23:
                    raise ValueError(f"El punto debe estar entre 0 y 23")
                return point
            except ValueError:
                raise ValueError(f"Formato de punto inválido: {point_str}")
    
    def _show_valid_moves(self, args: List[str]) -> None:
        """Muestra todos los movimientos válidos disponibles."""
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        if self.__game__.state != GameState.IN_PROGRESS:
            print("No hay movimientos válidos. El juego no está en progreso.")
            return
        
        valid_moves = self.__game__.get_valid_moves()
        
        if not valid_moves:
            print("No hay movimientos válidos disponibles.")
            return
        
        print("\nMOVIMIENTOS VÁLIDOS:")
        print("-" * 40)
        
        for i, (from_point, to_point) in enumerate(valid_moves, 1):
            from_str = "bar" if from_point == -1 else str(from_point)
            to_str = "off" if to_point == -1 else str(to_point)
            print(f"{i:2d}. move {from_str} {to_str}")
        
        print("-" * 40)
        print(f"Total: {len(valid_moves)} movimientos disponibles")
    
    def _show_board(self, args: List[str]) -> None:
        """Muestra el estado actual del tablero."""
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        print(str(self.__game__.board))
        
        # Mostrar información adicional
        if self.__game__.state == GameState.IN_PROGRESS:
            current_player = self.__game__.get_current_player()
            print(f"\nTurno actual: {current_player.name}")
            
            if self.__game__.dice.is_rolled():
                dice_values = self.__game__.dice.available_moves
                if dice_values:
                    print(f"Dados disponibles: {dice_values}")
            else:
                print("Debe tirar los dados (use 'roll')")
    
    def _show_status(self, args: List[str]) -> None:
        """Muestra el estado general del juego."""
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        status = self.__game__.get_game_status()
        
        print("\nESTADO DEL JUEGO:")
        print("=" * 40)
        print(f"Estado: {status['state']}")
        print(f"Turnos jugados: {status['turn_count']}")
        print(f"Turno actual: {status['current_player']}")
        
        if status['dice_rolled']:
            print(f"Dados: {status['dice_values']}")
            print(f"Movimientos disponibles: {status['available_moves']}")
        else:
            print("Debe tirar los dados")
        
        print("\nJUGADORES:")
        print("-" * 40)
        
        for player_id in [1, 2]:
            pdata = status[f'player{player_id}']
            print(f"{pdata['name']}:")
            print(f"  Fichas en barra: {pdata['on_bar']}")
            print(f"  Fichas sacadas: {pdata['borne_off']}/15")
        
        if status['winner']:
            print(f"\n🏆 GANADOR: {status['winner']}")
    
    def _quit_game(self, args: List[str]) -> None:
        """Sale del juego."""
        if self.__game__ and self.__game__.state == GameState.IN_PROGRESS:
            confirm = input("¿Estás seguro de que quieres salir? La partida se perderá (s/N): ")
            if confirm.lower() not in ['s', 'sí', 'si', 'y', 'yes']:
                print("Continuando el juego...")
                return
        
        print("¡Gracias por jugar Backgammon!")
        print("¡Hasta la próxima!")
        self.__running__ = False


def main():
    """
    Función principal para ejecutar la interfaz CLI.
    """
    try:
        cli = CLIInterface()
        cli.run()
    except Exception as e:
        print(f"Error fatal en la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()