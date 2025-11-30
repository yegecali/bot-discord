"""
Servicio de Plantillas Jinja2
Renderiza mensajes de Discord usando plantillas
"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from datetime import datetime
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

        # Agregar filtros personalizados
        self._add_custom_filters()

    def _add_custom_filters(self):
        """Agrega filtros personalizados a Jinja2"""

        def strftime_filter(dt_obj, fmt='%d/%m/%Y %H:%M'):
            """Filtro para formatear fechas"""
            if isinstance(dt_obj, str):
                # Si es string "now", usar datetime actual
                if dt_obj == 'now':
                    return datetime.now().strftime(fmt)
                # Si es una fecha string, intentar parsearla
                try:
                    dt_obj = datetime.fromisoformat(dt_obj)
                except:
                    return str(dt_obj)

            if isinstance(dt_obj, datetime):
                return dt_obj.strftime(fmt)

            return str(dt_obj)

        def format_money(value, decimals=2):
            """Filtro para formatear dinero"""
            try:
                return f"{float(value):.{decimals}f}"
            except:
                return str(value)

        # Registrar filtros
        self.env.filters['strftime'] = strftime_filter
        self.env.filters['money'] = format_money

    def render_gastos_recientes(self, gastos, dias=30):
        """Renderiza plantilla de gastos recientes"""
        template = self.env.get_template('gastos_recientes.md')
        return template.render(
            gastos=gastos,
            dias=dias,
            simbolo_moneda=SIMBOLO_MONEDA
        )

    def render_resumen_total(self, total, cantidad, promedio, dias=30):
        """Renderiza plantilla de resumen total"""
        template = self.env.get_template('resumen_total.md')
        return template.render(
            total=total,
            cantidad=cantidad,
            promedio=promedio,
            dias=dias,
            simbolo_moneda=SIMBOLO_MONEDA
        )

    def render_gastos_categorias(self, categorias, dias=30):
        """Renderiza plantilla de gastos por categoría"""
        template = self.env.get_template('gastos_categorias.md')
        total_general = sum(cat[1] for cat in categorias)
        return template.render(
            categorias=categorias,
            dias=dias,
            total_general=total_general,
            simbolo_moneda=SIMBOLO_MONEDA
        )


# Instancia global del servicio
template_service = TemplateService()

