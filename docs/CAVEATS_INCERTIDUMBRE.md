# Caveats de Incertidumbre y Confianza Estadística

**Última actualización**: 2025-11-19  
**Fase**: 2 - High Priority (Coherencia Analítica)

---

## 1. Resumen Ejecutivo

Este documento proporciona **guías de incertidumbre** para interpretar correctamente los resultados del análisis de desigualdad social. Ninguna de nuestras fuentes (INE, EUROSTAT) publica **intervalos de confianza** o errores estándar para los indicadores agregados, por lo que debemos establecer niveles de confianza **cualitativos** basados en el diseño metodológico de las encuestas.

### Matriz de confianza por tipo de conclusión

| Tipo de Conclusión | Nivel de Confianza | Justificación |
|-------------------|-------------------|---------------|
| **Tendencias multi-año (5+ años)** | 🟢 **ALTO** | Ruido muestral se promedia en largo plazo |
| **Comparaciones inter-regionales** | 🟢 **ALTO** | Muestras independientes, controladas por INE |
| **Diferencias >5 puntos Gini** | 🟢 **ALTO** | Magnitud supera variabilidad muestral típica |
| **Variaciones año-a-año (<2 puntos)** | 🟡 **MEDIO** | Puede confundirse con variabilidad muestral |
| **Diferencias entre quintiles Q5/Q1** | 🟢 **ALTO** | Magnitudes grandes, robustas a muestreo |
| **Diferencias entre deciles contiguos** | 🟡 **MEDIO** | Menor separación, más sensible a muestreo |
| **Comparaciones pre-2013 vs post-2013** | 🟠 **BAJO** | Break metodológico EU-SILC confunde tendencia |
| **Conclusiones periodo COVID (2020-2021)** | 🟠 **BAJO** | Distorsiones excepcionales, no estructurales |
| **Interpolaciones EPF años intermedios** | 🔴 **MUY BAJO** | No hay datos reales, solo bienal |

---

## 2. Limitaciones de los Datos

### 2.1 Ausencia de Intervalos de Confianza Publicados

**Problema**: El INE y EUROSTAT publican estimaciones puntuales (Gini, AROPE, S80/S20) pero **NO publican**:
- ❌ Intervalos de confianza (IC 95%)
- ❌ Errores estándar (SE)
- ❌ Coeficientes de variación (CV)
- ❌ Tamaños de muestra efectivos por estrato

**Implicación**: No podemos calcular **significancia estadística formal** para afirmar:
- "El Gini de 2024 es significativamente diferente del de 2023"
- "La diferencia España-UE27 es estadísticamente significativa"

### 2.2 Lo que SÍ sabemos (diseño muestral)

**Encuesta de Condiciones de Vida (ECV)**:
- **Tamaño muestral**: ~13,000 hogares/año (~35,000 personas)
- **Diseño**: Muestreo estratificado por CCAA, tamaño municipio, edad
- **Panel rotativo**: 4 años de permanencia (25% renovación anual)
- **Margen de error típico Gini**: Estimado ~0.3-0.5 puntos (basado en literatura)

**Encuesta de Presupuestos Familiares (EPF)**:
- **Tamaño muestral**: ~24,000 hogares/edición bienal
- **Diseño**: Muestreo bietápico estratificado
- **Margen de error gasto medio**: Estimado ~2-3% para agregados nacionales

**EUROSTAT EU-SILC**:
- Tamaños muestrales varían por país (España: ~13k hogares)
- Países pequeños (Malta, Chipre): muestras <5k → mayor variabilidad
- Armonización metodológica reduce comparabilidad directa

### 2.3 Reglas heurísticas de incertidumbre

En ausencia de IC publicados, usamos estas reglas conservadoras:

| Indicador | Cambio Mínimo Detectable (CMD) | Justificación |
|-----------|-------------------------------|---------------|
| **Gini** | ≥ 0.5 puntos | 2x error estándar estimado |
| **S80/S20** | ≥ 0.2 puntos | Ratios más volátiles que Gini |
| **AROPE %** | ≥ 1.0 punto porcentual | Combinación 3 indicadores |
| **Renta deciles** | ≥ 3% variación | Deciles extremos más variables |
| **IPC inflación** | ≥ 0.5 puntos porcentuales | Series administrativas (bajo error) |

**Interpretación CMD**:
- Cambios **< CMD**: No concluyentes (pueden ser ruido muestral)
- Cambios **≥ CMD**: Alta confianza de cambio real
- Cambios **≥ 2×CMD**: Muy alta confianza

---

## 3. Niveles de Confianza por Tipo de Análisis

### 3.1 Tendencias Temporales (Alta Confianza 🟢)

**Justificación**: El ruido muestral año-a-año se promedia en series largas. Cambios sostenidos en la misma dirección (3+ años) son robustos.

**Conclusiones válidas**:
✅ "El Gini en España ha mostrado una tendencia descendente 2014-2019 (de 34.7 a 33.0)"
✅ "La pobreza infantil (AROPE <18) aumentó sistemáticamente 2008-2014"
✅ "La inflación acumulada 2015-2024 fue del X%"

**Caveats obligatorios**:
⚠️ "Tendencia observada en datos muestrales ECV (n≈13k hogares/año)"
⚠️ "Variaciones puntuales año-a-año pueden reflejar variabilidad muestral"

**Ejemplo de redacción correcta**:
> "Entre 2014 y 2019, el índice de Gini descendió de 34.7 a 33.0 puntos (Δ=-1.7), una reducción sostenida que supera ampliamente el margen de incertidumbre muestral estimado (~0.5 puntos). Esta mejora distributiva se interrumpió con la pandemia (2020-2021), periodo que presenta distorsiones excepcionales."

### 3.2 Comparaciones Inter-Regionales (Alta Confianza 🟢)

**Justificación**: Las muestras son independientes por CCAA, el diseño estratificado garantiza representatividad regional.

**Conclusiones válidas**:
✅ "Andalucía presenta mayor AROPE que Navarra (diferencia ~15 puntos)"
✅ "La dispersión del Gini entre CCAA es de X puntos"

**Caveats obligatorios**:
⚠️ "Tamaños muestrales varían por CCAA (Andalucía ~1800 hogares, La Rioja ~500)"
⚠️ "CCAA pequeñas tienen mayor variabilidad muestral"

**Regla práctica**:
- Diferencias **≥3 puntos Gini** entre CCAA → Alta confianza
- Diferencias **<3 puntos** → Mencionar que pueden solaparse por incertidumbre

### 3.3 Variaciones Año-a-Año (Confianza Media 🟡)

**Problema**: Cambios pequeños (<1 punto Gini, <0.5pp inflación) pueden confundirse con ruido muestral.

**Conclusiones problemáticas**:
❌ "El Gini mejoró 0.2 puntos en 2024" → Indistinguible de ruido
❌ "La inflación bajó 0.3pp este mes" → IPC mensual es muy volátil

**Redacción correcta**:
🟡 "El Gini mostró una variación de 0.2 puntos en 2024, dentro del rango de variabilidad muestral esperada. Para confirmar una tendencia de mejora, se requieren datos de años sucesivos."

**Regla práctica**:
- Cambios **<0.5 Gini**: No afirmar cambio significativo sin varios años
- Cambios **0.5-1.0**: Mencionar como "cambio moderado, pendiente confirmación"
- Cambios **>1.0**: Alta confianza de cambio real

### 3.4 Diferencias entre Quintiles/Deciles (Variable 🟢🟡)

**Alta confianza** (Q5 vs Q1, D10 vs D1):
✅ "El quintil más rico gana 6 veces más que el más pobre (S80/S20=6.0)"
✅ "El decil 10 concentra el 25% de la renta total"

**Confianza media** (Deciles contiguos):
🟡 "El decil 6 gana un 12% más que el decil 5"
→ Diferencias pequeñas entre grupos contiguos son más sensibles a muestreo

**Redacción correcta**:
> "El ratio S80/S20 (quintil más rico / más pobre) de 6.0 refleja una desigualdad robusta, muy superior a la variabilidad muestral esperada. En cambio, diferencias menores del 10% entre deciles intermedios deben interpretarse con cautela."

### 3.5 Comparaciones España vs UE27 (Alta Confianza 🟢)

**Justificación**: Diferencias típicas España-UE27 son grandes (2-4 puntos Gini), superan ampliamente incertidumbre muestral.

**Conclusiones válidas**:
✅ "España tiene mayor desigualdad que la media UE27 (Gini 33.0 vs 30.2)"
✅ "La tasa AROPE española duplica la de Finlandia"

**Caveats obligatorios**:
⚠️ "Comparación basada en EU-SILC armonizado (2013+)"
⚠️ "Países con muestras pequeñas (Malta, Chipre) tienen mayor variabilidad"

### 3.6 Inflación Diferencial por Quintil (Confianza Media-Alta 🟢🟡)

**Alta confianza en existencia del efecto**:
✅ "Los hogares de menores ingresos enfrentan mayor inflación por mayor peso de alimentos"

**Confianza media en magnitud exacta**:
🟡 "Diferencial de inflación Q1-Q5: 0.8pp" → Depende de:
- Precisión ponderaciones EPF (bienal, n=24k)
- Volatilidad IPC sectorial (especialmente energía)
- Supuesto de cesta de consumo constante en año (irreal)

**Redacción correcta**:
> "El análisis de inflación diferencial por quintil revela que los hogares de menores ingresos experimentan una inflación sistemáticamente superior (~0.5-1.0pp) debido al mayor peso de alimentos y energía en su consumo. La magnitud exacta de este diferencial varía según la evolución de precios sectoriales y está sujeta a incertidumbre por el diseño bienal de la EPF."

---

## 4. Caveats Específicos por Indicador

### 4.1 Índice de Gini

**Fortalezas**:
✅ Indicador robusto, usado internacionalmente
✅ Muestra grande (n~13k hogares) reduce error muestral
✅ Comparable en el tiempo (2008-2024) y entre países

**Limitaciones**:
⚠️ Sensible a valores extremos (muy ricos/muy pobres)
⚠️ No captura toda la dimensión de desigualdad (riqueza, acceso servicios)
⚠️ Break metodológico 2013 (EU-SILC)

**Caveat estándar**:
> "Gini basado en renta disponible equivalente, ECV (n≈13k hogares/año). Variaciones <0.5 puntos pueden reflejar variabilidad muestral. Break metodológico EU-SILC en 2013."

### 4.2 AROPE (At Risk of Poverty or Exclusion)

**Fortalezas**:
✅ Indicador multidimensional (pobreza + privación + baja intensidad laboral)
✅ Armonizado UE (comparable entre países)

**Limitaciones**:
⚠️ Combina 3 componentes → mayor variabilidad que indicadores simples
⚠️ Definición "privación material severa" cambió en 2013 (EU-SILC)
⚠️ Umbral relativo (60% mediana) → puede bajar en recesiones por caída general de rentas

**Caveat estándar**:
> "AROPE combina 3 indicadores (pobreza relativa, privación material, baja intensidad laboral). Umbral de pobreza es relativo (60% mediana de ingresos), por lo que puede descender en recesiones si la mediana cae. Definición armonizada EU-SILC desde 2013."

### 4.3 S80/S20 (Ratio Quintiles)

**Fortalezas**:
✅ Fácil interpretación (cuántas veces gana Q5 respecto a Q1)
✅ Robusto a valores centrales de la distribución

**Limitaciones**:
⚠️ Ignora lo que pasa dentro de cada quintil
⚠️ Más volátil que Gini (depende solo de 2 puntos de la distribución)
⚠️ Sensible a cambios en colas (desempleo, pensiones)

**Caveat estándar**:
> "S80/S20 mide el ratio entre el quintil más rico y el más pobre, ignorando redistribución en quintiles intermedios. Más volátil que el Gini debido a su foco en las colas de la distribución."

### 4.4 Renta por Decil

**Fortalezas**:
✅ Desagregación detallada de la distribución
✅ Permite analizar movilidad entre deciles (con panel)

**Limitaciones**:
⚠️ Deciles extremos (D1, D10) tienen mayor variabilidad muestral
⚠️ Diferencias entre deciles contiguos (D5-D6) pueden ser ruido
⚠️ Valores nominales (requieren deflación para comparar temporalmente)

**Caveat estándar**:
> "Rentas medias y medianas por decil en euros corrientes (nominales). Para comparaciones temporales, deflactar con IPC base 2021. Deciles extremos (D1, D10) presentan mayor variabilidad muestral. Diferencias <10% entre deciles contiguos pueden reflejar incertidumbre."

### 4.5 IPC e Inflación

**Fortalezas**:
✅ Dato administrativo (no muestral) → bajo error de medición
✅ Actualización mensual → alta frecuencia
✅ Series largas y homogéneas (con reescalamientos de base)

**Limitaciones**:
⚠️ Representa cesta de consumo "promedio", no individualizada
⚠️ Cambio de base 2021 requiere cuidado en series históricas
⚠️ IPC sectorial puede ser volátil mensualmente (usar variaciones anuales)

**Caveat estándar**:
> "IPC base 2021=100 (INE tabla 24077). Representa cesta promedio de consumo, no personalizada por nivel de renta. Para inflación sectorial, usar Tipo_Metrica='Variación anual' (0% missingness). Cambio de base en 2021 no afecta a variaciones interanuales."

### 4.6 EPF - Gasto por Quintil

**Fortalezas**:
✅ Muestra grande (n~24k hogares por edición)
✅ Detalle por categorías COICOP
✅ Serie anual completa 2006-2023 (18 años)

**Limitaciones**:
⚠️ **Periodicidad anual vs EPF base bienal**: La tabla 24900 proporciona serie anual aunque EPF base es bienal. Metodología de anualización del INE no documentada públicamente.
⚠️ Cambio metodológico 2006→2008 (rediseño marco muestral, COICOP)
⚠️ Gasto declarado ≠ gasto real (subdeclaración en alcohol, tabaco)
⚠️ COVID-19 (2020): Patrón de consumo excepcional

**Caveat estándar**:
> "EPF tabla 24900: Serie anual 2006-2023 (n≈24k hogares por edición EPF base bienal). Gasto en euros corrientes (nominales). La metodología del INE para proporcionar valores anuales no está documentada; cambios año-a-año pequeños pueden reflejar estimación/interpolación. Tendencias multi-año son robustas. Periodo 2020-2021 presenta patrones de consumo atípicos por COVID-19. Metodología homogénea desde 2008."

---

## 5. Plantillas de Redacción Robusta

### 5.1 Para Tendencias Temporales

❌ **Redacción débil**:
> "El Gini bajó en 2024."

✅ **Redacción robusta**:
> "El Gini mostró una disminución de X puntos en 2024 (de Y a Z), continuando la tendencia descendente iniciada en 2022. Dado que la magnitud del cambio (X puntos) supera el cambio mínimo detectable estimado (~0.5 puntos), esta mejora distributiva se considera robusta a la variabilidad muestral de la ECV."

### 5.2 Para Comparaciones Inter-Regionales

❌ **Redacción débil**:
> "Cataluña tiene menos desigualdad que Andalucía."

✅ **Redacción robusta**:
> "Cataluña presenta un Gini de X puntos, frente a Y puntos en Andalucía (diferencia: Z puntos). Esta brecha regional, superior a 3 puntos, es sustancialmente mayor que la variabilidad muestral esperada en las estimaciones por CCAA del ECV, evidenciando diferencias estructurales en la distribución de la renta entre ambas regiones."

### 5.3 Para Diferencias Pequeñas

❌ **Redacción débil**:
> "El Gini mejoró 0.3 puntos."

✅ **Redacción robusta**:
> "El Gini mostró una variación de 0.3 puntos, dentro del rango de variabilidad muestral esperada (±0.5 puntos). Esta oscilación no permite concluir un cambio estructural; se requiere confirmación en años sucesivos para identificar una tendencia sostenida."

### 5.4 Para Periodo COVID

❌ **Redacción débil**:
> "La desigualdad se redujo en 2020."

✅ **Redacción robusta**:
> "El Gini descendió en 2020, coincidiendo con el despliegue de medidas extraordinarias (ERTE, IMV, transferencias). Esta reducción aparente debe interpretarse con cautela: refleja el efecto coyuntural de políticas de emergencia sobre la renta disponible, no una mejora estructural de la distribución del mercado. El rebote parcial observado en 2021-2022 confirma el carácter transitorio de este efecto."

### 5.5 Para Inflación Diferencial

❌ **Redacción débil**:
> "Los pobres sufren más inflación: 0.8pp de diferencia."

✅ **Redacción robusta**:
> "El análisis de inflación diferencial, basado en IPC sectorial ponderado por patrones de gasto EPF, revela que los hogares del quintil inferior experimentan una inflación efectiva ~0.5-1.0pp superior a la del quintil superior durante periodos de alta inflación alimentaria. La magnitud exacta de este diferencial está sujeta a incertidumbre por: (i) diseño bienal de EPF, (ii) volatilidad del IPC sectorial, (iii) supuesto de cesta de consumo constante. El efecto cualitativo (existencia del diferencial) es robusto y consistente con la literatura internacional."

---

## 6. Checklist de Validación de Conclusiones

Antes de publicar una conclusión, verificar:

- [ ] **Magnitud del cambio**: ¿Supera el CMD del indicador?
- [ ] **Dirección sostenida**: ¿Se repite en 2+ años consecutivos?
- [ ] **Break metodológico**: ¿Cruza 2013 (EU-SILC) o 2020 (COVID)?
- [ ] **Tamaño muestral**: ¿Es una CCAA pequeña o país pequeño UE?
- [ ] **Caveat incluido**: ¿Menciona fuente de datos y limitaciones?
- [ ] **Alternativa explicativa**: ¿Podría ser ruido muestral o artefacto metodológico?
- [ ] **Cuantificador adecuado**: ¿Usa "sugiere", "muestra", "evidencia" según confianza?

### Vocabulario según nivel de confianza

| Confianza | Verbos Apropiados | Ejemplo |
|-----------|------------------|---------|
| 🟢 **Alta** | evidencia, demuestra, confirma | "Los datos evidencian una reducción sostenida" |
| 🟡 **Media** | sugiere, indica, apunta a | "Los datos sugieren una mejora moderada" |
| 🟠 **Baja** | podría indicar, es compatible con | "Los datos podrían indicar un cambio, pendiente confirmación" |
| 🔴 **Muy Baja** | no permite concluir, inconcluyente | "La variación observada no permite concluir un cambio estructural" |

---

## 7. Limitaciones Generales del Proyecto

### 7.1 Limitaciones de Diseño

1. **Datos secundarios**: Dependemos de microdatos no públicos (INE no publica microdatos ECV abiertamente)
2. **Sin IC publicados**: No podemos calcular significancia estadística formal
3. **Agregación territorial**: Algunos análisis regionales tienen n muestral bajo
4. **Periodicidad heterogénea**: EPF bienal vs ECV anual

### 7.2 Limitaciones de Alcance

1. **Renta, no riqueza**: Gini de renta ignora desigualdad de patrimonio (vivienda, ahorros)
2. **Hogares, no individuos**: Supone equivalencia perfecta dentro del hogar (puede ocultar desigualdad intra-familiar)
3. **Desigualdad monetaria**: No captura desigualdad en salud, educación, acceso servicios
4. **Sin microdatos**: No podemos hacer regresiones multinivel o modelos complejos

### 7.3 Disclaimer General para Publicaciones

```markdown
---
**NOTA METODOLÓGICA**

Este análisis se basa en datos agregados de la Encuesta de Condiciones de Vida (ECV, 
n≈13,000 hogares/año) y EU-SILC de EUROSTAT. Dado que las fuentes oficiales no publican 
intervalos de confianza para los indicadores agregados (Gini, AROPE, S80/S20), establecemos 
niveles de confianza cualitativos basados en:

- Magnitud de los cambios observados vs. variabilidad muestral estimada
- Sostenibilidad temporal de las tendencias (2+ años)
- Robustez metodológica (breaks EU-SILC 2013, COVID 2020-2021)

Las conclusiones de **alta confianza** (tendencias multi-año, comparaciones regionales 
grandes) son robustas a la incertidumbre muestral. Las conclusiones de **confianza media** 
(variaciones año-a-año pequeñas) requieren confirmación en años sucesivos.

Ver documentación completa: `docs/CAVEATS_INCERTIDUMBRE.md`
---
```

---

## 8. Referencias

- **INE - ECV Metodología**: https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176807
- **EUROSTAT - Quality Reports EU-SILC**: https://ec.europa.eu/eurostat/web/microdata/european-union-statistics-on-income-and-living-conditions
- **Gastwirth (2017)**: "Is the Gini Index of Inequality Overly Sensitive to Changes in the Middle of the Income Distribution?" - Sobre robustez del Gini
- **Jenkins & Van Kerm (2009)**: "The Measurement of Economic Inequality" - Sobre errores estándar de indicadores de desigualdad

---

## 9. Historial de Cambios

| Fecha | Cambio | Responsable |
|-------|--------|-------------|
| 2025-11-19 | Creación inicial - Fase 2 coherencia analítica | GitHub Copilot |
