# 🏷️ Gastos por Categoría

## Período: Últimos {{ dias }} días

---

{% if categorias|length > 0 %}

{% for categoria, total, cantidad in categorias %}
### 📁 {{ categoria }}

| Concepto | Valor |
|----------|-------|
| **Monto Total** | `{{ simbolo_moneda }} {{ "%.2f"|format(total) }}` |
| **# Compras** | {{ cantidad }} |
| **Promedio** | `{{ simbolo_moneda }} {{ "%.2f"|format(total / cantidad) if cantidad > 0 else "0.00" }}` |

---

{% endfor %}

## 📈 Resumen General

| Categoría | Monto | % del Total |
|-----------|-------|-------------|
{% for categoria, total, cantidad in categorias %}
| **{{ categoria }}** | `{{ simbolo_moneda }} {{ "%.2f"|format(total) }}` | {{ "%.1f"|format((total / total_general) * 100) }}% |
{% endfor %}
| **TOTAL** | **`{{ simbolo_moneda }} {{ "%.2f"|format(total_general) }}`** | **100%** |

{% else %}
⚠️ **No hay categorías registradas**
{% endif %}

---

*Última actualización: {{ "now"|strftime("%d/%m/%Y %H:%M") }}*

