"""
Interfaz gráfica con Pygame para Backgammon - 
"""

import pygame
import sys
from typing import Optional, Tuple, List

from core.game import BackgammonGame, GameState
from core.exception import BackgammonException

# Colores estilo terminal/CLI
COLOR_FONDO = (20, 20, 30)           # Azul oscuro tipo terminal
COLOR_TABLERO = (40, 35, 30)         # Marrón oscuro
COLOR_PUNTO_1 = (180, 140, 100)      # Marrón claro
COLOR_PUNTO_2 = (80, 60, 40)         # Marrón oscuro
COLOR_FICHA_P1 = (255, 255, 255)     # Blanco
COLOR_FICHA_P2 = (30, 30, 30)        # Negro
COLOR_BORDE = (200, 200, 200)        # Gris claro
COLOR_TEXTO = (0, 255, 0)            # Verde terminal
COLOR_TITULO = (255, 255, 0)         # Amarillo
COLOR_ERROR = (255, 0, 0)            # Rojo
COLOR_SELECCION = (255, 215, 0)      # Dorado
COLOR_PANEL = (25, 25, 40)           # Azul muy oscuro

# Dimensiones
ANCHO = 1400
ALTO = 900
MARGEN = 30
ANCHO_TABLERO = 900
ALTO_TABLERO = 700
ANCHO_PANEL = 400
ANCHO_PUNTO = 65
ALTO_PUNTO = 280
RADIO_FICHA = 28


class PygameInterface:
    """Interfaz gráfica estilo CLI/Terminal para Backgammon."""
    
    def __init__(self):
        pygame.init()
        self.__screen__ = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Backgammon - Computación 2025")
        self.__clock__ = pygame.time.Clock()
        
        # Fuentes estilo terminal
        self.__font_titulo__ = pygame.font.Font(None, 42)
        self.__font_grande__ = pygame.font.Font(None, 32)
        self.__font_normal__ = pygame.font.Font(None, 26)
        self.__font_pequena__ = pygame.font.Font(None, 22)
        
        # Estado
        self.__game__ = None
        self.__running__ = True
        self.__selected__ = None
        self.__valid_moves__ = []
        self.__mensaje__ = "Escribe 'N' para nueva partida"
        self.__mensaje_tipo__ = "info"  # info, error, success
        self.__log__ = []  # Log de movimientos estilo CLI
    
    def run(self) -> None:
        """Loop principal."""
        while self.__running__:
            self._handle_events()
            self._draw()
            self.__clock__.tick(60)
        
        pygame.quit()
    
    def _handle_events(self) -> None:
        """Maneja eventos."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running__ = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_click(event.pos)
    
    def _handle_key(self, key: int) -> None:
        """Maneja teclas."""
        if key == pygame.K_ESCAPE or key == pygame.K_q:
            self.__running__ = False
        
        elif key == pygame.K_n:
            self._nueva_partida()
        
        elif key == pygame.K_r:
            self._tirar_dados()
        
        elif key == pygame.K_m:
            self._mostrar_movimientos()
        
        elif key == pygame.K_s:
            self._mostrar_status()
        
        elif key == pygame.K_SPACE:
            self._end_turn()
    
    def _nueva_partida(self) -> None:
        """Inicia nueva partida."""
        self.__game__ = BackgammonGame("Jugador 1", "Jugador 2")
        self.__game__.start_game()
        self.__selected__ = None
        self.__valid_moves__ = []
        self.__log__ = []
        self._add_log(">>> Nueva partida iniciada")
        self._add_log(f">>> {self.__game__.get_current_player().name} vs {self.__game__.get_player_by_id(2).name}")
        self._set_mensaje("Nueva partida iniciada. Presiona 'R' para tirar dados", "success")
    
    def _tirar_dados(self) -> None:
        """Tira los dados."""
        if not self.__game__:
            self._set_mensaje("Error: Primero inicia una partida con 'N'", "error")
            return
        
        if self.__game__.state != GameState.IN_PROGRESS:
            self._set_mensaje("Error: El juego no está en progreso", "error")
            return
        
        try:
            d1, d2 = self.__game__.roll_dice()
            self.__selected__ = None
            self.__valid_moves__ = []
            
            player = self.__game__.get_current_player().name
            msg = f"{player} tiró: [{d1}] [{d2}]"
            if d1 == d2:
                msg += " ¡DOBLES!"
            
            self._add_log(f">>> {msg}")
            self._set_mensaje(msg, "info")
            
            # Verificar si hay movimientos válidos
            valid = self.__game__.get_valid_moves()
            if not valid:
                self._add_log(">>> No hay movimientos válidos")
                self._set_mensaje("No hay movimientos válidos. Pasando turno...", "error")
                pygame.time.wait(1000)
                self.__game__.end_turn()
                self._add_log(f">>> Turno de {self.__game__.get_current_player().name}")
            else:
                self._add_log(f">>> {len(valid)} movimientos disponibles")
        
        except BackgammonException as e:
            self._set_mensaje(f"Error: {e}", "error")
    
    def _mostrar_movimientos(self) -> None:
        """Muestra movimientos válidos."""
        if not self.__game__ or not self.__game__.dice.is_rolled():
            self._set_mensaje("Primero tira los dados con 'R'", "error")
            return
        
        moves = self.__game__.get_valid_moves()
        self._add_log(f">>> Movimientos válidos: {len(moves)}")
        for i, (f, t) in enumerate(moves[:5], 1):
            from_str = "bar" if f == -1 else f
            to_str = "off" if t == -1 else t
            self._add_log(f"    {i}. {from_str} → {to_str}")
        
        if len(moves) > 5:
            self._add_log(f"    ... y {len(moves)-5} más")
    
    def _mostrar_status(self) -> None:
        """Muestra status del juego."""
        if not self.__game__:
            return
        
        status = self.__game__.get_game_status()
        self._add_log(">>> === STATUS ===")
        self._add_log(f">>> Turno: {status['current_player']}")
        self._add_log(f">>> Turnos jugados: {status['turn_count']}")
        
        for pid in [1, 2]:
            p = status[f'player{pid}']
            self._add_log(f">>> {p['name']}: {p['borne_off']}/15 sacadas")
    
    def _end_turn(self) -> None:
        """Termina el turno."""
        if not self.__game__:
            return
        
        try:
            self.__game__.end_turn()
            self._add_log(f">>> Turno terminado")
            self._add_log(f">>> Turno de {self.__game__.get_current_player().name}")
            self._set_mensaje(f"Turno de {self.__game__.get_current_player().name}", "info")
            self.__selected__ = None
            self.__valid_moves__ = []
        except BackgammonException as e:
            self._set_mensaje(f"Error: {e}", "error")
    
    def _handle_click(self, pos: Tuple[int, int]) -> None:
        """Maneja clicks del mouse."""
        if not self.__game__ or self.__game__.state != GameState.IN_PROGRESS:
            return
        
        punto = self._get_punto(pos)
        if punto is None:
            return
        
        if self.__selected__ is None:
            # Seleccionar origen
            if self._es_origen_valido(punto):
                self.__selected__ = punto
                self.__valid_moves__ = self._get_destinos_validos(punto)
                self._set_mensaje(f"Punto {punto} seleccionado. Click en destino", "info")
                self._add_log(f">>> Seleccionado: punto {punto}")
        else:
            # Intentar mover
            try:
                from_pt = self.__selected__
                to_pt = punto
                
                self.__game__.make_move(from_pt, to_pt)
                
                from_str = "bar" if from_pt == -1 else from_pt
                to_str = "off" if to_pt == -1 else to_pt
                
                self._add_log(f">>> move {from_str} {to_str}")
                self._set_mensaje(f"✓ Movimiento: {from_str} → {to_str}", "success")
                
                self.__selected__ = None
                self.__valid_moves__ = []
                
                # Verificar victoria
                if self.__game__.winner:
                    self._add_log(f">>> ¡¡¡ {self.__game__.winner.name} HA GANADO !!!")
                    self._set_mensaje(f"¡¡¡ {self.__game__.winner.name} GANA !!!", "success")
                
                # Verificar si debe cambiar turno
                elif not self.__game__.dice.has_available_moves():
                    valid = self.__game__.get_valid_moves()
                    if not valid:
                        self.__game__.end_turn()
                        self._add_log(f">>> Turno de {self.__game__.get_current_player().name}")
                        self._set_mensaje(f"Turno de {self.__game__.get_current_player().name}", "info")
            
            except BackgammonException as e:
                self._set_mensaje(f"Movimiento inválido: {e}", "error")
                self.__selected__ = None
                self.__valid_moves__ = []
    
    def _es_origen_valido(self, punto: int) -> bool:
        """Verifica si un punto es origen válido."""
        if not self.__game__.dice.is_rolled():
            self._set_mensaje("Primero tira los dados con 'R'", "error")
            return False
        
        checkers = self.__game__.board.get_point_checkers(punto)
        if not checkers:
            return False
        
        return checkers[0].player_id == self.__game__.get_current_player().player_id
    
    def _get_destinos_validos(self, from_point: int) -> List[int]:
        """Obtiene destinos válidos."""
        moves = self.__game__.get_valid_moves()
        return [t for f, t in moves if f == from_point]
    
    def _get_punto(self, pos: Tuple[int, int]) -> Optional[int]:
        """Convierte posición del mouse a número de punto."""
        x, y = pos
        x -= MARGEN
        y -= MARGEN
        
        if x < 0 or x > ANCHO_TABLERO or y < 0 or y > ALTO_TABLERO:
            return None
        
        superior = y < ALTO_TABLERO // 2
        idx = int(x / (ANCHO_TABLERO / 12))
        
        if idx < 0 or idx >= 12:
            return None
        
        if superior:
            return 12 + idx
        else:
            return 11 - idx
    
    def _set_mensaje(self, msg: str, tipo: str = "info") -> None:
        """Establece mensaje."""
        self.__mensaje__ = msg
        self.__mensaje_tipo__ = tipo
    
    def _add_log(self, msg: str) -> None:
        """Agrega entrada al log."""
        self.__log__.append(msg)
        if len(self.__log__) > 20:
            self.__log__.pop(0)
    
    def _draw(self) -> None:
        """Dibuja todo."""
        self.__screen__.fill(COLOR_FONDO)
        self._draw_tablero()
        
        if self.__game__:
            self._draw_fichas()
        
        self._draw_panel()
        pygame.display.flip()
    
    def _draw_tablero(self) -> None:
        """Dibuja el tablero."""
        # Fondo del tablero
        rect = pygame.Rect(MARGEN, MARGEN, ANCHO_TABLERO, ALTO_TABLERO)
        pygame.draw.rect(self.__screen__, COLOR_TABLERO, rect)
        pygame.draw.rect(self.__screen__, COLOR_BORDE, rect, 3)
        
        # Puntos triangulares
        for i in range(12):
            x = MARGEN + i * (ANCHO_TABLERO / 12)
            w = ANCHO_TABLERO / 12
            
            # Superior
            color = COLOR_PUNTO_1 if i % 2 == 0 else COLOR_PUNTO_2
            self._draw_triangulo(x, MARGEN, w, ALTO_PUNTO, color, False)
            
            # Número del punto (arriba)
            num = 12 + i
            color_num = COLOR_SELECCION if self.__selected__ == num else COLOR_TEXTO
            text = self.__font_pequena__.render(str(num), True, color_num)
            self.__screen__.blit(text, (x + w//2 - 10, MARGEN + ALTO_PUNTO + 5))
            
            # Inferior
            color = COLOR_PUNTO_2 if i % 2 == 0 else COLOR_PUNTO_1
            y = MARGEN + ALTO_TABLERO - ALTO_PUNTO
            self._draw_triangulo(x, y, w, ALTO_PUNTO, color, True)
            
            # Número del punto (abajo)
            num = 11 - i
            color_num = COLOR_SELECCION if self.__selected__ == num else COLOR_TEXTO
            text = self.__font_pequena__.render(str(num), True, color_num)
            self.__screen__.blit(text, (x + w//2 - 10, y - 25))
    
    def _draw_triangulo(self, x: float, y: float, ancho: float, 
                       alto: float, color: Tuple, arriba: bool) -> None:
        """Dibuja un triángulo."""
        if arriba:
            pts = [(x + ancho/2, y), (x, y + alto), (x + ancho, y + alto)]
        else:
            pts = [(x, y), (x + ancho, y), (x + ancho/2, y + alto)]
        
        pygame.draw.polygon(self.__screen__, color, pts)
        pygame.draw.polygon(self.__screen__, COLOR_BORDE, pts, 2)
    
    def _draw_fichas(self) -> None:
        """Dibuja las fichas."""
        for punto in range(24):
            checkers = self.__game__.board.get_point_checkers(punto)
            if not checkers:
                continue
            
            # Posición base
            if punto >= 12:
                x = MARGEN + (punto - 12) * (ANCHO_TABLERO / 12) + (ANCHO_TABLERO / 24)
                y = MARGEN + 35
                offset = 10
            else:
                x = MARGEN + (11 - punto) * (ANCHO_TABLERO / 12) + (ANCHO_TABLERO / 24)
                y = MARGEN + ALTO_TABLERO - 35
                offset = -10
            
            # Color de fichas
            color_ficha = COLOR_FICHA_P1 if checkers[0].player_id == 1 else COLOR_FICHA_P2
            color_borde = COLOR_FICHA_P2 if checkers[0].player_id == 1 else COLOR_FICHA_P1
            
            # Resaltar si es destino válido
            if punto in self.__valid_moves__:
                pygame.draw.circle(self.__screen__, COLOR_SELECCION, 
                                 (int(x), int(y)), RADIO_FICHA + 5, 3)
            
            # Dibujar fichas
            for i, checker in enumerate(checkers[:10]):
                pos_y = y + i * offset * 2.5
                pygame.draw.circle(self.__screen__, color_ficha, (int(x), int(pos_y)), RADIO_FICHA)
                pygame.draw.circle(self.__screen__, color_borde, (int(x), int(pos_y)), RADIO_FICHA, 2)
            
            # Número si hay muchas fichas
            if len(checkers) > 10:
                text = self.__font_pequena__.render(str(len(checkers)), True, COLOR_SELECCION)
                rect = text.get_rect(center=(int(x), int(pos_y)))
                self.__screen__.blit(text, rect)
    
    def _draw_panel(self) -> None:
        """Dibuja panel lateral estilo CLI."""
        x_panel = MARGEN + ANCHO_TABLERO + 20
        y = MARGEN
        
        # Fondo del panel
        panel_rect = pygame.Rect(x_panel - 10, MARGEN, ANCHO_PANEL, ALTO_TABLERO)
        pygame.draw.rect(self.__screen__, COLOR_PANEL, panel_rect)
        pygame.draw.rect(self.__screen__, COLOR_BORDE, panel_rect, 2)
        
        # Título
        text = self.__font_titulo__.render("BACKGAMMON", True, COLOR_TITULO)
        self.__screen__.blit(text, (x_panel, y))
        y += 50
        
        # Línea separadora
        pygame.draw.line(self.__screen__, COLOR_BORDE, 
                        (x_panel, y), (x_panel + ANCHO_PANEL - 30, y), 2)
        y += 20
        
        # Mensaje principal
        color_msg = COLOR_TEXTO
        if self.__mensaje_tipo__ == "error":
            color_msg = COLOR_ERROR
        elif self.__mensaje_tipo__ == "success":
            color_msg = COLOR_SELECCION
        
        # Mensaje en múltiples líneas si es largo
        palabras = self.__mensaje__.split()
        linea = ""
        for palabra in palabras:
            test = linea + palabra + " "
            if len(test) > 35:
                text = self.__font_normal__.render(linea, True, color_msg)
                self.__screen__.blit(text, (x_panel, y))
                y += 30
                linea = palabra + " "
            else:
                linea = test
        if linea:
            text = self.__font_normal__.render(linea, True, color_msg)
            self.__screen__.blit(text, (x_panel, y))
        
        y += 50
        
        # Info del juego
        if self.__game__:
            # Jugador actual
            player = self.__game__.get_current_player().name
            text = self.__font_normal__.render(f"> {player}", True, COLOR_TITULO)
            self.__screen__.blit(text, (x_panel, y))
            y += 35
            
            # Dados
            if self.__game__.dice.is_rolled():
                vals = self.__game__.dice.values
                avail = self.__game__.dice.available_moves
                text = self.__font_normal__.render(f"Dados: [{vals[0]}] [{vals[1]}]", True, COLOR_TEXTO)
                self.__screen__.blit(text, (x_panel, y))
                y += 30
                text = self.__font_pequena__.render(f"Disponibles: {avail}", True, COLOR_TEXTO)
                self.__screen__.blit(text, (x_panel, y))
                y += 40
        
        # Línea separadora
        pygame.draw.line(self.__screen__, COLOR_BORDE, 
                        (x_panel, y), (x_panel + ANCHO_PANEL - 30, y), 1)
        y += 15
        
        # Comandos estilo CLI
        text = self.__font_normal__.render("COMANDOS:", True, COLOR_TITULO)
        self.__screen__.blit(text, (x_panel, y))
        y += 35
        
        comandos = [
            "N - Nueva partida",
            "R - Roll dados",
            "M - Mostrar moves",
            "S - Status",
            "SPACE - End turn",
            "Q/ESC - Salir"
        ]
        
        for cmd in comandos:
            text = self.__font_pequena__.render(cmd, True, COLOR_TEXTO)
            self.__screen__.blit(text, (x_panel, y))
            y += 25
        
        y += 20
        
        # Log de movimientos (estilo terminal)
        pygame.draw.line(self.__screen__, COLOR_BORDE, 
                        (x_panel, y), (x_panel + ANCHO_PANEL - 30, y), 1)
        y += 10
        
        text = self.__font_normal__.render("LOG:", True, COLOR_TITULO)
        self.__screen__.blit(text, (x_panel, y))
        y += 30
        
        # Mostrar últimas 8 líneas del log
        for log_entry in self.__log__[-8:]:
            # Truncar si es muy largo
            if len(log_entry) > 40:
                log_entry = log_entry[:37] + "..."
            
            text = self.__font_pequena__.render(log_entry, True, COLOR_TEXTO)
            self.__screen__.blit(text, (x_panel, y))
            y += 22


def main():
    """Función principal."""
    try:
        interface = PygameInterface()
        interface.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()