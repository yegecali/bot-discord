"""
Configuración de OCR
Carga palabras clave desde JSON externo
"""
import json
from pathlib import Path


class OCRConfig:
    """Carga y gestiona la configuración de OCR"""

    def __init__(self):
        """Inicializa la configuración desde JSON"""
        self.config_path = Path(__file__).parent / 'ocr_keywords.json'
        self.config = self._cargar_config()

    def _cargar_config(self):
        """Carga la configuración desde JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"[OCR_CONFIG] Configuración cargada desde: {self.config_path}")
                return config.get('ocr', {})
        except FileNotFoundError:
            print(f"[OCR_CONFIG] [WARN] Archivo no encontrado: {self.config_path}")
            print(f"[OCR_CONFIG] Usando configuración por defecto")
            return self._config_por_defecto()
        except json.JSONDecodeError as e:
            print(f"[OCR_CONFIG] [ERROR] Error parseando JSON: {e}")
            return self._config_por_defecto()

    @staticmethod
    def _config_por_defecto():
        """Retorna configuración por defecto"""
        return {
            'palabras_total': [
                'total', 'monto', 'a pagar', 'importe', 'debe', 'pago', 'subtotal'
            ],
            'palabras_vendedor': [
                'comercio', 'tienda', 'empresa', 'establecimiento', 'vendedor'
            ],
            'palabras_fecha': [
                'fecha', 'día', 'emisión', 'expedición'
            ]
        }

    def get_palabras_total(self):
        """Obtiene palabras clave para detectar el total"""
        return self.config.get('palabras_total', self._config_por_defecto()['palabras_total'])

    def get_palabras_vendedor(self):
        """Obtiene palabras clave para detectar el vendedor"""
        return self.config.get('palabras_vendedor', self._config_por_defecto()['palabras_vendedor'])

    def get_palabras_fecha(self):
        """Obtiene palabras clave para detectar la fecha"""
        return self.config.get('palabras_fecha', self._config_por_defecto()['palabras_fecha'])

    def agregar_palabra_total(self, palabra):
        """Agrega una palabra clave para total"""
        palabras = self.get_palabras_total()
        if palabra not in palabras:
            palabras.append(palabra)
            self._guardar_config()
            print(f"[OCR_CONFIG] Palabra agregada: '{palabra}'")

    def _guardar_config(self):
        """Guarda la configuración actualizada en JSON"""
        try:
            config_completa = {'ocr': self.config}
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_completa, f, indent=2, ensure_ascii=False)
                print(f"[OCR_CONFIG] Configuración guardada")
        except Exception as e:
            print(f"[OCR_CONFIG] [ERROR] Error guardando config: {e}")


# Instancia global
ocr_config = OCRConfig()

