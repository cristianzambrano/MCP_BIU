from fastmcp import FastMCP
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import statistics

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

mcp = FastMCP("MCP Estacion Meteorologica")

TABLA = "datos_sensor"


def limpiar_valores(datos, campo):
    return [
        float(x[campo])
        for x in datos
        if x.get(campo) is not None
    ]


@mcp.tool()
def obtener_ultima_lectura() -> dict:
    """
    Obtiene la última lectura registrada por la estación meteorológica.
    """
    response = (
        supabase.table(TABLA)
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return {"mensaje": "No hay lecturas registradas"}

    return response.data[0]


@mcp.tool()
def obtener_ultimas_lecturas(limite: int = 50) -> list:
    """
    Obtiene las últimas lecturas de temperatura, humedad y presión.
    """
    response = (
        supabase.table(TABLA)
        .select("*")
        .order("created_at", desc=True)
        .limit(limite)
        .execute()
    )

    return response.data


@mcp.tool()
def obtener_datos_grafico(limite: int = 100) -> list:
    """
    Obtiene datos ordenados cronológicamente para gráficos del dashboard.
    """
    response = (
        supabase.table(TABLA)
        .select("created_at,temp,humedad,presion,id_sensor")
        .order("created_at", desc=False)
        .limit(limite)
        .execute()
    )

    return response.data


@mcp.tool()
def obtener_lecturas_por_sensor(id_sensor: int, limite: int = 100) -> list:
    """
    Obtiene las lecturas de un sensor específico.
    """
    response = (
        supabase.table(TABLA)
        .select("*")
        .eq("id_sensor", id_sensor)
        .order("created_at", desc=False)
        .limit(limite)
        .execute()
    )

    return response.data


@mcp.tool()
def obtener_lecturas_por_fecha(fecha_inicio: str, fecha_fin: str) -> list:
    """
    Obtiene lecturas entre dos fechas.

    Ejemplo:
    fecha_inicio = '2026-06-01T00:00:00Z'
    fecha_fin = '2026-06-08T23:59:59Z'
    """
    response = (
        supabase.table(TABLA)
        .select("*")
        .gte("created_at", fecha_inicio)
        .lte("created_at", fecha_fin)
        .order("created_at", desc=False)
        .execute()
    )

    return response.data


@mcp.tool()
def obtener_resumen_estacion(limite: int = 100) -> dict:
    """
    Calcula resumen estadístico de las últimas lecturas.
    """
    response = (
        supabase.table(TABLA)
        .select("*")
        .order("created_at", desc=True)
        .limit(limite)
        .execute()
    )

    datos = response.data

    if not datos:
        return {"mensaje": "No hay datos disponibles"}

    temperaturas = limpiar_valores(datos, "temp")
    humedades = limpiar_valores(datos, "humedad")
    presiones = limpiar_valores(datos, "presion")

    return {
        "total_lecturas": len(datos),
        "temperatura_promedio": round(statistics.mean(temperaturas), 2),
        "temperatura_maxima": max(temperaturas),
        "temperatura_minima": min(temperaturas),
        "humedad_promedio": round(statistics.mean(humedades), 2),
        "humedad_maxima": max(humedades),
        "humedad_minima": min(humedades),
        "presion_promedio": round(statistics.mean(presiones), 2),
        "presion_maxima": max(presiones),
        "presion_minima": min(presiones),
        "ultima_fecha": datos[0]["created_at"]
    }


@mcp.tool()
def detectar_alertas() -> dict:
    """
    Detecta alertas meteorológicas básicas usando la última lectura.
    """
    lectura = obtener_ultima_lectura()

    if "mensaje" in lectura:
        return lectura

    alertas = []

    temp = float(lectura.get("temp") or 0)
    humedad = float(lectura.get("humedad") or 0)
    presion = float(lectura.get("presion") or 0)

    if temp >= 35:
        alertas.append("Temperatura alta")

    if temp <= 15:
        alertas.append("Temperatura baja")

    if humedad >= 85:
        alertas.append("Humedad elevada")

    if presion < 1000:
        alertas.append("Presión baja, posible cambio climático o lluvia")

    return {
        "estado": "Con alertas" if alertas else "Normal",
        "alertas": alertas,
        "ultima_lectura": lectura
    }


@mcp.tool()
def datos_para_dashboard(limite: int = 100) -> dict:
    """
    Devuelve todos los datos que necesita una IA para crear un dashboard.
    """
    return {
        "ultima_lectura": obtener_ultima_lectura(),
        "resumen": obtener_resumen_estacion(limite),
        "alertas": detectar_alertas(),
        "datos_grafico": obtener_datos_grafico(limite),
        "tabla": obtener_ultimas_lecturas(limite),
        "graficos_recomendados": [
            "Temperatura vs tiempo",
            "Humedad vs tiempo",
            "Presión atmosférica vs tiempo"
        ]
    }


@mcp.tool()
def generar_prompt_dashboard() -> str:
    """
    Genera un prompt para que una IA cree un dashboard web.
    """
    return """
Crea un dashboard web moderno para una estación meteorológica IoT usando los datos de la herramienta datos_para_dashboard.

El dashboard debe incluir:
- Tarjetas de temperatura, humedad y presión actual.
- Gráficos de línea para temperatura, humedad y presión.
- Tabla con las últimas lecturas.
- Sección de alertas meteorológicas.
- Diseño responsivo.
- Estilo académico y profesional.
"""


if __name__ == "__main__":
     mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )