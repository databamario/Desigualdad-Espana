# 📋 Plantilla para Notebooks de Análisis

**Propósito:** Esta plantilla define la estructura estándar para todos los notebooks de análisis del proyecto. Úsala como base para crear nuevos análisis.

---

## 📝 Estructura Estándar de un Notebook de Análisis

```markdown
# [Título del Análisis] - [Ámbito: Nacional/Regional/Europeo]

**Nombre del archivo:** `XX_nombre_descriptivo.ipynb`  
**Objetivo:** [Descripción concisa del análisis - 1-2 frases]  
**Fuentes de datos:** [Tablas utilizadas, ej: INE_Gini_S80S20_CCAA, EUROSTAT_AROP_Espana]  
**Fecha de creación:** YYYY-MM-DD  
**Autor:** Mario (databamario)  

**Contexto:** [1-2 párrafos explicando por qué este análisis es relevante, qué pregunta intenta responder]

**Hipótesis/Preguntas de investigación:**
1. [Pregunta 1]
2. [Pregunta 2]
3. [etc.]

---

## 1. Configuración y Carga de Datos

[Importar librerías, conectar a BD, cargar tablas necesarias]

---

## 2. Preparación y Limpieza

[Filtrar, agregar, transformar datos según sea necesario. Documentar decisiones metodológicas]

---

## 3. Análisis Exploratorio

[Estadísticas descriptivas, distribuciones, tendencias temporales]

---

## 4. Análisis Principal

[Análisis detallado según objetivos: correlaciones, regresiones, comparaciones, etc.]

---

## 5. Visualizaciones

[Gráficos clave: evolución temporal, comparaciones geográficas, distribuciones]

---

## 6. Hallazgos y Conclusiones

### Principales hallazgos:
1. [Hallazgo 1 con evidencia numérica]
2. [Hallazgo 2 con evidencia numérica]
3. [etc.]

### Limitaciones:
- [Limitación metodológica 1]
- [Limitación de datos 1]

### Próximos pasos:
- [Análisis complementario sugerido]
- [Profundización en aspecto X]

---

## 7. Referencias

- [Referencias bibliográficas relevantes]
- [Enlaces a documentación técnica]

---
```

---

## 📌 Ejemplo Concreto: Análisis de Evolución del Gini 2008-2023

### Celda 1 (Markdown) - Cabecera:
```markdown
# Evolución de la Desigualdad en España (2008-2023) - Análisis Nacional

**Nombre del archivo:** `01_evolucion_gini_nacional.ipynb`  
**Objetivo:** Analizar la evolución del índice de Gini en España durante el periodo 2008-2023, identificando puntos de inflexión y relación con crisis económicas  
**Fuentes de datos:** INE_Gini_S80S20_CCAA (Total Nacional), EUROSTAT_Gini_Espana, INE_IPC_General  
**Fecha de creación:** 2025-11-16  
**Autor:** Mario (databamario)  

**Contexto:** La desigualdad de ingresos en España ha experimentado variaciones significativas en las últimas décadas, especialmente durante la crisis financiera de 2008 y la pandemia de COVID-19. El índice de Gini es el indicador más utilizado internacionalmente para medir desigualdad.

**Hipótesis/Preguntas de investigación:**
1. ¿El Gini aumentó durante la crisis financiera 2008-2013?
2. ¿La recuperación económica 2014-2019 redujo la desigualdad?
3. ¿Cómo impactó la pandemia (2020-2021) en la desigualdad?
4. ¿España converge o diverge respecto a la media UE27?

---
```

### Celda 2 (Code) - Configuración:
```python
# 1. CONFIGURACIÓN Y CARGA DE DATOS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc
import sys

# Configuración estética
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Añadir utils al path
sys.path.append('../../')
from utils.config import DB_CONNECTION_STRING

# Conexión a SQL Server
conn = pyodbc.connect(DB_CONNECTION_STRING)

# Cargar datos
df_gini_ine = pd.read_sql("""
    SELECT Año, Gini 
    FROM INE_Gini_S80S20_CCAA 
    WHERE Territorio = 'Total Nacional'
    ORDER BY Año
""", conn)

df_gini_eurostat = pd.read_sql("""
    SELECT Año, Gini 
    FROM EUROSTAT_Gini_Espana 
    WHERE geo_code = 'ES'
    ORDER BY Año
""", conn)

df_gini_ue27 = pd.read_sql("""
    SELECT Año, Gini 
    FROM EUROSTAT_Gini_UE27 
    WHERE geo_code = 'EU27_2020'
    ORDER BY Año
""", conn)

print(f"✅ Datos cargados: INE ({len(df_gini_ine)} años), EUROSTAT ES ({len(df_gini_eurostat)} años), UE27 ({len(df_gini_ue27)} años)")
```

### Celda 3 (Markdown) - Sección Análisis:
```markdown
---

## 2. Preparación y Limpieza

Validamos coherencia INE-EUROSTAT y preparamos dataset unificado.

---
```

### Celda 4 (Code) - Validación:
```python
# 2. PREPARACIÓN Y LIMPIEZA

# Merge INE y EUROSTAT para validar coherencia
df_validacion = pd.merge(
    df_gini_ine, 
    df_gini_eurostat, 
    on='Año', 
    how='inner', 
    suffixes=('_INE', '_EUROSTAT')
)

df_validacion['Diferencia'] = df_validacion['Gini_INE'] - df_validacion['Gini_EUROSTAT']
df_validacion['Dif_Pct'] = (df_validacion['Diferencia'] / df_validacion['Gini_INE']) * 100

print("📊 Validación coherencia INE vs EUROSTAT:")
print(df_validacion[['Año', 'Gini_INE', 'Gini_EUROSTAT', 'Dif_Pct']])
print(f"\n✅ Diferencia máxima: {df_validacion['Dif_Pct'].abs().max():.2f}%")

# Decisión metodológica: usar INE (serie más larga)
df_gini = df_gini_ine.copy()
df_gini = df_gini.rename(columns={'Gini': 'Gini_ES'})
```

### Celda 5 (Code) - Visualización Principal:
```python
# 5. VISUALIZACIONES

fig, ax = plt.subplots(figsize=(14, 7))

# Gini España
ax.plot(df_gini['Año'], df_gini['Gini_ES'], 
        marker='o', linewidth=2.5, markersize=6, 
        label='España (INE)', color='#d62728', zorder=3)

# Gini UE27 (para comparación)
ax.plot(df_gini_ue27['Año'], df_gini_ue27['Gini'], 
        marker='s', linewidth=2, markersize=5, 
        label='UE27 (EUROSTAT)', color='#1f77b4', alpha=0.7, linestyle='--')

# Marcadores de crisis
ax.axvspan(2008, 2013, alpha=0.2, color='red', label='Crisis Financiera')
ax.axvspan(2020, 2021, alpha=0.2, color='orange', label='COVID-19')

# Estética
ax.set_xlabel('Año', fontsize=12)
ax.set_ylabel('Índice de Gini', fontsize=12)
ax.set_title('Evolución del Índice de Gini: España vs UE27 (2008-2023)', 
             fontsize=14, fontweight='bold')
ax.legend(loc='best')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('../../outputs/figuras/gini_evolucion_espana_ue27.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Gráfico guardado en outputs/figuras/")
```

### Celda 6 (Markdown) - Conclusiones:
```markdown
---

## 6. Hallazgos y Conclusiones

### Principales hallazgos:

1. **Aumento durante la crisis (2008-2013):** El Gini pasó de 31.9 (2008) a 34.0 (2014), un incremento del 6.6%. La desigualdad aumentó significativamente durante la crisis financiera.

2. **Reducción en la recuperación (2014-2019):** Descenso gradual hasta 33.0 (2019), reducción del 2.9%. La recuperación económica no eliminó completamente el aumento de desigualdad de la crisis.

3. **Impacto limitado de COVID-19:** Ligero repunte a 33.2 (2020-2021), pero menor al esperado. Las políticas de protección social (ERTE, IMV) mitigaron el impacto en desigualdad.

4. **Convergencia con UE27:** España pasó de estar 1.5 puntos por encima de UE27 (2008) a solo 0.8 puntos (2023). Proceso de convergencia lento pero sostenido.

### Limitaciones:

- **Metodológica:** Cambios en la base del IPC pueden afectar comparabilidad intertemporal
- **Datos:** EUROSTAT solo disponible desde 2010, no permite validar serie completa
- **Causalidad:** El análisis es descriptivo, no establece relaciones causales con políticas específicas

### Próximos pasos:

- Analizar desagregación por CCAA para identificar heterogeneidad regional
- Correlacionar con tasa de desempleo y PIB per cápita
- Comparar con otros indicadores (S80/S20, brecha de pobreza)

---

## 7. Referencias

- INE (2024). Encuesta de Condiciones de Vida. https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176807
- EUROSTAT (2024). EU-SILC. https://ec.europa.eu/eurostat/web/income-and-living-conditions
- OECD (2023). Income Inequality (indicator). doi: 10.1787/459aa7f1-en

---
```

---

## ✅ Checklist Pre-Publicación de un Notebook de Análisis

Antes de considerar un notebook como "terminado", verifica:

- [ ] **Cabecera completa** (nombre, objetivo, fuentes, fecha, autor)
- [ ] **Contexto e hipótesis** claramente definidos
- [ ] **Datos cargados** con validación de coherencia
- [ ] **Decisiones metodológicas** documentadas en markdown
- [ ] **Visualizaciones** con títulos, leyendas, etiquetas claras
- [ ] **Gráficos guardados** en `outputs/figuras/` con nombres descriptivos
- [ ] **Conclusiones numéricas** específicas (no solo "aumentó", sino "aumentó X%")
- [ ] **Limitaciones** explícitas
- [ ] **Referencias bibliográficas** cuando se usan conceptos/metodologías externas
- [ ] **Código ejecutable** de principio a fin sin errores
- [ ] **Comentarios** en código complejo o no obvio

---

## 🎯 Tipos de Análisis Sugeridos

### 1. Análisis Nacional (`notebooks/01_analisis_nacional/`)
- Evolución temporal de indicadores (Gini, AROPE, S80/S20)
- Impacto de crisis económicas en desigualdad
- Relación entre indicadores (ej: AROP vs carencia material)
- Análisis por grupos demográficos (edad, sexo, situación laboral)

### 2. Análisis Regional (`notebooks/02_analisis_regional/`)
- Comparación entre CCAA
- Convergencia/divergencia regional
- Factores asociados a desigualdad regional (PIB, desempleo)
- Mapas coropléticos

### 3. Comparativa Europea (`notebooks/03_comparativa_europa/`)
- Posición de España en rankings europeos
- Convergencia con UE27
- Análisis de países con menor/mayor desigualdad
- Efecto de políticas redistributivas

---

## 📖 Recursos Adicionales

- **Diccionario de datos:** `docs/DICCIONARIO_DATOS.md`
- **Arquitectura del proyecto:** `docs/ARQUITECTURA.md`
- **Guía de validación:** `notebooks/00_etl/README_VALIDACION.md`

---

*Esta plantilla debe actualizarse según evolucionen las mejores prácticas del proyecto.*
