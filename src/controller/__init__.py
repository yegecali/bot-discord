"""
Módulo Controller
Controladores para manejar lógica de presentación
"""
from .comando_controller import ComandoController, registrar_comandos_en_controller
from .evento_controller import EventoController, registrar_eventos_en_controller

__all__ = ['ComandoController', 'EventoController', 'registrar_comandos_en_controller', 'registrar_eventos_en_controller']

