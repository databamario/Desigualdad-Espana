# 📚 Diccionario de Datos

**Proyecto:** Desigualdad Social en España - Pipeline ETL  
**Autor:** Mario (databamario)  
**Última actualización:** 2025-11-16  

---

## 🎯 Propósito

Este documento describe todas las tablas, variables y decisiones metodológicas del proyecto. Es la **referencia principal** para entender la estructura de datos y su procedencia.

---

## 📊 Resumen de Tablas

| Fuente | Tablas Extraídas | Tablas en SQL Server | Periodo Temporal |
|--------|------------------|----------------------|------------------|
| **INE** | 13 tablas origen | 16 tablas finales | 2008-2023 |
| **EUROSTAT** | 12 datasets API | 14 tablas finales | 2010-2023 |
| **TOTAL** | 25 fuentes | **30 tablas** | 2008-2023 |

---

## 📂 Tablas INE (Instituto Nacional de Estadística)

### 1. INE_IPC_General
**Fuente:** Tabla INE 24077 - IPC General Nacional  
**Descripción:** Índice de Precios al Consumo (IPC) general de España, base 2021=100  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia (2008-2023) |
| `IPC` | float | Índice de Precios al Consumo (base 2021=100) |

**Notas metodológicas:**
- Base de referencia actualizada a 2021=100 (INE cambió de base 2016 a 2021)
- Usado para deflactar variables monetarias (renta, umbral de pobreza)

---

### 2. INE_Umbral_Pobreza_Hogar
**Fuente:** Tabla INE 11205_4 - Umbral de Pobreza por Tipo de Hogar  
**Descripción:** Umbral de riesgo de pobreza (60% mediana ingreso equivalente) según tipo de hogar  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Tipo_Hogar` | str | Categoría de hogar (Total, 1 adulto sin hijos, 2 adultos sin hijos, etc.) |
| `Umbral_Pobreza_Euros` | float | Umbral de pobreza en euros/año |

**Categorías de Tipo_Hogar:**
- `Total`
- `1 adulto sin niños dependientes`
- `2 adultos sin niños dependientes, menores de 65 años`
- `Otros hogares sin niños dependientes`
- `1 adulto con al menos un niño dependiente`
- `2 adultos con 1 niño dependiente`
- `2 adultos con 2 niños dependientes`
- `2 adultos con 3 o más niños dependientes`
- `Otros hogares con niños dependientes`

**Notas metodológicas:**
- Calculado como 60% de la mediana de ingresos equivalentes (escala OCDE modificada)
- Hogar unipersonal = 1.0; adultos adicionales = +0.5; menores <14 años = +0.3

---

### 3. INE_Carencia_Material_Decil
**Fuente:** Tabla INE 9973 - Carencia Material por Decil de Renta  
**Descripción:** Hogares con carencia material severa según decil de ingresos  
**Periodo:** 2013-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Decil_Renta` | str | Decil de ingresos (1º decil, 2º decil, ..., 10º decil, Total) |
| `Porcentaje_Carencia_Severa` | float | % hogares con carencia material severa (0-100) |

**Definición de Carencia Material Severa:**
Hogares que no pueden permitirse al menos 4 de los siguientes 9 ítems:
1. Pagar alquiler, hipoteca o facturas
2. Mantener la vivienda a temperatura adecuada
3. Afrontar gastos imprevistos (≈650€)
4. Comer carne/pescado cada 2 días
5. Irse de vacaciones al menos 1 semana/año
6. Tener coche
7. Tener lavadora
8. Tener TV en color
9. Tener teléfono

**Notas metodológicas:**
- Componente de AROPE (At Risk Of Poverty or social Exclusion)
- Datos disponibles desde 2013 (armonización EU-SILC)

---

### 4. INE_AROPE_Edad_Sexo
**Fuente:** Tabla INE 29287 - Indicador AROPE por Edad y Sexo  
**Descripción:** Tasa AROPE (pobreza o exclusión social) desagregada por edad y sexo  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Edad` | str | Grupo de edad (Total, <16, 16-29, 30-44, 45-64, >=65) |
| `Sexo` | str | Sexo (Ambos sexos, Hombres, Mujeres) |
| `Indicador` | str | Tipo de indicador (AROPE, AROP, BITH, SM) |
| `Valor` | float | Porcentaje de población afectada (0-100) |

**Indicadores incluidos:**
- `AROPE`: At Risk Of Poverty or social Exclusion (pobreza o exclusión)
- `AROP`: At Risk Of Poverty (riesgo de pobreza - ingresos <60% mediana)
- `BITH`: Baja Intensidad de Trabajo en el Hogar (<20% del potencial)
- `SM`: Carencia Material Severa (≥4 de 9 ítems)

**Notas metodológicas:**
- AROPE = AROP ∪ BITH ∪ SM (cumplir al menos 1 de las 3 condiciones)
- Estrategia Europa 2020 para reducción de pobreza

---

### 5. INE_AROPE_Hogar
**Fuente:** Tabla INE 60259 - Indicador AROPE por Tipo de Hogar  
**Descripción:** Tasa AROPE desagregada por tipo de hogar  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Tipo_Hogar` | str | Categoría de hogar |
| `Indicador` | str | Tipo de indicador (AROPE, AROP, BITH, SM) |
| `Valor` | float | Porcentaje de población afectada (0-100) |

**Categorías de Tipo_Hogar:** (idénticas a Umbral_Pobreza_Hogar)

**IMPORTANTE:**  
Esta tabla contiene **AROP** (solo pobreza), mientras que `INE_AROPE_Edad_Sexo` contiene **AROPE completo** (pobreza + exclusión). Por eso usamos esta tabla para validación INE vs EUROSTAT.

---

### 6. INE_AROPE_Laboral
**Fuente:** Tabla INE 74862 - Indicador AROPE por Situación Laboral  
**Descripción:** Tasa AROPE según relación con la actividad económica  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Situacion_Laboral` | str | Relación con la actividad (Total, Ocupado, Parado, Jubilado, Otros inactivos) |
| `Indicador` | str | Tipo de indicador (AROPE, AROP, BITH, SM) |
| `Valor` | float | Porcentaje de población afectada (0-100) |

**Categorías de Situación_Laboral:**
- `Total`
- `Ocupados`
- `Parados`
- `Jubilados`
- `Otros inactivos` (estudiantes, trabajo doméstico, incapacidad)

---

### 7. INE_Gini_S80S20_CCAA
**Fuente:** Tabla INE 60143 - Desigualdad por Comunidades Autónomas  
**Descripción:** Índice de Gini y ratio S80/S20 por CCAA  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional y 17 CCAA + 2 Ciudades Autónomas  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Territorio` | str | CCAA o Total Nacional |
| `Gini` | float | Índice de Gini (0-100, donde 0=igualdad perfecta) |
| `S80/S20` | float | Ratio entre quintil 5 y quintil 1 (>1) |

**Territorios incluidos:**
- `Total Nacional`
- 17 Comunidades Autónomas
- 2 Ciudades Autónomas (Ceuta y Melilla)

**Notas metodológicas:**
- **Gini:** 0 = igualdad perfecta, 100 = desigualdad máxima
- **S80/S20:** Ingresos del 20% más rico / 20% más pobre (ej: 6.0 = ricos ganan 6 veces más)

---

### 8. INE_Renta_Media_Decil
**Fuente:** Tabla INE 11106_2 - Renta Media por Decil  
**Descripción:** Renta media anual por persona según decil de ingresos  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Decil` | str | Decil de renta (1º-10º, Total) |
| `Renta_Media_Euros` | float | Renta media por persona (€/año) |

**Notas metodológicas:**
- Renta neta disponible del hogar / unidades de consumo (escala OCDE modificada)
- Decil 1 = 10% más pobre; Decil 10 = 10% más rico

---

### 9. INE_Poblacion_Edad_Sexo_Nacionalidad
**Fuente:** Tabla INE 56936 - Población por Edad, Sexo y Nacionalidad  
**Descripción:** Población española por edad quinquenal, sexo y nacionalidad  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Edad_Grupo` | str | Grupo quinquenal (<5, 5-9, ..., 85+, Total) |
| `Sexo` | str | Sexo (Total, Hombres, Mujeres) |
| `Nacionalidad` | str | Nacionalidad (Total, Española, Extranjera) |
| `Poblacion` | int | Número de personas |

**Notas metodológicas:**
- Fuente: Padrón Municipal Continuo (INE)
- Usado para calcular tasas poblacionales

---

### 10. INE_Poblacion_CCAA
**Fuente:** Tabla INE 66014 - Población por CCAA, Edad y Sexo  
**Descripción:** Población por Comunidad Autónoma, grupos quinquenales de edad y sexo  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** 17 CCAA + 2 Ciudades Autónomas  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `CCAA` | str | Comunidad Autónoma |
| `Edad_Grupo` | str | Grupo quinquenal (<5, 5-9, ..., 85+, Total) |
| `Sexo` | str | Sexo (Total, Hombres, Mujeres) |
| `Poblacion` | int | Número de personas |

---

### 11. INE_AROPE_CCAA
**Fuente:** Tabla INE 29288 - Indicador AROPE por CCAA  
**Descripción:** Tasa AROPE por Comunidad Autónoma  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional y 17 CCAA + 2 Ciudades Autónomas  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `CCAA` | str | Comunidad Autónoma o Total Nacional |
| `Indicador` | str | Tipo de indicador (AROPE, AROP, BITH, SM) |
| `Valor` | float | Porcentaje de población afectada (0-100) |

---

### 12. INE_Gasto_Medio_Quintil_EPF
**Fuente:** Tabla INE 24900 - Gasto Medio por Hogar según Quintil (EPF)  
**Descripción:** Gasto medio anual por hogar según quintil de ingresos (Encuesta Presupuestos Familiares)  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Quintil` | str | Quintil de ingresos (1º-5º, Total) |
| `Gasto_Medio_Euros` | float | Gasto medio anual por hogar (€/año) |

**Notas metodológicas:**
- Fuente: Encuesta de Presupuestos Familiares (EPF), metodología diferente a ECV
- Quintil 1 = 20% más pobre; Quintil 5 = 20% más rico

---

### 13. INE_IPC_Sectorial_ECOICOP
**Fuente:** Tabla INE 50902 - IPC por Grupos ECOICOP  
**Descripción:** Índice de Precios al Consumo desagregado por grandes grupos de consumo (ECOICOP)  
**Periodo:** 2008-2023 (anual)  
**Nivel geográfico:** Nacional  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `Grupo_ECOICOP` | str | Categoría de consumo según clasificación ECOICOP |
| `IPC_Sectorial` | float | IPC del grupo (base 2021=100) |

**Grupos ECOICOP incluidos:**
1. Alimentos y bebidas no alcohólicas
2. Bebidas alcohólicas y tabaco
3. Vestido y calzado
4. Vivienda
5. Menaje
6. Medicina
7. Transporte
8. Comunicaciones
9. Ocio y cultura
10. Enseñanza
11. Hoteles, cafés y restaurantes
12. Otros bienes y servicios

---

## 🌍 Tablas EUROSTAT

### 14. EUROSTAT_Gini_Espana
**Fuente:** EUROSTAT dataset `ilc_di12` (Gini coefficient of equivalised disposable income)  
**Descripción:** Índice de Gini de España desde EUROSTAT  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** España (geo_code='ES')  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico (siempre 'ES') |
| `Gini` | float | Índice de Gini (0-100) |

**Notas metodológicas:**
- Fuente: EU-SILC (Statistics on Income and Living Conditions)
- Comparable con `INE_Gini_S80S20_CCAA` para validación cruzada

---

### 15. EUROSTAT_AROP_Espana
**Fuente:** EUROSTAT dataset `ilc_li02` (At-risk-of-poverty rate by poverty threshold)  
**Descripción:** Tasa de riesgo de pobreza (AROP) de España por edad y sexo  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** España (geo_code='ES')  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('ES') |
| `age` | str | Grupo de edad (TOTAL, Y_LT16, Y16-64, Y_GE65) |
| `sex` | str | Sexo (T=Total, M=Male, F=Female) |
| `AROP_%` | float | % población bajo umbral pobreza (0-100) |

**Categorías de edad:**
- `TOTAL`: Todas las edades
- `Y_LT16`: Menores de 16 años
- `Y16-64`: 16 a 64 años
- `Y_GE65`: 65 años o más

**IMPORTANTE:**  
Esta tabla contiene **AROP** (solo riesgo de pobreza), no AROPE completo. Comparable con `INE_AROPE_Hogar` filtrando por `Indicador='AROP'`.

---

### 16. EUROSTAT_S80S20_Espana
**Fuente:** EUROSTAT dataset `ilc_di11` (Income quintile share ratio)  
**Descripción:** Ratio S80/S20 de España por edad y sexo  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** España (geo_code='ES')  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('ES') |
| `age` | str | Grupo de edad (TOTAL, Y_LT16, Y16-64, Y_GE65) |
| `sex` | str | Sexo (T, M, F) |
| `S80S20_Ratio` | float | Ratio ingresos Q5/Q1 (>1) |

---

### 17. EUROSTAT_Brecha_Pobreza_Espana
**Fuente:** EUROSTAT dataset `sdg_10_30` (Relative median at-risk-of-poverty gap)  
**Descripción:** Brecha relativa de pobreza de España  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** España (geo_code='ES')  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('ES') |
| `Brecha_%` | float | Distancia mediana pobres al umbral (0-100) |

**Notas metodológicas:**
- Mide qué tan lejos están los pobres del umbral de pobreza
- Brecha alta = pobres muy lejos del umbral (pobreza más intensa)

---

### 18. EUROSTAT_Gini_UE27
**Fuente:** EUROSTAT dataset `ilc_di12`  
**Descripción:** Índice de Gini promedio de la UE27  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** UE27 (geo_code='EU27_2020')  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('EU27_2020') |
| `Gini` | float | Índice de Gini UE27 (0-100) |

---

### 19. EUROSTAT_AROP_UE27
**Fuente:** EUROSTAT dataset `ilc_li02`  
**Descripción:** Tasa AROP promedio de la UE27  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** UE27  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('EU27_2020') |
| `age` | str | Grupo de edad |
| `sex` | str | Sexo |
| `AROP_%` | float | % población bajo umbral (0-100) |

---

### 20. EUROSTAT_S80S20_UE27
**Fuente:** EUROSTAT dataset `ilc_di11`  
**Descripción:** Ratio S80/S20 promedio de la UE27  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** UE27  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('EU27_2020') |
| `age` | str | Grupo de edad |
| `sex` | str | Sexo |
| `S80S20_Ratio` | float | Ratio Q5/Q1 (>1) |

---

### 21. EUROSTAT_Brecha_Pobreza_UE27
**Fuente:** EUROSTAT dataset `sdg_10_30`  
**Descripción:** Brecha relativa de pobreza promedio UE27  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** UE27  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código geográfico ('EU27_2020') |
| `Brecha_%` | float | Distancia mediana al umbral (0-100) |

---

### 22-25. EUROSTAT_Gini_Ranking, EUROSTAT_AROP_Ranking, EUROSTAT_S80S20_Ranking, EUROSTAT_Brecha_Ranking
**Fuente:** Datasets `ilc_di12`, `ilc_li02`, `ilc_di11`, `sdg_10_30`  
**Descripción:** Rankings de todos los países europeos para comparación  
**Periodo:** 2010-2023 (anual)  
**Nivel geográfico:** Todos los países UE + EFTA  

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `Año` | int | Año de referencia |
| `geo_code` | str | Código país (ES, FR, DE, IT, etc.) |
| `Indicador` | float | Valor del indicador según tabla |

**Países incluidos:** ~40 países (UE27, UK, Noruega, Suiza, Islandia, etc.)

---

### 26-30. Tablas Adicionales EUROSTAT (España por regiones, detalle temporal, etc.)

**Nota:** Si has extraído más tablas EUROSTAT específicas, documéntalas aquí.

---

## 🔍 Decisiones Metodológicas Clave

### 1. ¿Por qué comparar AROP y no AROPE entre INE y EUROSTAT?

**Problema inicial:** Al comparar `INE_AROPE_Edad_Sexo` (indicador AROPE completo) con `EUROSTAT_AROP_Espana` (solo riesgo de pobreza), encontramos discrepancias del 25%.

**Solución:** Usar `INE_AROPE_Hogar` filtrando por `Indicador='AROP'` para comparar "manzanas con manzanas".

**Resultado:** Coherencia perfecta (<0.5% diferencia) entre INE y EUROSTAT.

**Lección:** **Siempre verificar qué indicador exacto contiene cada tabla** antes de comparar fuentes.

---

### 2. ¿Por qué deflactar con IPC base 2021=100?

El INE actualizó la base del IPC de 2016 a 2021 en 2022. Para mantener coherencia temporal:
- Todos los valores monetarios se deflactan con IPC base 2021=100
- Permite comparar poder adquisitivo real entre 2008 y 2023

---

### 3. ¿Por qué usar escala OCDE modificada?

La **escala de equivalencia OCDE modificada** ajusta los ingresos del hogar según su tamaño:
- Primer adulto: 1.0
- Adultos adicionales: +0.5 cada uno
- Menores de 14 años: +0.3 cada uno

**Ejemplo:** Hogar con 2 adultos + 2 niños = 1.0 + 0.5 + 0.3 + 0.3 = 2.1 unidades de consumo

Esto permite comparar hogares de diferente tamaño de forma justa.

---

### 4. ¿Por qué no añadir columna 'fuente' a todas las tablas?

**Decisión profesional:** La fuente está **implícita en el nombre de la tabla** (prefijo `INE_` o `EUROSTAT_`).

**Ventajas:**
- ✅ Evita redundancia (nombre de tabla ya identifica la fuente)
- ✅ Reduce tamaño de tablas
- ✅ Simplifica queries SQL

**Cuándo SÍ añadir columna 'fuente':**
- ❌ NO: Tablas que provienen de una sola fuente
- ✅ SÍ: Tablas fusionadas que mezclan INE + EUROSTAT (ej: comparativas, análisis integrado)

---

## 📖 Referencias Bibliográficas

1. **INE - Encuesta de Condiciones de Vida (ECV):**  
   https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176807&menu=ultiDatos&idp=1254735976608

2. **EUROSTAT - EU-SILC (Statistics on Income and Living Conditions):**  
   https://ec.europa.eu/eurostat/web/income-and-living-conditions

3. **Metodología AROPE (Estrategia Europa 2020):**  
   https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:At_risk_of_poverty_or_social_exclusion_(AROPE)

4. **Escala de Equivalencia OCDE:**  
   https://www.oecd.org/els/soc/OECD-Note-EquivalenceScales.pdf

5. **Clasificación ECOICOP (Consumo):**  
   https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Classification_of_individual_consumption_by_purpose_(COICOP)

---

## 📝 Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-11-16 | Creación inicial del diccionario | Mario |
| 2025-11-16 | Documentación de decisión metodológica AROP vs AROPE | Mario |

---

## 📧 Contacto

Para preguntas sobre este diccionario o sugerencias de mejora:
- **GitHub:** databamario
- **Repositorio:** https://github.com/databamario/Desigualdad-Espana

---

*Este documento es parte del proyecto de análisis de desigualdad social en España y debe actualizarse cada vez que se añadan nuevas tablas o se modifique la metodología.*
