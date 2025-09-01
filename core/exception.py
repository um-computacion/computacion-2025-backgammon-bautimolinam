"""
Excepciones personalizadas para el juego de Backgammon.

Este módulo define las excepciones específicas del dominio del juego,
siguiendo el principio de responsabilidad única y facilitando el manejo
de errores específicos del Backgammon.
"""


class BackgammonException(Exception):
    """Excepción base para todos los errores del juego de Backgammon."""
    
    def __init__(self, message: str):
        """
        Inicializa la excepción base.
        
        Args:
            message (str): Mensaje descriptivo del error
        """
        self.__message__ = message
        super().__init__(self.__message__)


class InvalidMoveException(BackgammonException):
    """Excepción lanzada cuando se intenta realizar un movimiento inválido."""
    
    def __init__(self, from_point: int, to_point: int, reason: str = "Movimiento inválido"):
        """
        Inicializa la excepción de movimiento inválido.
        
        Args:
            from_point (int): Punto de origen del movimiento
            to_point (int): Punto de destino del movimiento
            reason (str): Razón específica por la cual el movimiento es inválido
        """
        self.__from_point__ = from_point
        self.__to_point__ = to_point
        self.__reason__ = reason
        message = f"Movimiento inválido de {from_point} a {to_point}: {reason}"
        super().__init__(message)


class GameNotStartedException(BackgammonException):
    """Excepción lanzada cuando se intenta realizar una acción en un juego no iniciado."""
    
    def __init__(self):
        """Inicializa la excepción de juego no iniciado."""
        super().__init__("El juego no ha sido iniciado")


class GameAlreadyFinishedException(BackgammonException):
    """Excepción lanzada cuando se intenta realizar una acción en un juego ya terminado."""
    
    def __init__(self):
        """Inicializa la excepción de juego ya terminado."""
        super().__init__("El juego ya ha terminado")


class InvalidPlayerException(BackgammonException):
    """Excepción lanzada cuando se intenta acceder a un jugador inválido."""
    
    def __init__(self, player_id: int):
        """
        Inicializa la excepción de jugador inválido.
        
        Args:
            player_id (int): ID del jugador inválido
        """
        self.__player_id__ = player_id
        super().__init__(f"Jugador inválido: {player_id}")


class InvalidDiceValueException(BackgammonException):
    """Excepción lanzada cuando se obtiene un valor de dado inválido."""
    
    def __init__(self, dice_value: int):
        """
        Inicializa la excepción de valor de dado inválido.
        
        Args:
            dice_value (int): Valor del dado inválido
        """
        self.__dice_value__ = dice_value
        super().__init__(f"Valor de dado inválido: {dice_value}")


class NoMovesAvailableException(BackgammonException):
    """Excepción lanzada cuando no hay movimientos disponibles para un jugador."""
    
    def __init__(self, player_id: int):
        """
        Inicializa la excepción de no hay movimientos disponibles.
        
        Args:
            player_id (int): ID del jugador sin movimientos disponibles
        """
        self.__player_id__ = player_id
        super().__init__(f"No hay movimientos disponibles para el jugador {player_id}")


class InvalidPointException(BackgammonException):
    """Excepción lanzada cuando se intenta acceder a un punto inválido del tablero."""
    
    def __init__(self, point: int):
        """
        Inicializa la excepción de punto inválido.
        
        Args:
            point (int): Número de punto inválido
        """
        self.__point__ = point
        super().__init__(f"Punto de tablero inválido: {point}")


class CheckerNotAvailableException(BackgammonException):
    """Excepción lanzada cuando se intenta mover una ficha que no está disponible."""
    
    def __init__(self, point: int, player_id: int):
        """
        Inicializa la excepción de ficha no disponible.
        
        Args:
            point (int): Punto donde se intentó acceder a la ficha
            player_id (int): ID del jugador propietario esperado
        """
        self.__point__ = point
        self.__player_id__ = player_id
        super().__init__(f"No hay fichas del jugador {player_id} disponibles en el punto {point}")


class CannotBearOffException(BackgammonException):
    """Excepción lanzada cuando se intenta sacar fichas sin cumplir las condiciones."""
    
    def __init__(self, player_id: int, reason: str = "No se puede sacar fichas"):
        """
        Inicializa la excepción de no se puede sacar fichas.
        
        Args:
            player_id (int): ID del jugador que intenta sacar fichas
            reason (str): Razón específica por la cual no se puede sacar
        """
        self.__player_id__ = player_id
        self.__reason__ = reason
        super().__init__(f"El jugador {player_id} no puede sacar fichas: {reason}")