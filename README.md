# 🌦️ MCP Estación Meteorológica

Un servidor **Model Context Protocol (MCP)** basado en FastMCP que proporciona acceso a datos meteorológicos en tiempo real desde una estación conectada a **Supabase**.

## 📋 Descripción del Proyecto

Este proyecto es un servidor MCP que actúa como intermediario entre aplicaciones cliente y una base de datos Supabase que almacena lecturas de sensores meteorológicos. Ofrece herramientas y prompts para consultar, analizar y visualizar datos meteorológicos en tiempo real.

### Características principales:
- ✅ Conexión a Supabase para acceso a datos en tiempo real
- 📊 Herramientas para obtener datos meteorológicos
- 📈 Generación de resúmenes y estadísticas
- 🚨 Detección automática de alertas meteorológicas
- 📉 Preparación de datos para gráficos
- 🎨 Prompts para generación de dashboards personalizados
- 🔄 Soporte para análisis de tendencias históricas

---

## 🚀 Instalación

### Requisitos previos
- **Python 3.8+** instalado en tu sistema
- **pip** (gestor de paquetes de Python)
- Una cuenta y base de datos en **Supabase**
- Credenciales de Supabase (URL y API Key)

### Pasos de instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   cd c:\Code\MCP_BIU
   ```

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   - Crear un archivo `.env` en la raíz del proyecto
   - Añadir las siguientes variables:
     ```
     SUPABASE_URL=tu_url_supabase
     SUPABASE_KEY=tu_api_key_supabase
     ```

---

## ⚙️ Configuración

### Variables de entorno necesarias

El proyecto requiere las siguientes variables en el archivo `.env`:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SUPABASE_URL` | URL base de tu proyecto Supabase | `https://abc123.supabase.co` |
| `SUPABASE_KEY` | API Key de Supabase (anon o service) | `eyJhbGciOiJI...` |

### Base de datos Supabase

El proyecto espera una tabla llamada `datos_sensor` con la siguiente estructura:

```sql
CREATE TABLE datos_sensor (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  id_sensor TEXT,
  temp FLOAT,
  humedad FLOAT,
  presion FLOAT
);
```

---

## 📖 Uso

### Iniciar el servidor

```bash
python server.py
```

El servidor MCP estará listo para recibir conexiones de clientes que implementen el protocolo MCP.

### Uso como cliente MCP

Este servidor debe ser utilizado como un servidor MCP en aplicaciones cliente. Por ejemplo, con Claude o herramientas que soporten MCP.

---

## 🛠️ Herramientas Disponibles

El servidor ofrece las siguientes herramientas MCP:

### 1. `obtener_ultima_lectura()`
Obtiene la lectura más reciente registrada por la estación.

**Devuelve:**
- ID del registro
- Fecha y hora de registro (`created_at`)
- Temperatura (`temp`)
- Humedad (`humedad`)
- Presión atmosférica (`presion`)
- ID del sensor (`id_sensor`)

**Usar cuando:**
- El usuario pregunta por la temperatura, humedad o presión actual
- Se necesita el estado actual de la estación

---

### 2. `obtener_ultimas_lecturas(limite: int = 50)`
Obtiene una lista de las últimas lecturas registradas.

**Parámetros:**
- `limite` (int): Número máximo de registros a devolver (default: 50)

**Devuelve:**
- Lista ordenada de lecturas desde la más reciente hacia atrás

**Usar cuando:**
- Se necesita un histórico reciente
- Se requiere una tabla de datos
- Se solicita un listado de mediciones

---

### 3. `obtener_datos_grafico(limite: int = 100)`
Prepara datos meteorológicos para construir gráficos.

**Parámetros:**
- `limite` (int): Número máximo de registros (default: 100)

**Devuelve:**
- Fecha y hora (`created_at`)
- Temperatura (`temp`)
- Humedad (`humedad`)
- Presión (`presion`)
- ID del sensor (`id_sensor`)
- Datos ordenados cronológicamente

**Usar cuando:**
- Se necesita construir gráficos
- Se requiere serie temporal
- Se solicita visualización histórica

---

### 4. `obtener_resumen_estacion(limite: int = 100)`
Calcula estadísticas de la estación meteorológica.

**Parámetros:**
- `limite` (int): Cantidad de lecturas recientes para análisis (default: 100)

**Devuelve:**
- `total_lecturas`: Número de registros analizados
- `temperatura_promedio`, `temperatura_maxima`, `temperatura_minima`
- `humedad_promedio`, `humedad_maxima`, `humedad_minima`
- `presion_promedio`, `presion_maxima`, `presion_minima`

**Usar cuando:**
- Se solicitan promedios o estadísticas
- Se pregunta por máximos y mínimos
- Se requiere resumen general

---

### 5. `detectar_alertas()`
Detecta alertas meteorológicas basadas en la última lectura.

**Criterios de alerta:**
- Temperatura ≥ 35°C → "Temperatura alta"
- Temperatura ≤ 15°C → "Temperatura baja"
- Humedad ≥ 85% → "Humedad elevada"
- Presión < 1000 hPa → "Posible lluvia"

**Devuelve:**
- `estado`: "Normal" o "Con alertas"
- `alertas`: Lista de alertas detectadas

**Usar cuando:**
- Se pregunta por alertas o riesgos
- Se necesita el estado actual de la estación

---

### 6. `datos_para_dashboard(limite: int = 100)`
Obtiene todos los datos necesarios para construir un dashboard completo.

**Parámetros:**
- `limite` (int): Número máximo de registros (default: 100)

**Devuelve:**
- `ultima_lectura`: Última medición registrada
- `resumen`: Estadísticas generales
- `alertas`: Alertas actuales
- `historico`: Datos para gráficos
- `tabla`: Últimas lecturas en tabla

**Usar cuando:**
- Se necesita crear un dashboard
- Se requiere panel meteorológico completo
- Se solicita una página de monitoreo

---

## 📝 Prompts Disponibles

### 1. `prompt_dashboard_tendencias(fecha_inicio, fecha_fin)`
Genera un análisis de tendencias entre dos fechas.

**Parámetros:**
- `fecha_inicio`: Fecha inicial en formato de string
- `fecha_fin`: Fecha final en formato de string

**Genera:**
- Gráficos de serie temporal
- Detección de picos máximos y mínimos
- Cambios bruscos detectados
- Estadísticas completas
- Conclusiones automáticas

**Salida:** Página web HTML completa (estilo Power BI/Grafana)

---

### 2. `prompt_dashboard_personalizado(tipo_dashboard, limite)`
Crea un dashboard meteorológico personalizado.

**Parámetros:**
- `tipo_dashboard` (str): Tipo de dashboard: "ejecutivo", "técnico", etc. (default: "ejecutivo")
- `limite` (int): Número de registros a incluir (default: 100)

**Genera:**
- KPIs principales
- Gráficos interactivos
- Alertas automáticas
- Tabla de lecturas recientes
- Conclusiones

**Salida:** Página web HTML completa interactiva

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Obtener temperatura actual
```
Usuario: ¿Cuál es la temperatura actual?
MCP → obtener_ultima_lectura()
Resultado: Temperatura actual: 24.5°C
```

### Ejemplo 2: Generar un gráfico de temperatura
```
Usuario: Muéstrame un gráfico de temperatura
MCP → obtener_datos_grafico(limite=100)
Resultado: Gráfico interactivo con serie temporal
```

### Ejemplo 3: Obtener resumen estadístico
```
Usuario: ¿Cuál es el promedio de temperatura de hoy?
MCP → obtener_resumen_estacion(limite=100)
Resultado: Temperatura promedio: 22.3°C, Máxima: 28.1°C, Mínima: 18.5°C
```

### Ejemplo 4: Crear un dashboard
```
Usuario: Crea un dashboard meteorológico
MCP → datos_para_dashboard(limite=100)
Resultado: Página web completa con todos los datos
```

---

## 📁 Estructura del Proyecto

```
MCP_BIU/
├── server.py              # Servidor MCP principal
├── requirements.txt       # Dependencias del proyecto
├── .env                   # Variables de entorno (no incluido en repo)
└── README.md             # Este archivo
```

---

## 🔧 Dependencias

El proyecto utiliza las siguientes librerías Python:

| Librería | Versión | Propósito |
|----------|---------|----------|
| `fastmcp` | Latest | Framework MCP |
| `supabase` | Latest | Cliente de Supabase |
| `python-dotenv` | Latest | Gestión de variables de entorno |

---

## 🐛 Solución de Problemas

### Error: "Faltan SUPABASE_URL o SUPABASE_KEY"
**Solución:** Verifica que el archivo `.env` existe y contiene las variables correctas.

### Error: No conecta a Supabase
**Solución:** 
- Verifica que SUPABASE_URL y SUPABASE_KEY son correctas
- Comprueba tu conexión a internet
- Verifica que la tabla `datos_sensor` existe en tu base de datos

### No hay datos ("No hay lecturas registradas")
**Solución:**
- Verifica que hay datos insertados en la tabla `datos_sensor`
- Comprueba que los sensores están enviando datos a Supabase

### Error de módulos no encontrados
**Solución:**
- Asegúrate de haber activado el entorno virtual
- Ejecuta `pip install -r requirements.txt` nuevamente

---

## 📚 Funcionalidades Internas

El servidor incluye funciones internas de utilidad:

- `limpiar_valores()`: Filtra y convierte valores válidos de un campo
- `_obtener_ultima_lectura()`: Consulta Supabase por la última lectura
- `_obtener_ultimas_lecturas()`: Obtiene múltiples registros recientes
- `_obtener_datos_grafico()`: Prepara datos cronológicos
- `_obtener_resumen_estacion()`: Calcula estadísticas
- `_detectar_alertas()`: Analiza condiciones de riesgo
- `_datos_para_dashboard()`: Integra todos los datos

---

## 🎯 Casos de Uso

Este servidor es ideal para:

- 📱 **Aplicaciones móviles**: Obtener datos meteorológicos en tiempo real
- 🌐 **Dashboards web**: Visualización interactiva de tendencias
- 📊 **Análisis de datos**: Estadísticas y tendencias históricas
- 🤖 **Sistemas IA**: Integración con Claude u otros LLMs para análisis automático
- 🚨 **Alertas automáticas**: Monitoreo y detección de anomalías
- 📈 **Reporting**: Generación automática de reportes

---

## 📞 Soporte

Para más información sobre:
- **FastMCP**: https://github.com/zglide/fastmcp
- **Supabase**: https://supabase.com/docs
- **Model Context Protocol**: https://modelcontextprotocol.io/

---

## 📄 Licencia

Este proyecto utiliza las dependencias con sus respectivas licencias.

---

**Última actualización:** Junio 2026
