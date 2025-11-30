"""
Servicio de Plantillas Jinja2
Renderiza mensajes de Discord usando plantillas
"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from src.config import SIMBOLO_MONEDA


class TemplateService:
    """Servicio para renderizar plantillas Jinja2"""

    def __init__(self):
        """Inicializa el entorno Jinja2"""
        templates_dir = Path(__file__).parent.parent / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render_gastos_recientes(self, gastos, dias=30):
        """Renderiza plantilla de gastos recientes"""
        template = self.env.get_template('gastos_recientes.txt')
        return template.render(
            gastos=gastos,
            dias=dias,
            simbolo_moneda=SIMBOLO_MONEDA
        )

    def render_resumen_total(self, total, cantidad, promedio, dias=30):
        """Renderiza plantilla de resumen total"""
        template = self.env.get_template('resumen_total.txt')
        return template.render(
            total=total,
            cantidad=cantidad,
            promedio=promedio,
            dias=dias,
            simbolo_moneda=SIMBOLO_MONEDA
        )

    def render_gastos_categorias(self, categorias, dias=30):
        """Renderiza plantilla de gastos por categoría"""
        template = self.env.get_template('gastos_categorias.txt')
        total_general = sum(cat[1] for cat in categorias)
        return template.render(
            categorias=categorias,
            dias=dias,
            total_general=total_general,
            simbolo_moneda=SIMBOLO_MONEDA
        )


# Instancia global del servicio
template_service = TemplateService()

