# Informe de Coherencia Analítica
## Proyecto: Desigualdad Social en España - Pipeline ETL

**Fecha:** 19 de noviembre de 2025  
**Autor:** Análisis de Coherencia de Datos y Resultados  

---

## 📋 Resumen Ejecutivo

Este informe evalúa la **coherencia analítica** del proyecto, centrándose en la calidad de los datos, la validez de las conclusiones y las limitaciones metodológicas. Se han identificado 7 áreas clave de evaluación.

---

## 1️⃣ Inflación Sectorial (INE_IPC_Sectorial_ECOICOP) - ✅ RESUELTO

### Estado
**RESUELTO** - No requiere acción correctiva

### Hallazgos
- **Missingness reportado:** 75% en logs de validación
- **Missingness real:** 25% (312 de 1248 registros)
- **Causa:** Interpretación incorrecta de la estructura de datos

### Explicación Técnica
El INE proporciona IPC sectorial con **4 tipos de métricas**:

| Tipo de Métrica | Registros | Nulls en Inflacion_Sectorial_% | % Nulls |
|----------------|-----------|-------------------------------|---------|
| Variación anual | 312 | 0 | 0% |
| Variación mensual | 312 | 0 | 0% |
| Variación en lo que va de año | 312 | 0 | 0% |
| **Índice** | **312** | **312** | **100%** |
| **TOTAL** | **1248** | **312** | **25%** |

- El tipo "Índice" contiene valores base (ej: 67.2, 69.9) sin inflación calculada
- Los tipos "Variación" contienen las tasas de inflación directamente publicadas por INE
- Esto es **metodológicamente correcto** - INE no calcula inflación desde índices base

### Impacto en Análisis
**NINGUNO** ✅

El notebook `03_analisis_inflacion_diferencial.ipynb` filtra correctamente:
```python
df_ipc_clean = df_ipc_temp[df_ipc_temp[metric_col].astype(str) == 'Variación anual'].copy()
```

Esto garantiza que solo se usan registros con inflación calculada (0% nulls).

### Recomendaciones
1. ✅ **Documentar** en `DICCIONARIO_DATOS.md`:
   ```markdown
   **Nota:** 25% de registros (tipo "Índice") no contienen Inflacion_Sectorial_% 
   por diseño metodológico del INE. El análisis utiliza únicamente "Variación anual".
   ```

2. ✅ **Actualizar** log de validación para reportar:
   ```
   Inflacion_Sectorial_%: 0% nulls en registros de Variación anual (936/936)
   Inflacion_Sectorial_%: 100% nulls en registros de Índice (312/312) - ESPERADO
   ```

---

## 2️⃣ Escala e Interpretación de Gini - ⚠️ VERIFICACIÓN PARCIAL

### Estado
**REQUIERE AUDITORÍA** de textos y visualizaciones

### Hallazgos
- ✅ ETL normaliza correctamente 0-100 → 0-1 cuando detecta valores > 1.1
- ✅ Notebooks de análisis usan escala 0-1 en cálculos
- ⚠️ **Inconsistencia potencial** en tabla de comparativa europea:
  ```
  | Gini | ~33-34 | ~30-31 | +3pp | ⚠️ MÁS desigualdad |
  ```
  Esto sugiere mezcla de escalas (¿0-1 vs 0-100?)

### Ejemplos de Uso Correcto
```python
# 03_analisis_inflacion_diferencial.ipynb
gini_2019 = 0.330  # ✅ Escala 0-1
gini_2023 = 0.315  # ✅ Escala 0-1

# Visualizaciones
ax.set_ylabel('Coeficiente de Gini')  # ✅ Sin escala explícita
```

### Impacto en Conclusiones
- **MEDIO** - Confusión en interpretación de magnitudes
- Si "Gini = 33" se lee como 33% (incorrecto) vs 0.33 (correcto), las conclusiones sobre desigualdad relativa cambian

### Recomendaciones
1. 🔍 **Auditar** `07_comparativa_europea_CONSOLIDADO.ipynb`:
   - Verificar todas las celdas con valores Gini
   - Confirmar que tabla de resumen usa escala 0-1

2. 📊 **Estandarizar etiquetas** en visualizaciones:
   ```python
   ax.set_ylabel('Coeficiente de Gini (0=igualdad, 1=desigualdad máxima)')
   ```

3. 📝 **Añadir nota** en celdas markdown:
   ```markdown
   **Nota de escala:** Todos los valores Gini en este análisis usan escala 0-1.
   Un valor de 0.33 indica desigualdad moderada-alta.
   ```

---

## 3️⃣ Valores Nominales vs Reales y Deflación - ⚠️ SIN DOCUMENTAR

### Estado
**REQUIERE DOCUMENTACIÓN Y VALIDACIÓN**

### Hallazgos
- ✅ Pipeline incluye `INE_IPC_General` (base 2021=100) como deflactor potencial
- ❓ **No se identificó documentación explícita** del proceso de deflación
- ❓ **No confirmado** si comparaciones monetarias multi-temporales usan valores reales

### Variables que Requieren Deflación
1. **Renta media por decil** (`INE_Renta_Decil`)
2. **Umbral de pobreza** (`INE_Umbral_Pobreza_Hogar`) - en euros/año
3. **Gasto medio por hogar** (`INE_EPF_Gasto`) - EPF

### Impacto en Conclusiones
- **ALTO** - Comparaciones incorrectas de poder adquisitivo
- Si se comparan euros nominales de 2008 vs 2023, se subestima la pérdida de poder adquisitivo real
- Inflación acumulada 2008-2023 ≈ 25%, lo cual distorsiona tendencias monetarias

### Recomendaciones
1. 🔍 **Buscar** en notebooks de análisis:
   ```python
   grep -r "IPC_General\|deflat\|nominal\|real" notebooks/01_analisis_nacional/
   ```

2. 📝 **Documentar** en `RESUMEN_TRANSFORMACION.md`:
   ```markdown
   ## Deflación de Variables Monetarias
   
   ### Variables Deflactadas
   - Renta media por decil: Convertida a euros constantes base 2021
   - Umbral de pobreza: Convertido a euros constantes base 2021
   - Gasto EPF: Convertido a euros constantes base 2021
   
   ### Deflactor Utilizado
   - Fuente: INE_IPC_General (Tabla 24077)
   - Base: 2021 = 100
   - Fórmula: `valor_real_2021 = valor_nominal * (100 / IPC_año)`
   ```

3. ✅ **Validar** que gráficos temporales de variables monetarias usen valores reales:
   ```python
   # Ejemplo de validación
   assert 'euros constantes 2021' in ax.get_ylabel(), "Variable monetaria debe estar deflactada"
   ```

---

## 4️⃣ Alineación Temporal y Resolución - ⚠️ REQUIERE VALIDACIÓN

### Estado
**REQUIERE VERIFICACIÓN** de consistencia en agregaciones temporales

### Hallazgos Potenciales
- IPC sectorial: Datos **mensuales** agregados a **anuales** (promedio)
- AROPE, Gini: Datos nativamente **anuales**
- EPF: **Bienal** (cada 2 años) con interpolación potencial

### Riesgos de Inconsistencia
1. **Años publicación desfasados:** EPF publicada en 2023 puede contener datos de 2022
2. **Agregación mensual → anual:** ¿Promedio simple o ponderado?
3. **Cambios metodológicos:** ¿Se documentan breaks en series temporales?

### Impacto en Conclusiones
- **MEDIO** - Comparaciones incorrectas año-a-año
- Si EPF 2023 es realmente 2022, comparaciones con AROPE 2023 son inválidas

### Recomendaciones
1. 🔍 **Verificar cobertura temporal** por dataset:
   ```python
   for df_name, df in datasets.items():
       print(f"{df_name}: {df['Anio'].min()} - {df['Anio'].max()}")
       print(f"  Años únicos: {sorted(df['Anio'].unique())}")
   ```

2. 📝 **Documentar** en `DICCIONARIO_DATOS.md`:
   ```markdown
   ### Notas de Cobertura Temporal
   
   | Dataset | Años Disponibles | Frecuencia | Notas |
   |---------|------------------|------------|-------|
   | AROPE | 2008-2023 | Anual | Publicación año n contiene datos año n |
   | EPF | 2006-2023 | Bienal | Publicación año n puede contener datos año n-1 |
   | IPC Sectorial | 2002-2025 | Mensual → Anual | Agregado como promedio simple mensual |
   ```

3. ⚠️ **Añadir caveats** en conclusiones que comparan datasets con diferentes resoluciones:
   ```markdown
   **Limitación:** La comparación entre EPF (bienal) y AROPE (anual) 
   asume interpolación lineal para años intermedios.
   ```

---

## 5️⃣ Codificación de Nombres de Columnas - 🔴 CRÍTICO

### Estado
**CRÍTICO** - Corrupción de encoding detectada

### Hallazgos
Al inspeccionar pickles generados:
```python
Columns: ['A�o', 'Categoria_ECOICOP', 'Tipo_Metrica', 'IPC_Indice', 'Inflacion_Sectorial_%']
#         ^^^^^ CORRUPCIÓN - debería ser 'Año'
```

### Causa Raíz
- Windows pickle serialization con UTF-8 → lectura con cp1252 causa `Año` → `A�o`
- Notebooks usan `'Año'` en extracciones pero pickle corrompe en I/O

### Impacto en Análisis
- **CRÍTICO** - Potenciales fallos silenciosos en joins
- Si un notebook espera `'Año'` pero pickle tiene `'A�o'`, los joins devuelven 0 registros
- Los análisis podrían ejecutarse sin error pero con resultados vacíos

### Solución Recomendada
**Opción 1: Nombres ASCII-Safe (RECOMENDADO)**

Reemplazar `'Año'` → `'Anio'` en todas las extracciones:

```python
# En 01a_extract_transform_INE.ipynb
# ANTES:
registros.append({'Año': int(year), 'Valor': valor})

# DESPUÉS:
registros.append({'Anio': int(year), 'Valor': valor})
```

**Ventajas:**
- ✅ Compatible con cualquier encoding
- ✅ No requiere configuración especial de environment
- ✅ Portable entre Windows/Linux/Mac

**Opción 2: Forzar UTF-8 en Pickle**

```python
# Al guardar
with open(ruta, 'wb') as f:
    pickle.dump(df, f, protocol=pickle.HIGHEST_PROTOCOL)

# Al cargar
with open(ruta, 'rb') as f:
    df = pickle.load(f, encoding='utf-8')
```

**Desventajas:**
- ⚠️ Requiere modificar TODOS los puntos de carga
- ⚠️ Frágil ante cambios de environment

### Implementación
1. 🔧 **Reemplazar globalmente** en `01a_extract_transform_INE.ipynb`:
   - `'Año':` → `'Anio':`
   - `.groupby('Año'` → `.groupby('Anio'`
   - `['Año']` → `['Anio']`

2. 🔧 **Actualizar** notebooks de análisis:
   ```python
   # ANTES:
   df = pd.read_sql("SELECT * FROM INE_IPC_Sectorial_ECOICOP", engine)
   df_2020 = df[df['Año'] == 2020]  # ❌ Falla si columna es 'A�o'
   
   # DESPUÉS:
   df = pd.read_sql("SELECT * FROM INE_IPC_Sectorial_ECOICOP", engine)
   df_2020 = df[df['Anio'] == 2020]  # ✅ Funciona siempre
   ```

3. 🔧 **Actualizar SQL** table schemas:
   ```sql
   ALTER TABLE INE_IPC_Sectorial_ECOICOP 
   RENAME COLUMN [Año] TO [Anio];
   ```

---

## 6️⃣ Cuantificación de Incertidumbre - ⚠️ AUSENTE

### Estado
**NO IMPLEMENTADO** - Sin intervalos de confianza ni errores estándar

### Hallazgos
- Gini, S80/S20, AROPE: **Estimaciones puntuales sin IC**
- No se proporciona información sobre:
  - Tamaño de muestra (ECV/EPF)
  - Error muestral
  - Intervalos de confianza al 95%

### Impacto en Conclusiones
- **ALTO** - Imposible distinguir cambios significativos de ruido estadístico
- Ejemplo: 
  - ¿Gini 2022=0.330 vs 2023=0.315 es cambio real o fluctuación muestral?
  - Sin IC, no podemos afirmar "la desigualdad disminuyó significativamente"

### Diferencias Potencialmente No Significativas
```python
# Ejemplo de magnitudes pequeñas sin contexto estadístico
gini_2019 = 0.330
gini_2023 = 0.315
diff = -0.015  # -1.5 pp

# ¿Es significativo? Depende del error estándar:
# - Si SE = 0.005 → diff = -3.0 * SE → SIGNIFICATIVO (p<0.01)
# - Si SE = 0.010 → diff = -1.5 * SE → MARGINAL (p≈0.13)
# - Si SE = 0.020 → diff = -0.75 * SE → NO SIGNIFICATIVO (p>0.4)
```

### Recomendaciones
1. 📊 **Solicitar a INE/EUROSTAT:**
   - Errores estándar de Gini, S80/S20
   - Intervalos de confianza al 95%
   - Tamaños de muestra efectivos

2. 📝 **Documentar limitaciones** en conclusiones:
   ```markdown
   ### Limitación Estadística
   
   Los indicadores de desigualdad (Gini, S80/S20, AROPE) son estimaciones 
   muestrales de la Encuesta de Condiciones de Vida (ECV). El INE no publica 
   intervalos de confianza, por lo que:
   
   - **Cambios < 0.02 en Gini**: Considerar como fluctuación potencial
   - **Cambios < 1 pp en AROPE**: Requieren verificación multi-anual
   - **Comparaciones regionales**: Muestra CCAA pequeñas tiene mayor varianza
   
   **Recomendación:** Interpretar tendencias plurianuales en lugar de 
   diferencias año-a-año aisladas.
   ```

3. 📊 **Añadir análisis de sensibilidad:**
   ```python
   # Pseudo-código
   def sensitivity_analysis(series, assumed_se=0.01):
       """Simula IC asumiendo error estándar conservador"""
       ci_lower = series - 1.96 * assumed_se
       ci_upper = series + 1.96 * assumed_se
       return ci_lower, ci_upper
   
   # Visualizar con bandas de incertidumbre
   ax.fill_between(years, gini_lower, gini_upper, alpha=0.3, 
                    label='IC 95% estimado (SE≈0.01)')
   ```

---

## 7️⃣ Proveniencia de Datos y Cambios Metodológicos - ⚠️ SIN DOCUMENTAR

### Estado
**NO DOCUMENTADO** - Potenciales breaks en series temporales

### Cambios Metodológicos Conocidos de INE/EUROSTAT
#### IPC
- **2016:** Cambio de base 2011 → 2016
- **2021:** Cambio de base 2016 → 2021 (**ACTUAL**)
- **COVID-19:** Ajustes metodológicos 2020-2021 (ponderaciones)

#### Encuesta de Condiciones de Vida (ECV)
- **2013:** Armonización EU-SILC completa
- **2020:** Cambios en recogida de datos (COVID-19)

#### EPF
- **2006:** Nueva metodología COICOP
- **Bienal:** Cambio de continua → bienal en algunos períodos

### Impacto en Conclusiones
- **MEDIO-ALTO** - Tendencias aparentes pueden ser artefactos metodológicos
- Ejemplo: Salto en Gini 2013 puede deberse a cambio metodológico ECV, no a cambio real

### Recomendaciones
1. 📚 **Consultar metodología INE:**
   - [Metodología IPC Base 2021](https://www.ine.es/metodologia/t25/principales_caracteristicas_base_2021.pdf)
   - [Informe metodológico ECV](https://www.ine.es/dynt3/metadatos/es/RespuestaDatos.html?oe=30453)

2. 📝 **Documentar breaks** en `DICCIONARIO_DATOS.md`:
   ```markdown
   ### Cambios Metodológicos y Breaks en Series
   
   | Dataset | Año | Tipo de Cambio | Impacto |
   |---------|-----|----------------|---------|
   | IPC General | 2021 | Cambio base 2016→2021 | Series enlazadas automáticamente |
   | ECV (Gini/AROPE) | 2013 | Armonización EU-SILC | Posible discontinuidad en niveles |
   | ECV | 2020 | Recogida COVID-19 | Mayor incertidumbre 2020-2021 |
   | EPF | 2006 | Metodología COICOP | No comparable pre-2006 |
   ```

3. ⚠️ **Añadir notas** en visualizaciones con breaks:
   ```python
   # Marcar cambio metodológico en gráfico
   ax.axvline(x=2013, color='red', linestyle='--', alpha=0.5, 
              label='Cambio metodológico ECV 2013')
   ax.annotate('⚠️ Posible break', xy=(2013, max_value), 
               xytext=(2013, max_value*1.1), fontsize=8)
   ```

---

## 📊 Matriz de Priorización

| Issue | Impacto | Urgencia | Esfuerzo | Prioridad |
|-------|---------|----------|----------|-----------|
| 5. Encoding columnas | 🔴 CRÍTICO | Alta | Medio | **P0** |
| 6. Incertidumbre | 🟠 Alto | Media | Alto | **P1** |
| 3. Deflación | 🟠 Alto | Media | Bajo | **P1** |
| 7. Proveniencia | 🟡 Medio | Media | Bajo | **P2** |
| 2. Escala Gini | 🟡 Medio | Baja | Bajo | **P2** |
| 4. Alineación temporal | 🟡 Medio | Baja | Medio | **P3** |
| 1. IPC sectorial | ✅ Resuelto | N/A | N/A | **P4** |

---

## 🎯 Plan de Acción Recomendado

### Fase 1: Correcciones Críticas (Esta semana)
1. ✅ **Fix encoding:** Migrar `'Año'` → `'Anio'` en ETL + notebooks + SQL
2. 📝 **Documentar deflación:** Verificar + documentar proceso en `RESUMEN_TRANSFORMACION.md`

### Fase 2: Mejoras de Calidad (Próximas 2 semanas)
3. 📊 **Añadir caveats de incertidumbre:** Actualizar conclusiones con limitaciones estadísticas
4. 📚 **Documentar breaks metodológicos:** Completar `DICCIONARIO_DATOS.md` con cambios INE/EUROSTAT

### Fase 3: Validación Completa (Próximo mes)
5. ✅ **Auditar Gini escala:** Revisar todas las referencias en notebooks de análisis
6. 🔍 **Validar alineación temporal:** Verificar consistencia agregaciones mensuales→anuales

---

## 📈 Nivel de Confianza en Conclusiones Actuales

### Alta Confianza ✅
- **Tendencias plurianuales Gini/AROPE:** Series largas (2008-2023) con metodología estable post-2013
- **Inflación diferencial por quintil:** Metodología sólida, datos completos EPF + IPC sectorial

### Confianza Media ⚠️
- **Diferencias año-a-año pequeñas (<0.02 Gini):** Sin IC, podrían ser ruido muestral
- **Comparaciones monetarias multi-temporales:** Requiere verificar deflación aplicada

### Baja Confianza 🔴
- **Comparaciones pre/post 2013 (ECV):** Posible break metodológico no documentado
- **Conclusiones basadas en años únicos 2020-2021:** Mayor incertidumbre por COVID-19

---

## 📝 Conclusión

El proyecto presenta una **coherencia técnica sólida** en cuanto a pipeline ETL y procesamiento de datos. Sin embargo, la **coherencia analítica** requiere mejoras en:

1. **Documentación de limitaciones:** Explicitar incertidumbre y breaks metodológicos
2. **Estandarización de encoding:** Evitar corrupciones silenciosas en nombres de columnas
3. **Trazabilidad metodológica:** Documentar deflación, agregaciones y fuentes de error

**Recomendación final:** Implementar Fase 1 (encoding + deflación) antes de presentar resultados a stakeholders externos. Las conclusiones actuales son **válidas pero requieren caveats** sobre incertidumbre estadística.
