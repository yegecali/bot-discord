# ❌ ERROR - {{ contexto }}

## 🔴 Tipo de Error
```
{{ tipo_error }}
```

## 💬 Mensaje
{{ mensaje }}

## ⏰ Información de Tiempo
**{{ timestamp }}**

{% if datos_adicionales %}
## 📊 Datos Adicionales
{% for clave, valor in datos_adicionales.items() %}
- **{{ clave }}:** `{{ valor }}`
{% endfor %}
{% endif %}

## 📋 Traceback Completo
```
{{ traceback }}
```

---
*Sistema de manejo de errores centralizado - BotPersonal*

