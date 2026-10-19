# Contexto: IPM e ICS

Documento de referencia sobre los dos índices base del proyecto de pobreza multidimensional y condición social de Santiago de Cali, a nivel de **manzana**.

---

## 1. Índice de Pobreza Multidimensional (IPM)

### Definición

Indicador **inverso** que mide el nivel de privaciones de los hogares.

- `0` = sin pobreza (óptimo)
- `100` = máxima pobreza (crítico)
- Un hogar se considera en **pobreza multidimensional** cuando `IPM >= 33.3%`.
- Las 15 variables desagregadas también son **inversas** (mayor valor = peor situación).

### Nota metodológica: severidad

Para análisis de **severidad** se promedian únicamente las manzanas con `IPM > 0` (donde hay pobreza registrada), lo que mide la *profundidad* de la carencia en los hogares afectados.

- Cali Urbana (severidad) = **15.28**
- Cali Rural (severidad) = **38.33**

### Fuente de datos

| Formato | Archivo | Clave de manzana |
| :--- | :--- | :--- |
| GeoJSON | `data/geojson_ipm/Mzn_ipm_variables.geojson` | `COD_MZN` (22 chars) |
| Excel | `IPM - Variables (incidencias).xlsx` | `cod_mzn` (24 chars) |

> **Merge Excel ↔ ICS:** el `cod_mzn` del Excel tiene 24 chars; el `COD_MZN` del ICS tiene 22. Los 2 dígitos extra (posiciones 6-7) son el número de comuna. Transformación: `COD_MZN = cod_mzn[:6] + cod_mzn[8:]`. Match: 13.614 / 13.687 filas (99.5%).
>
> **Importante:** en los **GeoJSON** de IPM e ICS el `COD_MZN` ya viene homologado a 22 chars, por lo que el cruce entre ellos es directo (`on='COD_MZN'`) y NO requiere la transformación anterior.

### Las 15 variables de incidencia (%)

| Código | Descripción | Obs. aprox. (manzanas) |
| :--- | :--- | :--- |
| `ANALF_` | Analfabetismo | ~9.512 |
| `BAJO_` | Bajo logro educativo | ~13.484 |
| `INFANCIA_` | Barreras servicios de cuidado primera infancia | ~6.487 |
| `INASIS_` | Inasistencia escolar | ~7.435 |
| `REZAGO_` | Rezago escolar | ~12.210 |
| `TRAB_INFAN` | Trabajo infantil | ~2.662 |
| `DEPEN_` | Dependencia económica | ~13.415 |
| `INFOR_` | Informalidad | ~13.686 |
| `SALUD_` | Barreras de acceso a servicios de salud | ~7.932 |
| `ASEGU_` | Sin aseguramiento en salud | ~13.187 |
| `HACI_` | Hacinamiento crítico | ~9.228 |
| `PARED_` | Material inadecuado de paredes exteriores | ~1.425 |
| `EXCRE_` | Eliminación inadecuada de excretas | ~2.008 |
| `PISOS_` | Material inadecuado de los pisos | ~1.065 |
| `AGUA_` | Sin acceso a fuentes de agua mejorada | ~1.511 |

### Agrupación por dimensiones

| Dimensión | Variables |
| :--- | :--- |
| Educación | `ANALF_`, `BAJO_`, `INFANCIA_`, `INASIS_`, `REZAGO_` |
| Trabajo | `TRAB_INFAN`, `DEPEN_`, `INFOR_` |
| Salud | `SALUD_`, `ASEGU_` |
| Vivienda | `HACI_`, `PARED_`, `PISOS_` |
| Servicios | `AGUA_`, `EXCRE_` |

- Variable más crítica a nivel ciudad: `INFOR_` (Informalidad, >82% promedio).
- Segunda más crítica: `BAJO_` (Bajo logro educativo, >37% promedio).

### Columnas del GeoJSON de IPM

```
COD_DPTO, COD_MPIO, COD_DANE, ipm, OID_, COD_MZN,
ANALF_, BAJO_, INFANCIA_, INASIS_, REZAGO_, TRAB_INFAN,
DEPEN_, INFOR_, SALUD_, ASEGU_, HACI_, PARED_, EXCRE_,
PISOS_, AGUA_, zona, zona2, geometry
```

---

## 2. Índice de Condición Social (ICS)

### Definición

Indicador **directo** de bienestar y acceso.

- `0` = condición crítica
- `100` = condición óptima
- Se basa en clima educativo y hacinamiento.

### Fuente de datos

| Formato | Archivo | Clave de manzana |
| :--- | :--- | :--- |
| GeoJSON | `data/geojosn_ICS/ics_mzn.geojson` | `COD_MZN` (22 chars) |

### Columnas del GeoJSON de ICS

```
COD_MZN, CLASE, ZONA, cod_dane_a, ics, geometry
```

---

## 2b. ¿Cómo se interpreta el valor del IPM?

La escala del IPM funciona igual que una **tasa de reprobados en un salón de clases**: va de **0% a 100%** (o de 0,0 a 1,0) y representa el **porcentaje de personas que viven en hogares pobres multidimensionales** dentro de la zona.

- **0%:** en esa zona nadie es pobre multidimensional (cero carencias críticas acumuladas).
- **100%:** en esa zona todos son pobres multidimensionales.

Ejemplos con los datos del proyecto:

- **12,59% (Cali urbano):** de cada 100 personas de la zona urbana de Cali, ~13 viven en hogares que acumulan 33% o más de privaciones básicas.
- **26,52% (Ciudad Paraíso):** de cada 100 personas, casi 27 viven en hogares con privaciones críticas acumuladas (más del doble que el promedio de la ciudad).
- **7,51% (Roosevelt):** de cada 100 personas, solo ~7 u 8 están en esa condición.

### El "truco" de las dos etapas (no confundir los dos porcentajes)

La confusión habitual ocurre porque hay **dos porcentajes distintos**:

1. **El 33% — el examen del hogar.** Es la regla fija para decidir si un hogar es pobre o no. A cada hogar se le suman sus carencias (pisos de tierra, no cotizar a pensión, niños sin estudiar, etc.). Si suma **33% o más**, ese hogar "reprobó" y se cataloga como pobre.
2. **El IPM final — el reporte de la zona.** Es el **porcentaje de gente de la zona** que vive en esos hogares que "reprobaron".

En resumen: el IPM de la tabla (7,51%, 13,18%, 26,52%, etc.) es el porcentaje de habitantes en situación de pobreza multidimensional en cada polígono. Entre más alto el número, más pobre y vulnerable es la zona.

### Escala de referencia estándar para Colombia (área urbana)

Aunque técnicamente el IPM puede llegar a 100%, en las ciudades colombianas los valores urbanos se suelen clasificar así:

| Rango de IPM (%) | Nivel de pobreza multidimensional | Qué significa en la práctica | Ejemplo en el estudio |
| :--- | :--- | :--- | :--- |
| 0,0% – 8,0% | Muy Bajo / Bajo | Zonas consolidadas (estratos 4, 5 y 6). Cobertura casi total de servicios, empleo formal y buen nivel educativo. | Roosevelt (7,51%) |
| 8,1% – 15,0% | Medio / Típico urbano | Promedio de una ciudad capital. Servicios básicos y vivienda aceptable, pero pesa la informalidad laboral o adultos sin bachillerato. | Cali urbano (12,59%); Barrio Obrero (13,18%) |
| 15,1% – 25,0% | Alto | Sectores populares vulnerables. Alta deserción escolar, hacinamiento frecuente, empleo informal generalizado. | Comunas periféricas de ladera u oriente |
| > 25,0% | Crítico / Severo | Zonas deprimidas, inquilinatos precarios o asentamientos informales. Se acumulan fallas de vivienda, saneamiento, educación e ingresos. | Ciudad Paraíso (26,52%) |

> **Nota:** esta escala de referencia estándar (4 niveles) es para **interpretación socioeconómica** del promedio de una zona. Es distinta de la escala técnica de **8 categorías** que usan los mapas del proyecto (sección 3), que sirve para colorear cada manzana individualmente.

---

## 3. Escala de clasificación (8 categorías)

El IPM y el ICS comparten los **mismos rangos numéricos** pero usan **paletas distintas** (ambas accesibles para daltonismo):

- **IPM:** paleta `viridis` (indicador inverso, mayor = peor).
- **ICS:** paleta `cividis` (indicador directo, mayor = mejor).

> Usar coma como separador decimal en textos; punto en código.

| HEX | Rango | Categoría |
| :--- | :--- | :--- |
| `#00224e` | 0,4 - 20,0 | Bajo |
| `#213b6e` | 20,1 - 27,0 | Moderado-Bajo |
| `#4c556c` | 27,1 - 33,1 | Moderado |
| `#6c6e72` | 33,2 - 39,8 | Moderado-Alto |
| `#8e8978` | 39,9 - 48,6 | Alto |
| `#b1a570` | 48,7 - 60,6 | Muy Alto |
| `#d9c55c` | 60,7 - 80,0 | Extremo |
| `#fee838` | 80,1 - 100,0 | Extremo Máximo |

### Formato JSON (para código)

```json
{
  "leyenda": "IPM",
  "configuracion_escala": [
    {"rango_min": 0.4,  "rango_max": 20.0,  "hex": "#00224e", "categoria": "Bajo"},
    {"rango_min": 20.1, "rango_max": 27.0,  "hex": "#213b6e", "categoria": "Moderado-Bajo"},
    {"rango_min": 27.1, "rango_max": 33.1,  "hex": "#4c556c", "categoria": "Moderado"},
    {"rango_min": 33.2, "rango_max": 39.8,  "hex": "#6c6e72", "categoria": "Moderado-Alto"},
    {"rango_min": 39.9, "rango_max": 48.6,  "hex": "#8e8978", "categoria": "Alto"},
    {"rango_min": 48.7, "rango_max": 60.6,  "hex": "#b1a570", "categoria": "Muy Alto"},
    {"rango_min": 60.7, "rango_max": 80.0,  "hex": "#d9c55c", "categoria": "Extremo"},
    {"rango_min": 80.1, "rango_max": 100.0, "hex": "#fee838", "categoria": "Extremo Maximo"}
  ]
}
```

---

## 4. IPM Global comparativo por zona de estudio

| Zona | Manzanas con IPM | IPM Promedio |
| :--- | :--- | :--- |
| Cali (urbano) | 12.787 | 12,59 |
| Barrio Obrero | 11 | 13,18 |
| Roosevelt | 21 | 7,51 |
| Ciudad Paraíso | 33 | 26,52 |

Severidad IPM (`IPM > 0`) por zona: Cali Urbana = 15,28 · Cali Rural = 38,33 · Barrio Obrero = 13,18 · Roosevelt = 7,51.

### Hallazgos clave

- **Barrio Obrero:** severidad de Informalidad del 93,1% (supera el promedio urbano).
- **Roosevelt:** severidad de Sin Aseguramiento en Salud del 22,7%.
- **Ciudad Paraíso:** zona de estudio con mayor privación registrada. IPM global = 26,52 (supera el promedio ciudad), ICS promedio = 23,07. Top privaciones: Informalidad 89,7%, Bajo logro educativo 59,7%, Hacinamiento crítico 22,9%, Sin aseguramiento 21,6%, Dependencia económica 20,9%.
- **Brecha rural:** severidad crítica en infraestructura básica (Eliminación de excretas 41,9%, Agua mejorada 27,0%).

---

## 5. Lectura rápida para interpretar

| Si ves... | IPM | ICS |
| :--- | :--- | :--- |
| Dirección | Inverso (mayor = peor) | Directo (mayor = mejor) |
| Valor alto | Más pobreza / privación | Mejor condición social |
| Paleta | viridis | cividis |
| Umbral de referencia | Pobre si `>= 33,3%` | — |
| Clave de cruce | `COD_MZN` (22 chars en GeoJSON) | `COD_MZN` (22 chars) |
