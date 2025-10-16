

import sys
from typing import List, Tuple, Optional
from ..core.game import BackgammonGame, GameState, MoveType
from ..core import (
    Exception, InvalidMoveException, 
    GameNotStartedException, GameAlreadyFinishedException
)


class CLIInterface:
 
    
    def __init__(self):
       
        self.__game__ = None
        self.__running__ = False
        
        
        self.__commands__ = {
            'help': self._show_help,
            'new': self._new_game,
            'roll': self._roll_dice,
            'move': self._make_move,
            'moves': self._show_valid_moves,
            'board': self._show_board,
            'status': self._show_status,
            'history': self._show_history,
            'stats': self._show_stats,
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
        """
        Muestra la ayuda con todos los comandos disponibles.
        
        Args:
            args (List[str]): Argumentos del comando (no usados)
        """
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
  stats                      - Muestra estadísticas detalladas
  history                    - Muestra historial de movimientos

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
        """
        Inicia una nueva partida.
        
        Args:
            args (List[str]): [nombre_jugador1, nombre_jugador2] (opcional)
        """
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
        
        # Tirar dados para determinar orden
        print("Tirando dados para determinar el orden de juego...")
        while True:
            dice1, dice2, starter = self.__game__.roll_dice_for_turn_order()
            print(f"Jugador 1: {dice1}, Jugador 2: {dice2}")
            
            if starter != 0:
                starter_name = self.__game__.get_player_by_id(starter).name
                print(f"{starter_name} comienza el juego!")
                break
            else:
                print("Empate! Tirando de nuevo...")
        
        print("")
        self._show_board([])
        print(f"\nEs el turno de {self.__game__.get_current_player().name}")
        print("Escribe 'roll' para tirar los dados")
    
    def _roll_dice(self, args: List[str]) -> None:
        """
        Tira los dados para el turno actual.
        
        Args:
            args (List[str]): Argumentos (no usados)
        """
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        try:
            dice1, dice2 = self.__game__.roll_dice()
            current_player = self.__game__.get_current_player()
            
            print(f"{current_player.name} tiró: {dice1}, {dice2}")
            
            if dice1 == dice2:
                print(f"¡Dobles! Puedes usar el {dice1} cuatro veces.")
            
            available_moves = self.__game__.get_available_dice_values()
            print(f"Valores disponibles: {available_moves}")
            
            # Mostrar movimientos válidos automáticamente
            self._show_valid_moves([])
            
            # Verificar si no hay movimientos válidos
            if not self.__game__.has_valid_moves():
                print("\n¡No hay movimientos válidos disponibles!")
                print("El turno pasa automáticamente al siguiente jugador.")
                self.__game__.end_turn()
                next_player = self.__game__.get_current_player()
                print(f"\nAhora es el turno de {next_player.name}")
                print("Escribe 'roll' para tirar los dados")
        
        except GameNotStartedException:
            print("El juego no ha comenzado. Usa 'new' para crear una partida.")
        except GameAlreadyFinishedException:
            print("El juego ya ha terminado.")
        except InvalidMoveException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error al tirar dados: {e}")
    
    def _make_move(self, args: List[str]) -> None:
        """
        Realiza un movimiento.
        
        Args:
            args (List[str]): [punto_origen, punto_destino]
        """
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
            move_info = self.__game__.make_move(from_point, to_point)
            
            # Mostrar información del movimiento
            self._display_move_info(move_info)
            
            # Verificar si el juego terminó
            if self.__game__.state == GameState.FINISHED:
                winner = self.__game__.winner
                print(f"\n🎉 ¡{winner.name} ha ganado el juego! 🎉")
                self._show_stats([])
                return
            
            # Verificar si quedan movimientos
            if not self.__game__.get_available_dice_values():
                # No quedan dados, terminar turno
                self.__game__.end_turn()
                next_player = self.__game__.get_current_player()
                print(f"\nTurno terminado. Ahora juega {next_player.name}")
                print("Escribe 'roll' para tirar los dados")
            else:
                # Quedan dados disponibles
                available = self.__game__.get_available_dice_values()
                print(f"\nValores de dados disponibles: {available}")
                
                if self.__game__.has_valid_moves():
                    print("Puedes hacer más movimientos.")
                else:
                    print("No hay más movimientos válidos. El turno termina.")
                    self.__game__.end_turn()
                    next_player = self.__game__.get_current_player()
                    print(f"Ahora juega {next_player.name}")
                    print("Escribe 'roll' para tirar los dados")
        
        except GameNotStartedException:
            print("El juego no ha comenzado. Usa 'new' para crear una partida.")
        except GameAlreadyFinishedException:
            print("El juego ya ha terminado.")
        except InvalidMoveException as e:
            print(f"Movimiento inválido: {e}")
        except ValueError as e:
            print(f"Error en el formato: {e}")
        except Exception as e:
            print(f"Error al realizar movimiento: {e}")
    
    def _parse_point(self, point_str: str) -> int:
        """
        Parsea una cadena de punto a número.
        
        Args:
            point_str (str): Cadena del punto ("0"-"23", "bar", "off")
        
        Returns:
            int: Número del punto (-1 para barra/off según contexto)
        
        Raises:
            ValueError: Si el formato es inválido
        """
        point_str = point_str.lower().strip()
        
        if point_str in ['bar', 'barra']:
            return -1
        elif point_str in ['off', 'sacar', 'out']:
            return -1
        else:
            try:
                point = int(point_str)
                if point < 0 or point > 23:
                    raise ValueError(f"El punto debe estar entre 0 y 23, recibido: {point}")
                return point
            except ValueError:
                raise ValueError(f"Formato de punto inválido: {point_str}")
    
    def _display_move_info(self, move_info: dict) -> None:
        """
        Muestra información sobre un movimiento realizado.
        
        Args:
            move_info (dict): Información del movimiento
        """
        player_name = self.__game__.get_player_by_id(move_info['player_id']).name
        from_str = self._point_to_string(move_info['from_point'])
        to_str = self._point_to_string(move_info['to_point'])
        
        print(f"\n{player_name} movió de {from_str} a {to_str} (dado: {move_info['dice_value']})")
        
        if move_info['captured']:
            captured_player = self.__game__.get_player_by_id(move_info['captured_player']).name
            print(f"¡Ficha de {captured_player} capturada!")
        
        if move_info['move_type'] == MoveType.BEAR_OFF:
            print("Ficha sacada del tablero!")
        elif move_info['move_type'] == MoveType.ENTER_FROM_BAR:
            print("Ficha reingresada desde la barra!")
    
    def _point_to_string(self, point: int) -> str:
        """
        Convierte un número de punto a cadena descriptiva.
        
        Args:
            point (int): Número del punto (-1, 0-23)
        
        Returns:
            str: Cadena descriptiva
        """
        if point == -1:
            return "barra/off"
        else:
            return str(point)
    
    def _show_valid_moves(self, args: List[str]) -> None:
        """
        Muestra todos los movimientos válidos disponibles.
        
        Args:
            args (List[str]): Argumentos (no usados)
        """
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
        
        for i, (from_point, to_point, move_type) in enumerate(valid_moves, 1):
            from_str = "barra" if from_point == -1 else str(from_point)
            to_str = "sacar" if to_point == -1 else str(to_point)
            
            type_str = ""
            if move_type == MoveType.ENTER_FROM_BAR:
                type_str = " (desde barra)"
            elif move_type == MoveType.BEAR_OFF:
                type_str = " (sacar)"
            
            print(f"{i:2d}. move {from_str} {to_str}{type_str}")
        
        print("-" * 40)
        print(f"Total: {len(valid_moves)} movimientos disponibles")
    
    def _show_board(self, args: List[str]) -> None:
        """
        Muestra el estado actual del tablero.
        
        Args:
            args (List[str]): Argumentos (no usados)
        """
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        print(str(self.__game__.board))
        
        # Mostrar información adicional del turno actual
        if self.__game__.state == GameState.IN_PROGRESS:
            current_player = self.__game__.get_current_player()
            dice_values = self.__game__.get_available_dice_values()
            
            print(f"\nTurno actual: {current_player.name}")
            if dice_values:
                print(f"Dados disponibles: {dice_values}")
            else:
                print("Debe tirar los dados (use 'roll')")
    
    def _show_status(self, args: List[str]) -> None:
        """
        Muestra el estado general del juego.
        
        Args:
            args (List[str]): Argumentos (no usados)
        """
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        stats = self.__game__.get_game_statistics()
        
        print("\nESTADO DEL JUEGO:")
        print("=" * 40)
        print(f"Estado: {stats['state']}")
        print(f"Turnos jugados: {stats['turn_count']}")
        print(f"Movimientos totales: {stats['total_moves']}")
        
        if stats['winner_id']:
            winner_name = self.__game__.get_player_by_id(stats['winner_id']).name
            print(f"Ganador: {winner_name}")
        
        print("\nJUGADORES:")
        print("-" * 40)
        
        for player_id in [1, 2]:
            player_data = stats['players'][f'player{player_id}']
            current_mark = " <- TURNO ACTUAL" if stats['current_player_id'] == player_id else ""
            
            print(f"Jugador {player_id}: {player_data['name']}{current_mark}")
            print(f"  Fichas en juego: {player_data['checkers_in_play']}")
            print(f"  Fichas en barra: {player_data['checkers_on_bar']}")
            print(f"  Fichas sacadas: {player_data['checkers_borne_off']}")
            print(f"  Pip count: {player_data['pip_count']}")
            print(f"  Puede sacar: {'Sí' if player_data['can_bear_off'] else 'No'}")
            print()
        
        # Información de dados
        dice_info = stats['dice']
        if dice_info['is_rolled']:
            print("DADOS:")
            print("-" * 40)
            print(f"Valores: {dice_info['values'][0]}, {dice_info['values'][1]}")
            if dice_info['is_double']:
                print("¡DOBLES!")
            print(f"Disponibles: {dice_info['available_moves']}")
            print(f"Usados: {dice_info['used_moves']}")
    
    def _show_history(self, args: List[str]) -> None:
        """
        Muestra el historial de movimientos.
        
        Args:
            args (List[str]): Argumentos opcionales [número_de_movimientos]
        """
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        history = self.__game__.get_move_history()
        
        if not history:
            print("No hay movimientos en el historial.")
            return
        
        # Determinar cuántos movimientos mostrar
        show_count = len(history)
        if args and args[0].isdigit():
            show_count = min(int(args[0]), len(history))
        
        print(f"\nHISTORIAL DE MOVIMIENTOS (últimos {show_count}):")
        print("=" * 60)
        
        recent_moves = history[-show_count:]
        
        for i, move in enumerate(recent_moves, 1):
            player_name = self.__game__.get_player_by_id(move['player_id']).name
            from_str = "barra" if move['from_point'] == -1 else str(move['from_point'])
            to_str = "sacar" if move['to_point'] == -1 else str(move['to_point'])
            
            move_desc = f"{i:2d}. {player_name}: {from_str} → {to_str} (dado: {move['dice_value']})"
            
            if move['captured']:
                move_desc += " ¡CAPTURA!"
            
            if move.get('move_type') == MoveType.BEAR_OFF:
                move_desc += " [SACAR]"
            elif move.get('move_type') == MoveType.ENTER_FROM_BAR:
                move_desc += " [BARRA]"
            
            print(move_desc)
        
        print(f"\nTotal de movimientos: {len(history)}")
    
    def _show_stats(self, args: List[str]) -> None:
        """
        Muestra estadísticas detalladas del juego.
        
        Args:
            args (List[str]): Argumentos (no usados)
        """
        if not self.__game__:
            print("No hay partida activa. Usa 'new' para crear una.")
            return
        
        stats = self.__game__.get_game_statistics()
        race_status = self.__game__.get_race_status()
        
        print("\nESTADÍSTICAS DETALLADAS:")
        print("=" * 50)
        
        # Información general
        print("INFORMACIÓN GENERAL:")
        print(f"  Estado del juego: {stats['state']}")
        print(f"  Turnos completados: {stats['turn_count']}")
        print(f"  Movimientos totales: {stats['total_moves']}")
        print(f"  Promedio mov/turno: {stats['total_moves']/max(1,stats['turn_count']):.1f}")
        print()
        
        # Estado de la carrera
        print("ESTADO DE LA CARRERA:")
        print(f"  Es una carrera pura: {'Sí' if race_status['is_race'] else 'No'}")
        if race_status['leader']:
            leader_name = self.__game__.get_player_by_id(race_status['leader']).name
            print(f"  Líder actual: {leader_name}")
            print(f"  Diferencia pip count: {abs(race_status['difference'])}")
        else:
            print(f"  Empate en pip count")
        print()
        
        # Estadísticas por jugador
        for player_id in [1, 2]:
            player_data = stats['players'][f'player{player_id}']
            print(f"JUGADOR {player_id} ({player_data['name']}):")
            print(f"  Fichas en tablero: {player_data['checkers_in_play']}")
            print(f"  Fichas en barra: {player_data['checkers_on_bar']}")
            print(f"  Fichas sacadas: {player_data['checkers_borne_off']}")
            print(f"  Progreso: {player_data['checkers_borne_off']}/15 ({100*player_data['checkers_borne_off']/15:.1f}%)")
            print(f"  Pip count: {player_data['pip_count']}")
            print(f"  Puede sacar fichas: {'Sí' if player_data['can_bear_off'] else 'No'}")
            print()
        
        # Análisis del tablero
        board_rep = stats['board']
        print("ANÁLISIS DEL TABLERO:")
        
        # Contar puntos controlados por cada jugador
        points_p1 = sum(1 for point_data in board_rep['points'].values() 
                        if point_data['player_id'] == 1 and point_data['count'] >= 2)
        points_p2 = sum(1 for point_data in board_rep['points'].values() 
                        if point_data['player_id'] == 2 and point_data['count'] >= 2)
        
        print(f"  Puntos controlados P1: {points_p1}")
        print(f"  Puntos controlados P2: {points_p2}")
        
        # Verificar bloqueos largos
        p1_longest = self.__game__.board.get_longest_blocked_sequence(1)
        p2_longest = self.__game__.board.get_longest_blocked_sequence(2)
        
        print(f"  Secuencia más larga P1: {p1_longest} puntos")
        print(f"  Secuencia más larga P2: {p2_longest} puntos")
        
        if self.__game__.state == GameState.FINISHED:
            winner_name = self.__game__.winner.name
            print(f"\n🏆 GANADOR: {winner_name} 🏆")
    
    def _quit_game(self, args: List[str]) -> None:
        """
        Sale del juego.
        
        Args:
            args (List[str]): Argumentos (no usados)
        """
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