# Metodología Completa: Análisis Desigualdad y Pobreza España 2008-2023

> **Documento técnico complementario al Reporte Ejecutivo**  
> Autor: databamario  
> Proyecto: Desigualdad-Espana  
> Última actualización: 2025-11-20

---

## 📋 Índice

1. [Fuentes de Datos Primarias](#1-fuentes-de-datos-primarias)
2. [Metodología AROPE](#2-metodología-arope)
3. [Proceso de Deflactación](#3-proceso-de-deflactación)
4. [Trayectorias Detalladas por Fase](#4-trayectorias-detalladas-por-fase)
5. [Checklist de Validación](#5-checklist-de-validación)
6. [Registro de Cambios Metodológicos](#6-registro-de-cambios-metodológicos)
7. [Limitaciones Conocidas](#7-limitaciones-conocidas)
8. [Supuestos Críticos](#8-supuestos-críticos)
9. [Referencias Bibliográficas](#9-referencias-bibliográficas)
10. [Metadatos del Análisis](#10-metadatos-del-análisis)

---

## 1. Fuentes de Datos Primarias

### Instituto Nacional de Estadística (INE)

#### 1.1 Encuesta de Condiciones de Vida (ECV)
- **Contenido:** Gini, S80/S20, Umbral Pobreza, Deciles Renta
- **URL:** https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176807
- **Frecuencia:** Anual (2008-2023)
- **Cobertura:** España nacional y CCAA
- **Tamaño muestral:** ~13,000 hogares/año

#### 1.2 AROPE (At Risk of Poverty or Social Exclusion)
- **Contenido:** Indicador multidimensional Eurostat
- **URL:** https://www.ine.es/ss/Satellite?L=es_ES&c=INESeccion_C&cid=1259925408327
- **Frecuencia:** Anual (2008-2023)
- **Metodología:** Regulation (EU) No 1303/2013

#### 1.3 Encuesta de Presupuestos Familiares (EPF)
- **Contenido:** Gasto por quintil y categoría ECOICOP
- **URL:** https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176806
- **Frecuencia:** Irregular (2008, 2011, 2013, 2015, 2018, 2021)
- **Nivel detalle:** 12 categorías ECOICOP nivel 1
- **Nota:** Cambio metodológico EPF 2006→2021 puede afectar comparabilidad

#### 1.4 IPC (Índice de Precios al Consumo)
- **Contenido:** IPC General y Sectorial ECOICOP
- **URL:** https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176802
- **Frecuencia:** Mensual (agregado anual usado en análisis)
- **Base:** IPC base 2016 (rebasado a 2008 para deflactación)

### Eurostat

- **AROPE metodología oficial**
- **URL:** https://ec.europa.eu/eurostat/web/income-and-living-conditions
- **Usado para:** Validación cruzada y comparativa europea

---

## 2. Metodología AROPE

### 2.1 Definición Eurostat

```
AROPE_rate = Personas en al menos UNA de estas situaciones:
  1. Pobreza monetaria (renta < 60% mediana)
  2. Carencia material severa (≥4 de 9 items)
  3. Baja intensidad laboral (adultos trabajando < 20% tiempo)
```

### 2.2 Items Carencia Material Severa

1. No poder permitirse 1 semana vacaciones al año
2. No poder permitirse comida con carne/pollo/pescado cada 2 días
3. No poder mantener vivienda con temperatura adecuada
4. No tener capacidad para afrontar gastos imprevistos
5. Retrasos en pago hipoteca/alquiler/recibos
6. No poder permitirse teléfono
7. No poder permitirse TV color
8. No poder permitirse lavadora
9. No poder permitirse coche

### 2.3 Baja Intensidad Laboral

- **Definición:** Hogares donde adultos en edad laboral (18-59 años, excluidos estudiantes) trabajaron menos del 20% del tiempo potencial durante el año anterior
- **Exclusiones:** Pensionistas, estudiantes a tiempo completo
- **Fuente:** Regulation (EU) No 1303/2013

---

## 3. Proceso de Deflactación

### 3.1 Base de Deflactación

- **Base elegida:** €2008
- **Razón:** Año pre-crisis, permite capturar todo el ciclo 2008-2023
- **IPC usado:** IPC base 2016 rebasado a 2008=100

### 3.2 Fórmula de Deflactación

```
Renta_Real_2008 = Renta_Nominal_t × (IPC_2008 / IPC_t)
```

### 3.3 Índices IPC Usados (2008=100)

| Año | IPC (2008=100) | Deflactor |
|-----|----------------|-----------|
| 2008 | 100.0 | 1.000 |
| 2014 | 106.2 | 0.942 |
| 2019 | 111.8 | 0.894 |
| 2021 | 115.4 | 0.867 |
| 2023 | 124.9 | 0.801 |

### 3.4 Validación

- ✅ Cross-check con IPC publicado INE
- ✅ Verificación manual años clave (2008, 2014, 2020, 2023)
- ✅ Comparación con series deflactadas oficiales INE

---

## 4. Trayectorias Detalladas por Fase

### 4.1 Tabla Resumen por Fases

| Fase | Período | Gini (Δ) | D1 (Δ%) | AROPE (Δpp) | Diagnóstico |
|------|---------|----------|---------|-------------|-------------|
| Pre-Crisis | 2008-2009 | -0.0008 | +1.4% | +0.9 | Estable |
| Crisis | 2010-2014 | +0.0276 | -18.1% | +4.5 | 🔴 Colapso |
| Recuperación | 2015-2019 | -0.0140 | +13.4% | -3.9 | ⚠️ Recuperación parcial |
| COVID | 2020-2021 | -0.0010 | -3.7% | +1.7 | 🔴 Retroceso |
| Post-COVID | 2022-2023 | -0.0070 | -2.1% | -0.5 | 🔴 Deterioro continuo |

### 4.2 Interpretación por Fase

**Pre-Crisis (2008-2009):**
- Gini estable (-0.08pp)
- D1 crece ligeramente (+1.4%)
- AROPE sube levemente (+0.9pp) por efectos rezagados crisis financiera 2007

**Crisis (2010-2014):**
- Gini sube (+2.76pp) por ampliación brechas
- D1 colapsa -18.1% (pérdida nunca recuperada)
- AROPE dispara +4.5pp (pico 29.2% en 2014)
- Mecanismo: Clase media pierde rentas más rápido que extremos

**Recuperación (2015-2019):**
- Gini baja (-1.40pp) por compresión distribución
- D1 recupera +13.4% pero insuficiente vs pérdida -18.1%
- AROPE baja -3.9pp pero no alcanza niveles pre-crisis
- Mecanismo: Ricos recuperan primero (capital, formación)

**COVID (2020-2021):**
- Gini estable (-0.10pp)
- D1 cae -3.7% (ERTE, cierres sectores baja cualificación)
- AROPE sube +1.7pp (pérdida empleos precarios)
- Mecanismo: Shock asimétrico sobre sectores intensivos en trabajo poco cualificado

**Post-COVID (2022-2023):**
- Gini baja -0.70pp (falsa mejora por compresión hacia abajo)
- D1 sigue cayendo -2.1% pese a recuperación empleo
- AROPE baja levemente -0.5pp (mejora empleo compensada por inflación)
- Mecanismo: Inflación diferencial erosiona poder adquisitivo pobres (gasto 40% alimentos, inflación >8%)

---

## 5. Checklist de Validación

### 5.1 Validación de Datos

| Item | Estado | Método | Fecha |
|------|--------|--------|-------|
| 1. Coherencia temporal (sin saltos irracionales) | ✅ VALIDADO | Validación automática `src.validacion` | 2025-11-18 |
| 2. Valores dentro de rangos esperados | ✅ VALIDADO | Umbrales min/max por métrica | 2025-11-18 |
| 3. Sin duplicados en datos fuente | ✅ VALIDADO | Query SQL con GROUP BY | 2025-11-18 |
| 4. Deflactación IPC correcta (base 2008) | ✅ VALIDADO | Verificación manual vs IPC publicado | 2025-11-18 |
| 5. Agregaciones EPF coinciden con INE publicado | ✅ VALIDADO | Comparación con tablas oficiales INE | 2025-11-18 |
| 6. AROPE calculado según metodología Eurostat | ✅ VALIDADO | Revisión fórmula AROPE_rate = (pobreza OR carencia OR baja_intensidad) | 2025-11-18 |
| 7. Gini replica valores oficiales INE | ✅ VALIDADO | Cross-check con INE Gini oficial | 2025-11-18 |
| 8. Sin datos faltantes en años críticos (2008, 2013, 2020, 2023) | ✅ VALIDADO | Inspección visual + alertas automáticas | 2025-11-18 |

### 5.2 Scripts de Validación

- **Ubicación:** `utils/validation_framework.py`, `utils/validation_rules.py`
- **Ejecución:** Automática en pipeline ETL (`notebooks/00_etl/02_run_validation.py`)
- **Logs:** `data/validated/logs/` (timestamp de cada validación)

---

## 6. Registro de Cambios Metodológicos

| Fecha | Cambio | Razón | Impacto Resultados |
|-------|--------|-------|-------------------|
| 2025-11-15 | División de notebook consolidado en 4 notebooks modulares | Arquitectura 3 capas (validación → análisis → reporte) | NINGUNO (reorganización código) |
| 2025-11-16 | Implementación de validación automática pre-análisis | Detectar errores datos antes de interpretación | NINGUNO (preventivo) |
| 2025-11-17 | Adición de análisis inflación diferencial por quintil | Capturar heterogeneidad impacto inflación 2022-2023 | ALTO (revela inflación regresiva) |
| 2025-11-18 | Exportación de resultados en formato Parquet para reproducibilidad | Facilitar re-análisis y trazabilidad | NINGUNO (formato almacenamiento) |

---

## 7. Limitaciones Conocidas

### 7.1 Tabla Resumen Limitaciones

| Dimensión | Limitación | Impacto | Mitigación |
|-----------|------------|---------|------------|
| **Datos** | EPF Gasto Quintil: frecuencia irregular (cada 2-3 años) | MEDIO - Interpolación necesaria para años sin datos | Usar años EPF reales (2008, 2011, 2013, 2015, 2018, 2021) |
| **Datos** | IPC Sectorial ECOICOP: categorías limitadas (12 grupos) | BAJO - 12 categorías cubren ~95% gasto | Suficiente para análisis diferencial comparativo |
| **Metodología** | Inflación diferencial: mapeo EPF→ECOICOP imperfecto | BAJO - Validado con agregado nacional | Cross-check con IPC nacional ponderado |
| **Metodología** | Umbral pobreza: calculado como 60% mediana (no canasta básica) | MEDIO - Umbral relativo vs absoluto | Análisis separado umbral nominal vs real |
| **Interpretación** | Gini: no captura movilidad intergeneracional | BAJO - Complementado con AROPE y D1 | Análisis multidimensional (Gini + D1 + AROPE + S80/S20) |
| **Alcance** | Análisis: solo España nacional (sin desagregación CCAA) | ALTO - Heterogeneidad regional oculta | Análisis regional en notebooks separados |

### 7.2 Limitaciones No Resueltas

1. **Microdatos ECV no accesibles:** Imposibilita cálculo propio Gini y bootstrap CIs
2. **IPC específico por quintil no disponible:** Requiere construcción manual con EPF+ECOICOP
3. **Cambio metodológico EPF 2006→2021:** Puede introducir discontinuidad en series gasto
4. **Datos panel ECV restringidos:** Imposibilita análisis movilidad intergeneracional

---

## 8. Supuestos Críticos

### 8.1 Supuestos Asumidos

#### 1. Deflactación con IPC (base 2008)

- **Supuesto:** IPC refleja inflación experimentada por todos los quintiles
- **Realidad:** Inflación diferencial existe (demostrado en notebook 03_analisis_inflacion_diferencial.ipynb)
- **Consecuencia:** Rentas reales de pobres **sobrestimadas** (inflación real > IPC)
- **Magnitud error:** ~0.5pp anual subestimación empobrecimiento real
- **Mitigación:** Análisis inflación diferencial separado en sección 3

#### 2. Umbral pobreza como 60% mediana

- **Supuesto:** Pobreza es relativa al nivel de vida mediano
- **Alternativa:** Canasta básica absoluta (no disponible en INE)
- **Consecuencia:** Si toda economía se empobrece, umbral baja → menos "pobres" estadísticos
- **Mitigación:** Análisis umbral real (€2008) revela empobrecimiento absoluto
- **Ejemplo:** Umbral real 2023 (€8,643) es -5.4% vs 2008 (€9,141)

#### 3. AROPE = pobreza OR carencia OR baja_intensidad

- **Supuesto:** Exclusión social es multidimensional (no solo renta)
- **Fortaleza:** Metodología Eurostat validada internacionalmente
- **Consecuencia:** Captura vulnerabilidad mejor que Gini
- **Nota:** AROPE puede subir aunque Gini baje (crisis 2008-2014)

#### 4. Mapeo EPF → ECOICOP

- **Supuesto:** 12 categorías ECOICOP representan distribución gasto
- **Validación:** Cobertura ~95% del gasto total
- **Limitación:** Subcategorías (ej. alimentos específicos) no capturadas
- **Mitigación:** Análisis a nivel agregado (inflación general por quintil)

### 8.2 Trade-offs Metodológicos

| Decisión | Alternativa | Razón de Elección |
|----------|-------------|-------------------|
| Usar Gini oficial INE | Calcular Gini desde microdatos | Trazabilidad + comparabilidad internacional |
| IPC general para deflactar | IPC específico por quintil | No disponible para serie completa 2008-2023 |
| Umbral 60% mediana | Canasta básica absoluta | Estándar europeo (AROPE) + disponibilidad datos |
| Análisis nacional | Desagregación CCAA | Enfoque inicial (regional en notebooks separados) |

### 8.3 Impacto en Conclusiones

#### Conclusiones ROBUSTAS (no afectadas por limitaciones)

- ✅ Paradoja Gini vs D1 (confirmada con múltiples métricas)
- ✅ Empobrecimiento absoluto 2008-2023 (umbral real confirma)
- ✅ COVID no superado (AROPE 2023 > 2019)

#### Conclusiones MATIZADAS (afectadas moderadamente)

- ⚠️ Magnitud exacta empobrecimiento D1 (inflación diferencial sugiere infraestimación ~0.5pp/año)
- ⚠️ Comparación 2008 vs 2023 (cambio metodológico EPF 2006→2021 puede afectar ~1-2%)

#### Conclusiones NO AFIRMADAS (datos insuficientes)

- ❌ Movilidad intergeneracional (requiere datos panel)
- ❌ Causalidad específica (análisis correlacional, no causal)
- ❌ Heterogeneidad regional (requiere análisis CCAA separado)

---

## 9. Referencias Bibliográficas

### 9.1 Estudios Comparables

1. **Ayala, L. & Paniagua, M. (2019).**  
   *"The Evolution of Income Inequality in Spain: 2008-2014."*  
   Revista de Economía Aplicada, 27(80), 5-34.
   - **Relevancia:** Análisis período crisis 2008-2014 con mismas fuentes INE
   - **Coincidencia:** Confirma colapso D1 -18% durante crisis

2. **Cantó, O., Gradín, C., & Del Río, C. (2020).**  
   *"Pobreza y desigualdad en España tras la Gran Recesión."*  
   Fundación FOESSA.
   - **Relevancia:** Análisis multidimensional pobreza incluyendo AROPE
   - **Coincidencia:** Identifica recuperación insuficiente 2015-2019

3. **OECD (2023).**  
   *"Income Inequality (indicator)."*  
   DOI: 10.1787/459aa7f1-en
   - **Relevancia:** Comparativa internacional Gini
   - **Uso:** Contextualización España en OCDE

4. **Eurostat (2024).**  
   *"Living conditions in Europe - poverty and social exclusion."*  
   Luxembourg: Publications Office of the European Union.
   - **Relevancia:** Metodología oficial AROPE
   - **Uso:** Validación cálculos AROPE España

### 9.2 Metodología Gini

- **Cowell, F. A. (2011).** *Measuring Inequality*. Oxford University Press.
  - Capítulo 3: "The Lorenz Curve and the Gini Coefficient"
  
- **Sen, A. (1997).** *On Economic Inequality*. Clarendon Press.
  - Capítulo 2: "Inequality, Poverty and Welfare"

### 9.3 Inflación Diferencial

- **Crossley, T. F., & O'Dea, C. (2010).**  
  *"The Design and Implementation of a Household Inflation Index."* IFS Working Papers.
  - **Relevancia:** Metodología construcción IPC específico por quintil

- **Hobijn, B., & Lagakos, D. (2005).**  
  *"Inflation Inequality in the United States."* Review of Income and Wealth, 51(4), 581-606.
  - **Relevancia:** Evidencia empírica inflación diferencial por nivel renta

### 9.4 Metodología AROPE

- **Regulation (EU) No 1303/2013** of the European Parliament and of the Council.
  - Annex II: Common indicators for the European Social Fund
  - **URL:** https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013R1303

---

## 10. Metadatos del Análisis

### 10.1 Información General

- **Proyecto:** Desigualdad-Espana
- **Autor:** databamario
- **Repositorio:** https://github.com/databamario/Desigualdad-Espana
- **Fecha último análisis:** 2025-11-20
- **Versión Python:** 3.11.4
- **Entorno:** Virtual environment (`desigualdad/`)

### 10.2 Notebooks Utilizados

1. **00_etl/01_run_etl.py** - Pipeline ETL automático
2. **00_etl/02_run_validation.py** - Validación automática datos
3. **01_analisis_nacional/02_analisis_desigualdad_consolidado.ipynb** - Análisis nacional completo
4. **02_analisis_regional/05_analisis_geografico_ccaa_CONSOLIDADO.ipynb** - Análisis CCAA
5. **03_comparativa_europa/07_comparativa_europea_CONSOLIDADO.ipynb** - Comparativa UE27
6. **01_analisis_nacional/99_reporte_final.ipynb** - Reporte ejecutivo

### 10.3 Dependencias Principales

```python
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
sqlalchemy==2.0.19
pyodbc==4.0.39
openpyxl==3.1.2
```

### 10.4 Periodo de Análisis

- **Inicio:** 2008 (pre-crisis)
- **Fin:** 2023 (último dato disponible INE)
- **Total años:** 16 años
- **Años clave:** 2008 (pre-crisis), 2014 (pico crisis), 2019 (pre-COVID), 2023 (actual)

### 10.5 Base de Deflactación

- **Base:** €2008
- **IPC:** IPC base 2016 rebasado a 2008=100
- **Fuente:** INE - IPC Nacional

### 10.6 Estructura Base de Datos

- **Motor:** SQL Server (MSSQL)
- **Tablas:** 28+ tablas (INE + Eurostat)
- **Schema:** `dbo.INE_*`, `dbo.EUROSTAT_*`
- **Ubicación:** Local (`localhost`)

### 10.7 Archivos de Salida

- **Formato:** Parquet (reproducibilidad), CSV (legibilidad), Excel (presentación)
- **Ubicación:** `outputs/tablas/`, `outputs/figuras/`, `outputs/pickle_cache/`

### 10.8 Scripts de Validación

- **Framework:** `utils/validation_framework.py`
- **Reglas:** `utils/validation_rules.py`
- **Logs:** `data/validated/logs/`

---

## 📝 Notas Finales

Este documento técnico complementa el **Reporte Ejecutivo** (`99_reporte_final.ipynb`). 

**Para detalles técnicos adicionales, consultar:**
- Notebooks en `notebooks/01_analisis_nacional/`
- Scripts validación en `utils/`
- Documentación arquitectura en `docs/ARQUITECTURA.md`
- Diccionario datos en `docs/DICCIONARIO_DATOS.md`

**Para análisis futuros recomendados:**
- Desagregación regional (CCAA) - `notebooks/02_analisis_regional/`
- Comparativa europea - `notebooks/03_comparativa_europa/`
- Análisis sociodemográfico (edad, sexo, educación)
- Modelización econométrica panel

---

*Última actualización: 2025-11-20*
