"""
Script de prueba para verificar funciones de utils.py
"""
from src.utils import (
    extraer_numero,
    extraer_numeros_multiples,
    buscar_palabra_clave,
    limpiar_texto,
    normalizar_lineas
)

def test_extraer_numero():
    """Prueba extraer_numero"""
    print("\n=== Prueba extraer_numero ===")

    casos = [
        ("S/. 150.50", 150.50),
        ("$100,25", 100.25),
        ("Monto: 99.99", 99.99),
        ("250", 250.0),
        ("sin números", None),
    ]

    for texto, esperado in casos:
        resultado = extraer_numero(texto)
        estado = "✅" if resultado == esperado else "❌"
        print(f"{estado} extraer_numero('{texto}') = {resultado} (esperado: {esperado})")

def test_extraer_numeros_multiples():
    """Prueba extraer_numeros_multiples"""
    print("\n=== Prueba extraer_numeros_multiples ===")

    texto = "Precio: S/. 100.50, IVA: 18.00, Total: 118.50"
    resultado = extraer_numeros_multiples(texto)
    print(f"Texto: '{texto}'")
    print(f"Números encontrados: {resultado}")
    print(f"✅ Se encontraron {len(resultado)} números" if len(resultado) == 3 else f"❌ Se esperaban 3 números")

def test_buscar_palabra_clave():
    """Prueba buscar_palabra_clave"""
    print("\n=== Prueba buscar_palabra_clave ===")

    lineas = [
        "Primera línea",
        "Segunda línea",
        "Total: 150.00",
        "Cuarta línea"
    ]

    palabras = ["total", "suma", "monto"]
    linea_encontrada, indice = buscar_palabra_clave(lineas, palabras, retornar_indice=True)

    print(f"Lineas: {lineas}")
    print(f"Palabras buscadas: {palabras}")
    print(f"Encontrada: '{linea_encontrada}' en índice {indice}")
    print(f"✅ Palabra encontrada correctamente" if linea_encontrada and indice == 2 else "❌ Error en búsqueda")

def test_limpiar_texto():
    """Prueba limpiar_texto"""
    print("\n=== Prueba limpiar_texto ===")

    texto_sucio = """Primer párrafo
    
    
    Segundo párrafo    con   espacios   extra
    
    Tercer párrafo"""

    resultado = limpiar_texto(texto_sucio)
    print(f"Texto original:\n{repr(texto_sucio)}")
    print(f"\nTexto limpio:\n{repr(resultado)}")
    print(f"✅ Texto limpiado correctamente")

def test_normalizar_lineas():
    """Prueba normalizar_lineas"""
    print("\n=== Prueba normalizar_lineas ===")

    texto = "Primera\n  Segunda  \n\nTercera"
    resultado = normalizar_lineas(texto)

    print(f"Texto original:\n{repr(texto)}")
    print(f"Líneas normalizadas: {resultado}")
    print(f"✅ Líneas normalizadas correctamente" if len(resultado) == 3 else "❌ Error en normalización")

if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBAS DE FUNCIONES UTILS")
    print("=" * 50)

    test_extraer_numero()
    test_extraer_numeros_multiples()
    test_buscar_palabra_clave()
    test_limpiar_texto()
    test_normalizar_lineas()

    print("\n" + "=" * 50)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 50)

