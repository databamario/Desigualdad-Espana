#  End-to-End Data Engineering Pipeline: Desigualdad Social en España

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Matrix%20Testing-2ea44f)](https://github.com/features/actions)
[![Quality Gate](https://img.shields.io/badge/Code%20Quality-Strict-red)](https://flake8.pycqa.org/en/latest/)
[![SQL Server](https://img.shields.io/badge/DB-SQL%20Server%20ODBC%2018-lightgrey)]()

> **Visión General:** Pipeline ETL modular de nivel productivo diseñado para ingesta, transformación y validación de datos socioeconómicos (INE y EUROSTAT). El proyecto simula un entorno empresarial real priorizando la robustez, la calidad del dato y la automatización DevOps.

---

## 🧠 Ingeniería y Decisiones de Arquitectura

Este proyecto no es solo un script de ciencia de datos; es una implementación de ingeniería de software aplicada a datos.

### 1. ⚙️ Arquitectura ETL Modular y Resiliente

El sistema desacopla estrictamente las responsabilidades para garantizar mantenibilidad y testabilidad:

```mermaid
flowchart TD
  INE[INE (JSON/CSV)] --> E[Extract]
  EURO[Eurostat (SDMX API)] --> E
  E --> T[Transform]
  T --> V[Validation]
  V -->|Pass| L[Load to SQL]
  V -->|Fail| Alert[Log Error & Stop]
  L --> SQL[(SQL Server)]
  V -.-> Logs[Validation Logs]
```

**Puntos clave del diseño:**
- **Extract & Transform:** Normalización de fuentes dispares (API SDMX de Eurostat + CSV/JSON de INE) en estructuras pandas optimizadas.
- **Validation Framework:** Verificación de integridad de esquema, reglas de negocio (ej. Gini 0–100) y continuidad temporal antes de la carga.
- **Load (Idempotencia):** Procesos re-ejecutables evitando duplicidades ante fallos o reintentos.

---

### 2. 🛠 DevOps y CI/CD Avanzado (GitHub Actions)

Pipeline de integración continua diseñado para entornos híbridos con robustez empresarial:

- **Matrix Testing:** Drivers ODBC instalados dinámicamente en **Ubuntu** y **Windows Server**.
- **Gestión de secretos y entornos:** Lógica condicional para adaptar la ejecución según entorno.
- **Quality Gates obligatorios:**
  - `Black` – Formateo PEP 8  
  - `Flake8` – Linting  
  - `MyPy` – Tipado estático  
  - `Pytest` – Tests unitarios

---

### 3. 🔒 Seguridad y Conectividad

- **ODBC Driver 18:** Compatibilidad con OpenSSL 3 (Ubuntu 24.04 / Azure).
- **Encriptación en tránsito:** Uso de `TrustServerCertificate` y configuración segura de cadena de conexión.
- **Gestión de secretos vía GitHub Actions + .env**

---

## 🧰 Stack Tecnológico

| Área | Herramientas |
|------|---------------|
| **Lenguaje** | Python 3.11+ (Pandas, NumPy, PyODBC, Requests) |
| **Orquestación & CI** | GitHub Actions (Matrix Strategy) |
| **Base de Datos** | SQL Server (Azure/Local), T-SQL |
| **Calidad & Testing** | Pytest, Flake8, Black, MyPy, Validation Framework |
| **Infraestructura** | Docker (opcional), entornos virtuales |

---

## 📁 Estructura del Proyecto

```text
desigualdad_social_etl/
├── .github/workflows/           # 🤖 CI/CD Pipelines (Matrix testing, Linting)
├── src/                         # 🧠 Lógica de negocio modular
│   ├── extractors/              # Conectores a APIs (Eurostat) y ficheros (INE)
│   ├── loaders/                 # Carga idempotente a SQL Server
│   ├── utils/                   # Utilidades transversales
│   └── validation_framework.py  # Motor de validación custom
├── notebooks/                   # 📓 ETL y análisis
│   ├── 00_etl/                  # Pipelines de ingesta y transformación
│   ├── 01_analisis_nacional/    # Ciencia de datos
│   └── 06_sintesis/             # Informes ejecutivos
├── tests/                       # ✅ Tests unitarios e integración
├── docs/                        # 📚 Documentación técnica y funcional
├── scripts/                     # 🔧 Scripts de mantenimiento
└── requirements.txt             # 📦 Dependencias
```

---

## ⚡ Quick Start

### 1. Preparación del entorno

```bash
# Clonar y activar entorno
git clone https://github.com/tu-usuario/Desigualdad-Espana.git
cd Desigualdad-Espana
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Variables de Entorno (`.env`)

```env
DB_CONNECTION_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=desigualdad;Trusted_Connection=yes;TrustServerCertificate=yes;"
```

> **Nota:** las comillas dobles alrededor de la cadena de conexión ayudan a preservar caracteres especiales al exportar la variable en distintos shells.

### 3. Ejecución del Pipeline

```bash
# Ejecución completa (E-T-L)
python notebooks/00_etl/01_run_etl.py

# Validación de datos
python notebooks/00_etl/02_run_validation.py
```

---

## 📊 Impacto y Resultados

El pipeline procesa y consolida **30 tablas analíticas** con indicadores críticos (AROPE, Gini, IPC).  
Se garantiza una coherencia del **99.5%** entre fuentes nacionales (INE) y europeas (Eurostat).

📌 Más detalles en:  
`docs/DICCIONARIO_DATOS.md`

---

## 📬 Contacto

Este proyecto demuestra capacidades reales de **Data Engineering + Data Quality + CI/CD**.

**Autor:** Mario  
**Enfoque:** Ingeniería de Datos, Calidad del Dato, DevOps

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia **MIT**.
