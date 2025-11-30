# 💰 Gastos Recientes

**Período:** Últimos {{ dias }} días | **Total de registros:** {{ gastos|length }}

---

{% if gastos|length > 0 %}
{% for gasto in gastos[:10] %}
### {{ loop.index }}. {{ gasto.categoria }}
- **Monto:** `{{ simbolo_moneda }} {{ "%.2f"|format(gasto.monto) }}`
- **Descripción:** {{ gasto.descripcion }}
- **Fecha:** 📅 {{ gasto.fecha }}

{% endfor %}

{% if gastos|length > 10 %}
---
📌 *y {{ gastos|length - 10 }} gasto(s) más...*
{% endif %}

{% else %}
⚠️ **No hay gastos registrados en este período**
{% endif %}

---

*Última actualización: {{ "now"|strftime("%d/%m/%Y %H:%M") }}*

