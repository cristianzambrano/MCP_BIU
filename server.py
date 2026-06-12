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
    return [ float(x[campo]) 
            for x in datos
              if x.get(campo) is not None 
              ]

# ==========================
# FUNCIONES INTERNAS
# ==========================

def _obtener_ultima_lectura():

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


def _obtener_ultimas_lecturas(limite=50):

    response = (
        supabase.table(TABLA)
        .select("*")
        .order("created_at", desc=True)
        .limit(limite)
        .execute()
    )

    return response.data


def _obtener_datos_grafico(limite=100):

    response = (
        supabase.table(TABLA)
        .select("created_at,temp,humedad,presion,id_sensor")
        .order("created_at")
        .limit(limite)
        .execute()
    )

    return response.data


def _obtener_resumen_estacion(limite=100):

    datos = _obtener_ultimas_lecturas(limite)

    if not datos:
        return {"mensaje": "No hay datos"}

    temperaturas = limpiar_valores(datos, "temp")
    humedades = limpiar_valores(datos, "humedad")
    presiones = limpiar_valores(datos, "presion")

    return {
        "total_lecturas": len(datos),
        "temperatura_promedio": round(statistics.mean(temperaturas),2),
        "temperatura_maxima": max(temperaturas),
        "temperatura_minima": min(temperaturas),
        "humedad_promedio": round(statistics.mean(humedades),2),
        "humedad_maxima": max(humedades),
        "humedad_minima": min(humedades),
        "presion_promedio": round(statistics.mean(presiones),2),
        "presion_maxima": max(presiones),
        "presion_minima": min(presiones)
    }


def _detectar_alertas():

    lectura = _obtener_ultima_lectura()

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
        alertas.append("Posible lluvia")

    return {
        "estado": "Con alertas" if alertas else "Normal",
        "alertas": alertas
    }


def _datos_para_dashboard(limite=100):

    return {
        "ultima_lectura": _obtener_ultima_lectura(),
        "resumen": _obtener_resumen_estacion(limite),
        "alertas": _detectar_alertas(),
        "historico": _obtener_datos_grafico(limite),
        "tabla": _obtener_ultimas_lecturas(limite)
    }

# ==========================
# HERRAMIENTAS MCP
# ==========================

@mcp.tool()
def obtener_ultima_lectura():
    return _obtener_ultima_lectura()


@mcp.tool()
def obtener_ultimas_lecturas(limite:int=50):
    return _obtener_ultimas_lecturas(limite)


@mcp.tool()
def obtener_datos_grafico(limite:int=100):
    return _obtener_datos_grafico(limite)


@mcp.tool()
def obtener_resumen_estacion(limite:int=100):
    return _obtener_resumen_estacion(limite)


@mcp.tool()
def detectar_alertas():
    return _detectar_alertas()


@mcp.tool()
def datos_para_dashboard(limite:int=100):
    return _datos_para_dashboard(limite)

@mcp.prompt()
def prompt_dashboard_tendencias(fecha_inicio: str, fecha_fin: str):
    """
    Prompt para analizar tendencias entre dos fechas.
    """
    return f"""
Utiliza la herramienta obtener_lecturas_por_fecha(
    fecha_inicio="{fecha_inicio}",
    fecha_fin="{fecha_fin}"
).

Construye un dashboard analítico de tendencias para una estación meteorológica.

Incluye:

1. Serie temporal de temperatura.
2. Serie temporal de humedad.
3. Serie temporal de presión atmosférica.
5. Detección automática de:
   - Picos máximos
   - Picos mínimos
   - Cambios bruscos
6. Estadísticas:
   - Promedio
   - Desviación estándar
   - Valor máximo
   - Valor mínimo
7. Conclusiones automáticas sobre el comportamiento de la estación.

El dashboard debe ser una página web descargable.
Entrega el resultado como una página web completa en HTML, CSS y JavaScript.
El diseño debe ser tipo Power BI o Grafana.
"""

@mcp.prompt()
def prompt_dashboard_personalizado(tipo_dashboard: str = "ejecutivo", limite: int = 100):
    return f"""
Utiliza la herramienta datos_para_dashboard(limite={limite}).

Crea un dashboard meteorológico de tipo: {tipo_dashboard}.

Incluye KPIs, gráficos interactivos, alertas automáticas, tabla de lecturas recientes y conclusiones.

Entrega el resultado como una página web completa en HTML, CSS y JavaScript.
"""
