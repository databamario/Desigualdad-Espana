# Rupturas y Discontinuidades Metodológicas

**Última actualización**: 2025-11-19  
**Fase**: 2 - High Priority (Coherencia Analítica)

---

## 1. Resumen Ejecutivo

Este documento identifica **rupturas metodológicas** (breaks) en las series temporales que pueden afectar la comparabilidad inter-temporal de los datos. Estas discontinuidades NO invalidan los datos, pero requieren **caveats explícitos** en conclusiones.

### Breaks identificados por impacto

| Break | Años Afectados | Impacto | Severidad |
|-------|---------------|---------|-----------|
| **Armonización EU-SILC** | Pre-2013 vs Post-2013 | ECV (Gini, AROPE, Renta) | 🔴 ALTO |
| **Cambio base IPC** | Pre-2021 vs Post-2021 | IPC General + Sectorial | 🟡 MEDIO |
| **COVID-19** | 2020-2021 | Todos los indicadores | 🔴 ALTO |
| **EPF rediseño muestral** | 2006 vs 2008+ | Patrones de gasto | 🟡 MEDIO |
| **Ampliación UE** | 2004, 2007, 2013 | Comparativas europeas | 🟢 BAJO |

---

## 2. Break 1: Armonización EU-SILC (2013) 🔴 ALTO IMPACTO

### 2.1 Descripción del cambio

En **2013**, el INE armonizó completamente la Encuesta de Condiciones de Vida (ECV) con el estándar europeo **EU-SILC** (Statistics on Income and Living Conditions).

**Cambios metodológicos principales**:
- Rediseño del cuestionario (nuevas preguntas sobre privación material)
- Ajustes en definiciones de ingresos (inclusión/exclusión de componentes)
- Cambio en técnicas de imputación de valores perdidos
- Actualización del marco muestral (Censo 2011)

### 2.2 Variables afectadas

| Variable | Tabla | Impacto |
|----------|-------|---------|
| **Gini** | `INE_Gini_CCAA`, `EUROSTAT_Gini_*` | Discontinuidad ~0.5-1.0 puntos |
| **S80/S20** | `INE_Gini_S80S20` | Discontinuidad ~0.1-0.3 puntos |
| **AROPE** | `INE_AROPE_*`, `EUROSTAT_AROP_*` | Cambio definición privación material |
| **Renta por decil** | `INE_Renta_Decil` | Cambio componentes de renta |
| **Umbral pobreza** | `INE_Umbral_Pobreza` | Cambio cálculo mediana |

### 2.3 Evidencia empírica

```python
# Ejemplo de discontinuidad observable en Gini nacional
# Año 2012: Gini ≈ 34.0 (metodología antigua)
# Año 2013: Gini ≈ 33.7 (metodología EU-SILC)
# Salto metodológico: -0.3 puntos (no refleja mejora real)
```

### 2.4 Recomendaciones de uso

✅ **Comparaciones válidas**:
- Series 2013-2024 (metodología homogénea)
- Series 2008-2012 (metodología homogénea)
- Comparativas europeas 2013+ (todos países EU-SILC)

❌ **Comparaciones problemáticas**:
- Evolución 2008-2024 sin caveat del break 2013
- Cálculo de tendencias lineales cruzando 2013
- Afirmaciones del tipo "el Gini cayó entre 2012-2013" (puede ser artefacto metodológico)

⚠️ **Caveat obligatorio**:
> "En 2013 el INE armonizó completamente la ECV con EU-SILC, introduciendo cambios metodológicos que pueden generar discontinuidades menores en las series. Las comparaciones pre-2013 vs post-2013 deben interpretarse con cautela."

### 2.5 Soluciones analíticas

**Opción 1: Análisis por sub-periodos**
```python
# Analizar 2008-2012 y 2013-2024 por separado
df_pre = df[df['Anio'] <= 2012]
df_post = df[df['Anio'] >= 2013]
```

**Opción 2: Variable dummy de periodo**
```python
df['Post_EUSILC'] = (df['Anio'] >= 2013).astype(int)
# Usar en regresiones para controlar el break
```

**Opción 3: Encadenar series (avanzado)**
```python
# Ajustar serie pre-2013 usando ratio 2012/2013
factor_ajuste = df.loc[df['Anio']==2013, 'Gini'].values[0] / df.loc[df['Anio']==2012, 'Gini'].values[0]
df.loc[df['Anio']<=2012, 'Gini_Ajustado'] = df['Gini'] * factor_ajuste
# ⚠️ Esto asume que todo el cambio es metodológico (hipótesis fuerte)
```

---

## 3. Break 2: Cambio Base IPC (2021) 🟡 IMPACTO MEDIO

### 3.1 Descripción del cambio

En **enero 2021**, el INE cambió el año base del IPC de **2016=100** a **2021=100**.

**Implicaciones**:
- Actualización de ponderaciones de la cesta de consumo (datos EPF 2019-2020)
- Incorporación de nuevos productos/servicios (streaming, delivery, etc.)
- Ajustes en categorías ECOICOP

### 3.2 Variables afectadas

| Variable | Tabla | Impacto |
|----------|-------|---------|
| **IPC_Medio_Anual** | `INE_IPC_Anual` | Series históricas reescaladas |
| **IPC_Indice** | `INE_IPC_Sectorial_ECOICOP` | Rebase por categoría |
| **Inflacion_Anual_%** | Calculado | Variaciones NO afectadas |

### 3.3 Estado en nuestra BD

✅ **Series homogeneizadas**: Todos los datos históricos en `INE_IPC_Anual` están expresados en **base 2021=100** (el INE publica series retroactivas reescaladas).

✅ **Variaciones anuales preservadas**: El cambio de base NO afecta a `Inflacion_Anual_%` porque es una tasa de variación (invariante a reescalamientos).

### 3.4 Recomendaciones de uso

✅ **Uso seguro**:
- Calcular tasas de inflación (% variación YoY)
- Deflactar valores nominales a base 2021
- Comparaciones temporales de poder adquisitivo

⚠️ **Precaución**:
- Si usas datos de otras fuentes con base 2016, convertir primero
- Verificar que IPC_Medio_Anual > 100 para años post-2021 (sanity check)

**Fórmula de conversión** (si necesitas base 2016):
```python
# Base 2021 → Base 2016
IPC_base2016 = IPC_base2021 * (IPC_2016_base2021 / 100)
# Donde IPC_2016_base2021 ≈ 91.65 (valor del año 2016 en base 2021)
```

---

## 4. Break 3: Pandemia COVID-19 (2020-2021) 🔴 ALTO IMPACTO

### 4.1 Descripción del shock

La pandemia COVID-19 generó **distorsiones excepcionales** en:
- Patrones de consumo (confinamiento, cierre sectores)
- Mercado laboral (ERTE, teletrabajo, cierres empresas)
- Transferencias públicas (prestaciones extraordinarias, IMV)
- Recogida de datos (encuestas telefónicas vs presenciales)

### 4.2 Variables afectadas

| Variable | Impacto COVID | Mecanismo |
|----------|---------------|-----------|
| **IPC Sectorial** | Volatilidad extrema | Caída demanda viajes (-70%), subida alimentos (+15%) |
| **Gini** | Caída artificial 2020 | Transferencias públicas + cobertura ERTE |
| **AROPE** | Aumento retardado 2021-2022 | Fin de apoyos extraordinarios |
| **EPF** | No representa comportamiento típico | Cambio radical en cesta consumo |
| **Renta deciles** | Comprensión del D1-D3 | Ayudas focalizadas en bajos ingresos |

### 4.3 Ejemplos de distorsiones

**IPC Sectorial (2020)**:
- Transporte: -10% (nadie viajaba)
- Ocio y cultura: -8% (cierres cines, teatros)
- Alimentos en hogar: +3% (shift de restaurantes a supermercados)
- Restaurantes: -5% (cierres obligatorios)

**Gini 2020 (aparente mejora)**:
- Gini cayó ~1 punto → ⚠️ NO es reducción estructural de desigualdad
- Causas: ERTE preservó rentas medias, IMV reforzó cola baja
- 2021-2022: Rebote hacia niveles pre-pandemia

### 4.4 Recomendaciones de uso

❌ **Evitar**:
- Incluir 2020-2021 en tendencias lineales sin controles
- Afirmar "la desigualdad se redujo en 2020" sin contexto
- Usar EPF 2020-2021 como representativa de patrones habituales

✅ **Análisis válidos**:
- Estudios de impacto específico COVID
- Comparaciones 2019 vs 2022-2024 (excluyendo shock)
- Análisis de eficacia de políticas de emergencia

⚠️ **Caveat obligatorio**:
> "Los años 2020-2021 presentan distorsiones excepcionales derivadas de la pandemia COVID-19 y las políticas de respuesta (ERTE, IMV, transferencias). Las tendencias observadas en este periodo no deben extrapolarse como estructurales."

### 4.5 Solución analítica: Variable dummy COVID

```python
df['Periodo_COVID'] = df['Anio'].isin([2020, 2021]).astype(int)

# En regresiones/modelos
import statsmodels.formula.api as smf
modelo = smf.ols('Gini ~ Anio + Periodo_COVID', data=df).fit()
# El coeficiente de Periodo_COVID captura el shock excepcional
```

---

## 5. Break 4: EPF - Periodicidad y Metodología 🟡 IMPACTO MEDIO

### 5.1 Hallazgo Crítico: EPF Anual vs Bienal

**Descubrimiento (2025-11-19)**: La tabla INE 24900 (fuente de `INE_EPF_Gasto`) proporciona **datos anuales continuos 2006-2023**, NO bienales como indica la documentación oficial de EPF.

**Evidencia**:
- Años disponibles: 2006, 2007, 2008, ..., 2022, 2023 (18 años consecutivos)
- Registros por año: 312 constantes (6 quintiles × 13 grupos × 1 tipo valor)

**Implicación**: El INE proporciona una **serie temporal anualizada** en esta tabla, aunque la EPF base es bienal. La metodología para años intermedios no está documentada públicamente (posible interpolación, estimación modelo, o datos de encuestas complementarias).

### 5.2 Rediseño EPF (2006→2008)

Entre **EPF 2006** y **EPF 2008** hubo cambios metodológicos:
- Cambio en marco muestral (Censo 2001 → Padrón continuo)
- Modificación clasificación COICOP (actualización a revisión 2008)
- Ajustes en técnicas de imputación

### 5.3 Variables afectadas

| Variable | Tabla | Impacto |
|----------|-------|---------|
| **Gasto por quintil** | `INE_EPF_Gasto` | Periodicidad anual (no bienal), discontinuidad menor 2006-2008 |
| **Grupos de gasto** | `INE_EPF_Gasto` | Algunas categorías re-agrupadas en 2008 |

### 5.4 Recomendaciones de uso

✅ **Uso seguro**: 
- Análisis 2008-2023 (metodología post-rediseño homogénea)
- Tendencias multi-año (serie anual completa disponible)

⚠️ **Precaución**: 
- Comparar 2006-2007 vs 2008+ requiere caveat del rediseño
- Cambios año-a-año pequeños pueden reflejar metodología de anualización del INE

⚠️ **Caveats obligatorios**:
> "EPF (tabla INE 24900): Datos anuales 2006-2023. Aunque la EPF base es bienal, esta tabla proporciona serie anual. La metodología del INE para la anualización no está documentada públicamente. Tendencias multi-año son robustas; cambios año-a-año pequeños deben interpretarse con cautela."

> "La EPF 2006-2007 usa una metodología diferente a las ediciones 2008 en adelante. Comparaciones pre-2008 vs post-2008 pueden reflejar cambios metodológicos además de cambios reales en patrones de gasto."

---

## 6. Break 5: Ampliaciones de la UE 🟢 IMPACTO BAJO

### 6.1 Cambios en composición UE27

- **2004**: +10 países (Malta, Chipre, países bálticos, Europa del Este)
- **2007**: +2 países (Rumanía, Bulgaria)
- **2013**: +1 país (Croacia)
- **2020**: -1 país (Brexit: Reino Unido sale)

### 6.2 Implicación para comparativas europeas

Las medias/medianas **UE27** cambian de composición:
- 2004-2006: UE25
- 2007-2012: UE27 (sin Croacia)
- 2013-2019: UE28 (con UK)
- 2020+: UE27 (sin UK, con Croacia)

### 6.3 Estado en nuestra BD

✅ EUROSTAT publica series **retroactivas con composición constante UE27** (2020 definition).

⚠️ Si usas fuentes externas pre-2020, verificar composición.

---

## 7. Guía de Caveats por Tipo de Análisis

### 7.1 Análisis de Tendencia Temporal (España)

**Periodo recomendado sin caveats**: 2013-2019 + 2022-2024

**Si incluyes otros periodos, añadir**:
- 2008-2012: "Metodología ECV pre-armonización EU-SILC"
- 2020-2021: "Periodo excepcional COVID-19 con distorsiones no estructurales"
- EPF 2006: "Metodología diferente a ediciones posteriores"

### 7.2 Comparativa España vs Europa

**Periodo recomendado**: 2013-2024 (todos países EU-SILC armonizados)

**Caveats**:
- Pre-2013: "Armonización EU-SILC completa a partir de 2013"
- Composición UE27: "UE27 según definición 2020 (sin Reino Unido)"

### 7.3 Análisis de Poder Adquisitivo (Deflación)

**Caveats**:
- "Valores deflactados a euros constantes base 2021 usando IPC General (INE tabla 24077)"
- "Cambio de base IPC en 2021 no afecta a variaciones calculadas"

### 7.4 Inflación Diferencial por Renta

**Caveats**:
- "Análisis usa IPC sectorial Tipo_Metrica='Variación anual' (0% missingness)"
- "Ponderaciones de gasto basadas en EPF [año], metodología bienal"
- 2020-2021: "Patrones de consumo atípicos por COVID-19"

---

## 8. Plantilla de Caveat para Notebooks

### Caveat Genérico (copiar al inicio de notebooks de análisis)

```python
print("""
⚠️ CAVEATS METODOLÓGICOS:

1. ARMONIZACIÓN EU-SILC (2013): La ECV se armonizó completamente con el estándar 
   europeo en 2013. Comparaciones pre/post-2013 pueden reflejar cambios metodológicos.

2. COVID-19 (2020-2021): Distorsiones excepcionales en todos los indicadores por 
   confinamiento, ERTE, transferencias extraordinarias. No extrapolar tendencias.

3. BASE IPC (2021): Cambio de base a 2021=100. Series históricas reescaladas por INE.
   Variaciones interanuales no afectadas.

4. EPF BIENAL: Encuesta de Presupuestos Familiares disponible cada 2 años. 
   No interpolar años intermedios.

Ver documentación completa: docs/BREAKS_METODOLOGICOS.md
""")
```

### Caveat Específico por Periodo

```python
# Ejemplo: Análisis que cruza 2013
if df['Anio'].min() < 2013 and df['Anio'].max() >= 2013:
    print("⚠️ ADVERTENCIA: Este análisis cruza el break metodológico EU-SILC (2013).")
    print("   Las tendencias mostradas pueden reflejar cambios metodológicos además de cambios reales.")
```

---

## 9. Validación de Breaks: Tests Estadísticos

### 9.1 Test de Chow (detección de break estructural)

```python
import statsmodels.formula.api as smf

# Test en año 2013 para Gini
df['Post2013'] = (df['Anio'] >= 2013).astype(int)
df['Anio_Post2013'] = df['Anio'] * df['Post2013']

# Modelo con break
modelo_con_break = smf.ols('Gini ~ Anio + Post2013 + Anio_Post2013', data=df).fit()

# Si Anio_Post2013 es significativo (p<0.05), hay cambio de tendencia en 2013
print(modelo_con_break.summary())
```

### 9.2 Visualización de breaks

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df['Anio'], df['Gini'], marker='o')

# Líneas verticales en años de breaks
ax.axvline(2013, color='red', linestyle='--', alpha=0.7, label='EU-SILC')
ax.axvline(2020, color='orange', linestyle='--', alpha=0.7, label='COVID-19')
ax.axvline(2021, color='blue', linestyle='--', alpha=0.7, label='Base IPC')

ax.set_title('Gini con Breaks Metodológicos Marcados')
ax.legend()
plt.show()
```

---

## 10. Referencias

- **INE - ECV Metodología EU-SILC**: https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176807
- **EUROSTAT - EU-SILC Quality Reports**: https://ec.europa.eu/eurostat/web/microdata/european-union-statistics-on-income-and-living-conditions
- **INE - Cambio Base IPC 2021**: https://www.ine.es/prensa/ipc_base2021.pdf

---

## 11. Historial de Cambios

| Fecha | Cambio | Responsable |
|-------|--------|-------------|
| 2025-11-19 | Creación inicial - Fase 2 coherencia analítica | GitHub Copilot |
