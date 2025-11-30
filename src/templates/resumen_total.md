# 📊 Resumen de Gastos

## Período: Últimos {{ dias }} días

---

## 💵 Total: **{{ simbolo_moneda }} {{ "%.2f"|format(total) }}**

| Métrica | Valor |
|---------|-------|
| 📈 Transacciones | {{ cantidad }} |
| 📊 Promedio | `{{ simbolo_moneda }} {{ "%.2f"|format(promedio) }}` |
| 💰 Máximo | `{{ simbolo_moneda }} {{ "%.2f"|format(total) if cantidad == 1 else "N/A" }}` |

---

{% if cantidad > 0 %}
✅ **{{ cantidad }}** compra(s) registrada(s) en este período

{% if cantidad > 1 %}
📌 Gasto promedio: **{{ simbolo_moneda }} {{ "%.2f"|format(promedio) }}** por transacción
{% endif %}

{% else %}
⚠️ **No hay transacciones en este período**
{% endif %}

---

*Última actualización: {{ "now"|strftime("%d/%m/%Y %H:%M") }}*

