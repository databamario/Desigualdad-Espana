# 🏗️ ESTRUCTURA DEL PROYECTO: Análisis Multidimensional de Desigualdad en España

## 📊 Visión General

Este proyecto analiza la **desigualdad social en España** desde múltiples perspectivas: temporal, geográfica, sociodemográfica y económica.

---

## 🎯 BLOQUES DE ANÁLISIS

### 📦 BLOQUE 0: ETL y Preparación de Datos

**Objetivo**: Cargar y preparar todos los datos necesarios

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `01_desigualdad_etl.ipynb` | ETL completo: Extracción INE/Eurostat → SQL Server | ✅ Completado |

**Salida**: 12 tablas en SQL Server (base de datos `desigualdad`)

---

### 📈 BLOQUE 1: Análisis de Desigualdad General (Nacional)

**Objetivo**: Analizar la desigualdad a nivel agregado de España (2008-2023)

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `02_analisis_desigualdad.ipynb` | Análisis exploratorio inicial (hasta celda 17) | ✅ Completado |
| `03_verificacion_deciles.ipynb` | Verificación D1 vs D10 + Indicadores oficiales | ✅ Completado |
| `04_analisis_inflacion_diferencial.ipynb` | IPC sectorial por decil (EPF + IPC) | ⏳ Pendiente |

**Contenido del Bloque 1**:
- ✅ Evolución del umbral de pobreza (2008-2023)
- ✅ Gini y S80/S20 (indicadores oficiales)
- ✅ AROPE nacional (riesgo de pobreza y exclusión)
- ✅ Carencia material nacional
- ✅ Renta por deciles (D1-D10)
- ✅ Comparación D1 vs D10 (pobres vs ricos)
- ✅ Ratio D10/D1 y brechas absolutas
- ✅ Análisis de inflación (IPC general)
- ⚠️ Análisis de inflación diferencial (documentado, no implementado)

**Conclusiones del Bloque 1**:
- ✅ Desigualdad relativa disminuyó levemente (Gini -5.2%, S80/S20 -8.5%)
- ✅ Ratio D10/D1 aumentó +2.1% (de 9.57x a 9.77x)
- ✅ AROPE aumentó +19.8% (más exclusión social)
- ✅ Todos los deciles perdieron renta real, pero D1 perdió más (-6.96% vs -4.98%)

---

### 🗺️ BLOQUE 2: Análisis Geográfico y Sociodemográfico (Regional)

**Objetivo**: Identificar desigualdades territoriales y sociales

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `05_analisis_geografico_ccaa.ipynb` | Desigualdad por Comunidades Autónomas | 📝 A crear |
| `06_analisis_sociodemografico.ipynb` | Pobreza por edad, sexo, tipo de hogar, situación laboral | 📝 A crear |

**Contenido del Bloque 2**:

#### 📍 Análisis Geográfico (CCAA)
- Gini y S80/S20 por Comunidad Autónoma
- Ranking de desigualdad regional
- Evolución temporal por región
- Mapas de calor geográficos
- Convergencia o divergencia regional

#### 👥 Análisis Sociodemográfico
- **Por edad**: Menores de 16, 16-64, 65+
- **Por sexo**: Hombres vs Mujeres
- **Por tipo de hogar**: 
  - Persona sola
  - Familia monoparental
  - Pareja con hijos
  - Otros hogares
- **Por situación laboral**:
  - Ocupados
  - Desempleados
  - Inactivos
  - Intensidad laboral del hogar

**Fuentes de datos**:
- `INE_Gini_S80S20_CCAA` (Gini y S80/S20 por CCAA)
- `INE_AROPE_Edad_Sexo` (AROPE por grupos demográficos)
- `EUROSTAT_AROPE_Edad_Sexo` (Comparativa europea)
- `INE_Carencia_Material_Decil` (Carencia por grupos)

---

### 🌍 BLOQUE 3: Comparativa Internacional (España vs Europa)

**Objetivo**: Posicionar a España en el contexto europeo

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `07_comparativa_europa.ipynb` | España vs UE (ranking, convergencia, políticas) | 📝 A crear |

**Contenido del Bloque 3**:
- Ranking de España en desigualdad (UE-27)
- Evolución comparada: España vs media UE vs países nórdicos vs sur de Europa
- Impacto de políticas redistributivas (antes/después de transferencias)
- AROPE comparado por país
- Convergencia o divergencia con Europa

**Fuentes de datos**:
- `EUROSTAT_Gini_S80S20` (Gini europeo)
- `EUROSTAT_AROPE_Edad_Sexo` (AROPE europeo)

---

### 💼 BLOQUE 4: Análisis Sectorial y Laboral

**Objetivo**: Entender desigualdad por sector económico y mercado laboral

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `08_analisis_sectorial.ipynb` | Desigualdad por sector económico | 📝 A crear |
| `09_analisis_laboral.ipynb` | Brecha salarial, precariedad, intensidad laboral | 📝 A crear |

**Contenido del Bloque 4**:
- Desigualdad por sector económico
- Brecha salarial de género
- Impacto del desempleo en AROPE
- Intensidad laboral del hogar (trabajo a tiempo completo vs parcial)
- Trabajadores pobres (working poor)

---

### 🔮 BLOQUE 5: Modelado Predictivo y Simulaciones

**Objetivo**: Proyecciones y escenarios futuros

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `10_modelado_predictivo.ipynb` | Proyecciones de desigualdad y AROPE | 📝 A crear |
| `11_simulaciones_politicas.ipynb` | Simulación de impacto de políticas públicas | 📝 A crear |

**Contenido del Bloque 5**:
- Proyecciones de Gini y AROPE (2024-2030)
- Simulación de impacto de:
  - Aumento del SMI (Salario Mínimo Interprofesional)
  - Renta Básica Universal
  - Impuestos progresivos
  - Transferencias sociales

---

### 📋 BLOQUE 6: Síntesis y Conclusiones Finales

**Objetivo**: Consolidar hallazgos y recomendaciones

| Notebook | Descripción | Estado |
|----------|-------------|--------|
| `12_sintesis_final.ipynb` | Dashboard ejecutivo y conclusiones | 📝 A crear |

**Contenido del Bloque 6**:
- Dashboard interactivo con KPIs principales
- Resumen ejecutivo
- Recomendaciones de política pública
- Limitaciones del análisis
- Líneas de investigación futuras

---

## 📂 ESTRUCTURA DE CARPETAS PROPUESTA

```
desigualdad_social_etl/
├── README.md                                  # Descripción general del proyecto
├── ESTRUCTURA_PROYECTO.md                     # Este archivo (arquitectura)
├── INDEX.md                                   # Índice navegable de notebooks
├── requirements.txt                           # Dependencias Python
│
├── notebooks/
│   ├── 00_etl/
│   │   └── 01_desigualdad_etl.ipynb          # ✅ ETL completo
│   │
│   ├── 01_analisis_nacional/
│   │   ├── 02_analisis_desigualdad.ipynb     # ✅ Análisis exploratorio
│   │   ├── 03_verificacion_deciles.ipynb     # ✅ D1 vs D10
│   │   └── 04_inflacion_diferencial.ipynb    # ⏳ IPC sectorial
│   │
│   ├── 02_analisis_regional/
│   │   ├── 05_geografico_ccaa.ipynb          # 📝 Desigualdad por CCAA
│   │   └── 06_sociodemografico.ipynb         # 📝 Edad, sexo, hogar, laboral
│   │
│   ├── 03_comparativa_europa/
│   │   └── 07_comparativa_europa.ipynb       # 📝 España vs UE
│   │
│   ├── 04_sectorial_laboral/
│   │   ├── 08_sectorial.ipynb                # 📝 Por sector económico
│   │   └── 09_laboral.ipynb                  # 📝 Brecha salarial, precariedad
│   │
│   ├── 05_predictivo/
│   │   ├── 10_modelado.ipynb                 # 📝 Proyecciones
│   │   └── 11_simulaciones.ipynb             # 📝 Políticas públicas
│   │
│   └── 06_sintesis/
│       └── 12_sintesis_final.ipynb           # 📝 Dashboard y conclusiones
│
├── data/                                      # (Opcional) Datos raw/procesados
│   ├── raw/                                  # Datos originales
│   └── processed/                            # Datos procesados
│
├── outputs/                                   # Visualizaciones y reportes
│   ├── figuras/
│   ├── tablas/
│   └── reportes/
│
├── docs/                                      # Documentación adicional
│   ├── METODOLOGIA.md                        # Metodología del análisis
│   ├── FUENTES_DATOS.md                      # Descripción de fuentes
│   └── CONCLUSIONES.md                       # ✅ Ya existe
│
└── desigualdad/                               # ✅ Entorno virtual Python
```

---

## 🔄 FLUJO DE TRABAJO RECOMENDADO

### Fase 1: Completar Bloque 1 (Nacional) ✅ COMPLETADO
- ✅ `02_analisis_desigualdad.ipynb` (hasta celda 17)
- ✅ `03_verificacion_deciles.ipynb` (completo)
- ⏳ `04_inflacion_diferencial.ipynb` (opcional, documentado)

### Fase 2: Bloque 2 (Regional y Sociodemográfico) 🎯 SIGUIENTE
1. Crear `05_analisis_geografico_ccaa.ipynb`
2. Crear `06_analisis_sociodemografico.ipynb`

### Fase 3: Bloque 3 (Europa)
1. Crear `07_comparativa_europa.ipynb`

### Fase 4: Bloques 4-6 (Sectorial, Predictivo, Síntesis)
1. Crear notebooks de análisis sectorial/laboral
2. Modelado predictivo (opcional)
3. Dashboard final

---

## 🎯 ESTADO ACTUAL DEL PROYECTO

| Bloque | Notebooks | Estado Global |
|--------|-----------|---------------|
| **0. ETL** | 1/1 | ✅ 100% Completado |
| **1. Nacional** | 2/3 | ✅ 67% Completado (2 OK, 1 opcional) |
| **2. Regional** | 0/2 | 📝 0% Pendiente |
| **3. Europa** | 0/1 | 📝 0% Pendiente |
| **4. Sectorial** | 0/2 | 📝 0% Pendiente |
| **5. Predictivo** | 0/2 | 📝 0% Pendiente |
| **6. Síntesis** | 0/1 | 📝 0% Pendiente |

**TOTAL**: 3/12 notebooks completados (25%)

---

## 📋 PRÓXIMOS PASOS INMEDIATOS

### 1. Crear esqueleto del Bloque 2 (Regional y Sociodemográfico)

**Notebook 05: Análisis Geográfico (CCAA)**
```python
# Estructura propuesta:
# 1. Configuración
# 2. Carga de datos INE_Gini_S80S20_CCAA
# 3. Ranking de CCAA por Gini
# 4. Evolución temporal por CCAA
# 5. Mapas de calor
# 6. Análisis de convergencia/divergencia
# 7. Conclusiones regionales
```

**Notebook 06: Análisis Sociodemográfico**
```python
# Estructura propuesta:
# 1. Configuración
# 2. AROPE por edad y sexo
# 3. AROPE por tipo de hogar
# 4. AROPE por situación laboral
# 5. Carencia material por grupos
# 6. Interseccionalidad (ej: mujeres + monoparentales)
# 7. Conclusiones sociodemográficas
```

---

## 🔗 DEPENDENCIAS ENTRE NOTEBOOKS

```
01_ETL (base de datos)
    ↓
02_Analisis_Nacional → 03_Verificacion_Deciles
    ↓
05_Geografico_CCAA ← INE_Gini_S80S20_CCAA
06_Sociodemografico ← INE_AROPE_Edad_Sexo
    ↓
07_Comparativa_Europa ← EUROSTAT_*
    ↓
12_Sintesis_Final (consolidación)
```

---

## 📊 TABLAS SQL DISPONIBLES

### Tablas del INE (España)
1. `INE_IPC_Anual` - Índice de Precios al Consumo
2. `INE_Umbral_Pobreza` - Umbral de riesgo de pobreza
3. `INE_Gini_S80S20_CCAA` - Desigualdad por CCAA **← Bloque 2**
4. `INE_AROPE_Edad_Sexo` - Riesgo de pobreza por demografía **← Bloque 2**
5. `INE_Carencia_Material_Decil` - Carencia material **← Bloque 2**
6. `INE_Renta_Media_Decil` - Renta por deciles
7. `INE_Distribucion_Renta` - Distribución detallada
8. `INE_Politicas_Redistributivas` - Impacto de políticas

### Tablas de Eurostat (Europa)
9. `EUROSTAT_Gini_S80S20` - Desigualdad europea **← Bloque 3**
10. `EUROSTAT_AROPE_Edad_Sexo` - AROPE europeo **← Bloque 3**
11. `EUROSTAT_Distribucion_Renta` - Distribución europea
12. `EUROSTAT_Politicas_Redistributivas` - Políticas europeas

---

## ✅ VALIDACIÓN DE DATOS NECESARIA

Antes de comenzar Bloque 2, verificar que estas tablas tienen datos:
- ✅ `INE_Gini_S80S20_CCAA` (todas las CCAA + Total Nacional)
- ✅ `INE_AROPE_Edad_Sexo` (grupos de edad, sexo, tipo de hogar)
- ✅ `INE_Carencia_Material_Decil` (D1-D10)

---

## 📝 NOTAS METODOLÓGICAS

### Limitaciones Documentadas (Bloque 1)
1. Período afectado por crisis (2008-2012, COVID 2020-2021)
2. Carencia material solo disponible para 2023
3. IPC general (no diferencial por decil) - Ver Sección 2.3 de `03_verificacion_deciles.ipynb`
4. Renta media (no mediana) - Sensible a outliers

### Recomendaciones para Bloque 2
1. Usar mapas interactivos (folium, plotly) para visualización geográfica
2. Aplicar tests estadísticos de convergencia (β-convergence)
3. Analizar interseccionalidad (ej: mujeres + edad + tipo de hogar)
4. Comparar evolución temporal por grupos

---

## 🎯 OBJETIVO FINAL DEL PROYECTO

Generar un **análisis integral y riguroso** de la desigualdad en España que:
1. ✅ Documente la evolución temporal (2008-2023)
2. 📝 Identifique desigualdades regionales y sociales
3. 📝 Compare con Europa
4. 📝 Proporcione recomendaciones de política pública
5. 📝 Proyecte escenarios futuros

---

**Fecha de creación**: 29 de octubre de 2025  
**Última actualización**: 29 de octubre de 2025  
**Estado**: Bloque 1 completado, preparando Bloque 2
