#  End-to-End Data Engineering Pipeline: Desigualdad Social en España

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Matrix%20Testing-2ea44f)](https://github.com/features/actions)
[![Quality Gate](https://img.shields.io/badge/Code%20Quality-Strict-red)](https://flake8.pycqa.org/en/latest/)
[![SQL Server](https://img.shields.io/badge/DB-SQL%20Server%20ODBC%2018-lightgrey)]()

> **Visión General:** Pipeline ETL modular de nivel productivo diseñado para ingesta, transformación y validación de datos socioeconómicos (INE y EUROSTAT). El proyecto simula un entorno empresarial real priorizando la robustez, la calidad del dato y la automatización DevOps.

---

##  Ingeniería y Decisiones de Arquitectura

Este proyecto no es solo un script de movimiento de datos; es una implementación de ingeniería de software aplicada a datos.

### 1. Arquitectura ETL Modular y Resiliente
El sistema desacopla estrictamente las responsabilidades para garantizar mantenibilidad y testabilidad:

`mermaid
graph TD
    subgraph Sources
        INE[INE (JSON/CSV)]
        EURO[Eurostat (SDMX API)]
    end

    subgraph ETL_Pipeline["ETL Pipeline (Python)"]
        E[Extract] --> T[Transform]
        T --> V{Validation Framework}
        V -- "Pass" --> L[Load to SQL]
        V -- "Fail" --> Alert[Log Error & Stop]
    end

    subgraph Storage
        SQL[(SQL Server)]
        Logs[Validation Logs]
    end

    INE --> E
    EURO --> E
    L --> SQL
    V -.-> Logs
`

* **Extract & Transform:** Normalización de fuentes dispares (API SDMX de Eurostat + CSV/JSON de INE) en estructuras pandas optimizadas.
* **Validation Framework:** No solo "muevo" datos; aseguro su fiabilidad. Implementé un framework personalizado que verifica integridad de esquema, reglas de negocio (ej. Gini 0-100) y continuidad temporal antes de la carga.
* **Load (Idempotencia):** Los procesos de carga a SQL Server están diseñados para ser re-ejecutables (idempotentes), evitando duplicidad de datos ante fallos y reintentos.

### 2. DevOps y CI/CD Avanzado (GitHub Actions)
El pipeline de integración continua está diseñado para entornos híbridos y robustez empresarial:
* **Matriz de Ejecución (Matrix Testing):** El pipeline aprovisiona explícitamente drivers ODBC tanto en **Ubuntu** como en **Windows Server**, garantizando que el ETL es agnóstico al sistema operativo del despliegue.
* **Gestión de Secretos y Entornos:** Lógica condicional (if: env.SKIP_DB_LOAD != 'true') que detecta automáticamente el entorno (Prod/CI) para adaptar el flujo sin romper el pipeline.
* **Quality Gates Estrictos:** El código no pasa a producción si no supera:
    * Black (Formateo PEP 8)
    * Flake8 (Linting y detección de errores)
    * MyPy (Tipado estático)

### 3. Seguridad y Conectividad
* **ODBC Driver 18:** Migración forzada para compatibilidad con estándares de seguridad modernos (OpenSSL 3 / Ubuntu 24.04).
* **Encriptación:** Manejo de cadenas de conexión con soporte para TrustServerCertificate y encriptación en tránsito.

---

##  Stack Tecnológico

| Área | Herramientas |
|------|--------------|
| **Lenguaje** | Python 3.11+ (Pandas, NumPy, PyODBC, Requests) |
| **Orquestación & CI** | GitHub Actions (Workflows, Matrix Strategy) |
| **Base de Datos** | SQL Server (Azure/Local), T-SQL |
| **Calidad & Testing** | Pytest, Flake8, Black, MyPy, Custom Validation Framework |
| **Infraestructura** | Docker (opcional), Gestión de entornos virtuales |

---

##  Estructura del Proyecto

El repositorio sigue una estructura de "Data Product" profesional, separando lógica, configuración y orquestación:

`	ext
desigualdad_social_etl/
  .github/workflows/       # CI/CD Pipelines (Matrix testing, Linting)
  src/                     # Lógica de negocio modular
     extractors/          # Conectores a APIs (Eurostat) y ficheros (INE)
     loaders/             # Carga idempotente a SQL Server
     validacion.py        # Reglas de calidad de datos
  utils/                   # Utilidades transversales
     validation_framework.py # Motor de validación custom
     config.py            # Gestión de configuración centralizada
  notebooks/               # Análisis y Orquestación
     00_etl/              # Pipelines de Ingesta y Transformación
     01_analisis_nacional/
     02_analisis_regional/
     06_sintesis/         # Informes ejecutivos
  tests/                   # Tests unitarios e integración
  docs/                    # Documentación técnica y funcional
  scripts/                 # Scripts de mantenimiento y limpieza
  templates/               # Estándares y plantillas de código
  requirements.txt         # Dependencias del proyecto
`

##  Quick Start

### 1. Configuración

`ash
# Clonar y preparar entorno
git clone https://github.com/tu-usuario/Desigualdad-Espana.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
`

### 2. Variables de Entorno (.env)
El proyecto utiliza python-dotenv para seguridad. Crea un archivo .env:

`ini
DB_CONNECTION_STRING=DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=desigualdad;Trusted_Connection=yes;TrustServerCertificate=yes;
`

### 3. Ejecución del Pipeline

`ash
# Ejecución completa (E-T-L)
python notebooks/00_etl/01_run_etl.py

# Ejecución de Suite de Validación
python notebooks/00_etl/02_run_validation.py
`

##  Impacto y Resultados
El pipeline procesa y consolida **30 tablas analíticas** cubriendo indicadores críticos (AROPE, Gini, IPC), garantizando una coherencia del **99.5%** entre fuentes nacionales (INE) y europeas (Eurostat).

Para detalles metodológicos completos, ver [docs/DICCIONARIO_DATOS.md](docs/DICCIONARIO_DATOS.md).

##  Contacto
Este proyecto demuestra mi capacidad para construir infraestructura de datos sólida y mantenible.

**Autor:** Mario  
**Enfoque:** Data Engineering, Data Quality, CI/CD.

---

###  Licencia
Este proyecto es de código abierto y está disponible bajo la licencia MIT.
