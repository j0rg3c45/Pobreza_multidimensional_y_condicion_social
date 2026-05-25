# Contexto Maestro para Agente

Este archivo resume el contexto mas importante del repo para que otro agente pueda trabajar con buen criterio metodologico y operativo desde el inicio.

## 1. Objetivo del proyecto

El repositorio calcula el **Indice de Transformacion Territorial (ITT)** para zonas de intervencion urbana de Cali, Colombia.

El ITT busca medir transformacion positiva del territorio en escala `0-100` y permitir comparaciones entre zonas usando una metodologia comun.

## 2. Regla metodologica principal

La metodologia vigente del proyecto exige:

- Usar `ref_min/ref_max` fijos por indicador.
- No usar min-max relativo calculado desde la propia muestra de la zona cuando el territorio es pequeno o los conteos son bajos.
- Diferenciar entre datos reales, valores Proxy y resultados efectivamente calculados.

La fuente metodologica principal y prioritaria es:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`

Si hay contradiccion entre un resumen corto en `docs/` y la guia metodologica completa, debe priorizarse la guia metodologica completa y luego el estado real de los notebooks.

## 3. Dimensiones y pesos oficiales

El ITT vigente usa 5 dimensiones:

- Seguridad: `0.30`
- Movilidad: `0.25`
- Entorno Urbano: `0.20`
- Educacion y Desarrollo: `0.13`
- Cohesion Social: `0.12`

La suma de los pesos debe ser `1.0`.

## 4. Valores Proxy actuales

Mientras una zona no tenga datos propios para ciertas dimensiones o indicadores, el proyecto usa referentes de `Pulmon de Oriente`.

Valores vigentes:

- `Entorno Urbano = 39.2`
- `Educacion y Desarrollo = 54.9`
- `Vulnerabilidad = 54.1`

Estos valores deben tratarse como **provisionales**, no como mediciones propias de la zona analizada.

Excepcion actual importante:

- En `notebooks/03_itt_barrio_obrero.ipynb`, `Entorno Urbano` ya puede dejar de usar `39.2` si se ejecuta la celda proxy basada en `deficit habitacional 2024`.

## 5. Estado real de notebooks

### Notebook de referencia principal

- `notebooks/03_itt_barrio_obrero.ipynb`

Este notebook es la referencia operativa mas importante del repo porque:

- Ya usa `ref_min/ref_max` fijos.
- Tiene la estructura metodologica vigente.
- Es el mejor punto de partida para revisar logica de calculo, normalizacion, pesos, series anuales y trimestrales, y exportacion.
- Ademas, ya documenta un caso real de reemplazo parcial del referente fijo de `Entorno Urbano` mediante un proxy territorial.
- Periodo: 2023-2026 Q1 (anual solo 2023-2025; trimestral incluye Q1 2026 real, sin Proxy).
- Archivos DATIC: `DATIC_*_2023_2026T1_Barrio_O.geojson` (homicidios, hurtos, VIF, comparendos).

### Detalle actual de Entorno Urbano en Barrio Obrero

- La celda `3B` recalcula `REF_ENTORNO_U` con `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`.
- La base territorial usada es `Comuna 9`, como aproximacion a `Barrio Obrero`.
- El proxy combina dos componentes:
  - `Deficit Cualitativo`
  - `Deficit Cualitativo / Deficit Habitacional`
- Ambos componentes se normalizan con referencias fijas y luego se promedian.
- La celda `3C` agrega una visualizacion `heatmap` de componentes del deficit cualitativo 2024.
- Ese insumo no tiene periodicidad mensual ni trimestral observada; es un corte anual `2024`.
- `Predios titulados` y `subsidios de mejoramiento` fueron revisados, pero no hacen parte del calculo actual de esta dimension.

### Roosevelt

- `notebooks/01_itt_roosevelt.ipynb`

Estado:

- Implementado.
- Ya migrado a `ref_min/ref_max` fijos.
- Replica la estructura de Barrio Obrero, adaptada a corredor con buffer.
- Usa valores Proxy para `Entorno Urbano`, `Educacion y Desarrollo` y `Vulnerabilidad`.

### Avenida Ciudad de Cali

- `notebooks/02_itt_avenida_ciudad_de_cali.ipynb`

Estado:

- Implementado y funcional.
- Analiza 8 tramos buffer de 100 m sobre corredor vial.
- Requiere `spatial join` de eventos a tramos.
- Sigue usando min-max relativo para normalizar indicadores reales.

Conclusion importante:

- Es la principal deuda metodologica del repo.
- No debe asumirse como notebook plenamente homologado al metodo vigente.

### Pulmon de Oriente 2026

- `notebooks/04_itt_pulmon_oriente_2026_v2.ipynb`

Estado:

- No es el notebook comparativo del proyecto.
- Es una salida completa para Seguridad y Cohesion Social 2023-2026.
- 2026 solo tiene datos reales de T1; Q2, Q3 y Q4 se estiman con valores Proxy (promedio historico trimestral 2023-2025).
- Los valores Proxy se marcan con doble asterisco (`**`).
- Incluye deduplicacion automatica por fecha+coordenada.

Rol en el proyecto:

- Sirve como referencia de seguimiento con serie temporal completa (real + Proxy).
- Pulmon de Oriente tambien es la base de los valores Proxy usados por otras zonas.

### Comparativo entre zonas

- `notebooks/05_comparativo_itt_zonas.ipynb`

Estado:

- Es la plantilla comparativa real que existe hoy en disco.
- Depende de resultados exportados por zona.
- Todavia no representa un flujo consolidado totalmente maduro.

## 6. Zonas del repo y como pensarlas

### Barrio Obrero

- Unidad de analisis: poligono unico.
- No requiere `spatial join` por tramo.
- Caso mas limpio para entender la metodologia vigente.
- Caso actual mas importante para entender el uso experimental de `deficit habitacional` dentro de `Entorno Urbano`.
- Periodo: 2023-2026 (Q1 2026 real, sin Proxy).
- Analisis anual (base): solo 2023-2025 (años completos).
- Serie trimestral: incluye Q1 2026 real; NO se generan Proxy para Q2-Q4 2026.
- Archivos DATIC: `DATIC_homicidios_2023_2026T1_Barrio_O.geojson`, `DATIC_hurtos_2023_2026T1_Barrio_O.geojson`, `DATIC_violencia_intrafamiliar_2023_2026T1_Barrio_O.geojson`, `DATIC_comparendos_2023_2026T1_Barrio_O.geojson`.
- Heatmaps y barras trimestrales: gradiente claro a oscuro (2023=claro, 2026=oscuro). Trimestres sin datos (Q2-Q4 2026) muestran `-` en heatmaps con color base.
  - Seguridad: azul `['#90CAF9', '#42A5F5', '#1565C0', '#003366']`
  - Movilidad: naranja `['#FFCC80', '#FB8C00', '#E65100', '#4E2600']`
  - Cohesion: purpura `['#CE93D8', '#8E24AA', '#4A148C', '#1A0033']`
  - 2026 solo dibuja barra en Q1 (no repite en Q2-Q4).

### Roosevelt

- Unidad de analisis: corredor con buffer de 100 m.
- Periodo trabajado: `2023-2025`.
- Caso homologado a la metodologia vigente pero en contexto de corredor.

### Avenida Ciudad de Cali

- Unidad de analisis: 8 tramos.
- Metodo espacial: `spatial join`.
- Caso mas complejo espacialmente.
- Todavia no esta homologado en normalizacion.

### Pulmon de Oriente

- Funciona como referencia metodologica.
- Aporta los scores provisionales usados en otras zonas.
- Tiene notebook propio parcial 2026, pero no equivale al flujo principal de comparacion entre zonas.

## 7. Disponibilidad real de datos

### Datos presentes en el repo

Hay ZIP versionados para:

- `data/itt_roosevelt/`
- `data/itt_barrio_obrero/`
- `data/itt_pulmon_oriente/`

Estos ZIP contienen insumos reales para trabajo territorial y validan que Roosevelt, Barrio Obrero y Pulmon de Oriente si tienen base de datos local dentro del repo.

### Datos no versionados en el repo

- `data/itt_avenida_ciudad_de_cali/` tiene estructura y README, pero no trae los insumos fuente versionados.

Implicacion:

- Su ejecucion depende de carga externa, Colab o entrega manual de archivos.

## 8. Referencias territoriales y su estado actual

La carpeta `data/referencia/` contiene Excel de apoyo metodologico:

- `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`
- `BD_PREDIOS_TITULADOS 2023-2025 (1).xlsx`
- `BD_SUBSIDIOS_MEJORAMIENTO_VIV_AÑOS_2024_2025 (1).xlsx`

Lectura correcta:

- No todos hacen parte del calculo actual del ITT.
- Se consideran insumos potenciales para fortalecer `Entorno Urbano` u otras lecturas territoriales futuras.
- El candidato mas fuerte documentado hoy para `Entorno Urbano` es el deficit habitacional.
- Ese candidato ya fue incorporado de forma experimental en `03_itt_barrio_obrero.ipynb`.
- `Predios titulados` y `subsidios de mejoramiento` siguen fuera del calculo actual de la dimension.

## 9. Donde vive el conocimiento

Para responder bien sobre este repo, un agente debe leer en este orden:

1. `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`
2. `agent/context/contexto_proyecto.md`
3. `agent/context/zonas_estudio.md`
4. `docs/03_fuentes_datos.md`
5. `notebooks/03_itt_barrio_obrero.ipynb`
6. `notebooks/01_itt_roosevelt.ipynb`
7. `notebooks/02_itt_avenida_ciudad_de_cali.ipynb`

## 10. Precauciones para otro agente

- No asumir que todo notebook implementado ya esta metodologicamente homologado.
- No confundir `04_itt_pulmon_oriente_2026.ipynb` con el comparativo entre zonas.
- No asumir que `outputs/` ya contiene resultados versionados listos para consolidacion.
- Los archivos `_patch_*.py` son scripts temporales para modificar notebooks. Una vez aplicados, se eliminan del repo. No deben quedar versionados.
- Cada vez que se ajuste un notebook, actualizar tambien: .md de estructura, contexto del agente, CONSOLIDADO, script .py equivalente, y steering.
- Tratar con cuidado textos con problemas de codificacion como `año`, `T1`, o caracteres especiales en algunos `.md` y notebooks.
- Distinguir siempre entre:
  - dato observado real
  - score normalizado
  - valor Proxy
  - valor Proxy estimado (marcado con `**`)
  - resultado exportado
- No presentar el proxy de `Entorno Urbano` de Barrio Obrero como serie mensual o trimestral observada.
- Los valores Proxy de 2026 Q2-Q4 deben identificarse siempre con doble asterisco (`**`) y no deben presentarse como datos reales observados.
- Cuando se reemplacen valores Proxy por datos reales, actualizar simultaneamente todos los `.md` del proyecto.

## 11. Resumen ejecutivo para handoff rapido

Este repo ya tiene una metodologia definida y parcialmente consolidada. `Barrio Obrero` es la referencia operativa vigente (periodo 2023-2026 Q1 real, sin Proxy). `Roosevelt` ya esta alineado con esa metodologia. `Avenida Ciudad de Cali` sigue funcional, pero pendiente de migrar desde min-max relativo hacia `ref_min/ref_max` fijos. `Pulmon de Oriente` es la referencia metodologica de fondo y la fuente de los scores provisionales usados en otras zonas. Los datos versionados existen para Roosevelt, Barrio Obrero y Pulmon de Oriente, pero no para Avenida Ciudad de Cali. En Barrio Obrero, `Entorno Urbano` ya puede recalcularse con un proxy experimental de `deficit habitacional 2024` para `Comuna 9`, explicado con un `heatmap` de componentes del deficit cualitativo 2024. Barrio Obrero ahora tiene archivos DATIC con datos hasta 2026 Q1; el analisis anual usa solo 2023-2025 y la serie trimestral incluye Q1 2026 real con 4to color naranja (#FF6F00) en heatmaps y barras.

## 12. Prompt sugerido para otro agente

Puedes iniciar a otro agente con este texto:

> Este repo calcula el ITT de zonas urbanas de Cali. La metodologia vigente exige `ref_min/ref_max` fijos por indicador y esta documentada en `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`. `notebooks/03_itt_barrio_obrero.ipynb` es la referencia operativa principal; `notebooks/01_itt_roosevelt.ipynb` ya esta alineado a esa logica; `notebooks/02_itt_avenida_ciudad_de_cali.ipynb` sigue funcional pero aun usa min-max relativo y debe tratarse como implementacion pendiente de homologacion. Los valores Proxy actuales provenientes de Pulmon de Oriente son `Entorno Urbano = 39.2`, `Educacion y Desarrollo = 54.9` y `Vulnerabilidad = 54.1`, pero en Barrio Obrero `Entorno Urbano` ya puede sobrescribirse con un proxy experimental de `deficit habitacional 2024` para `Comuna 9`. Ese proxy no tiene periodicidad mensual o trimestral observada; su visualizacion adecuada hoy es el `heatmap` de componentes del deficit cualitativo 2024. Distingue siempre entre datos reales, scores provisionales y metodologia vigente. No inventes outputs no versionados ni asumas que el comparativo ya esta completo.

## 13. Escala de clasificacion del ICS (Indice de Condicion Social)

El ICS se clasifica en 8 categorias con la siguiente escala de colores y rangos numericos (usar coma como separador decimal):

| HEX | Rango | Categoria |
| :--- | :--- | :--- |
| `#FFFF99` | 0,4 - 20,0 | Bajo |
| `#B2FF66` | 20,1 - 27,0 | Moderado-Bajo |
| `#66FF33` | 27,1 - 33,1 | Moderado |
| `#4CD164` | 33,2 - 39,8 | Moderado-Alto |
| `#40A485` | 39,9 - 48,6 | Alto |
| `#2D82A6` | 48,7 - 60,6 | Muy Alto |
| `#2A4B8C` | 60,7 - 80,0 | Extremo |
| `#1A1C78` | 80,1 - 335,1 | Extremo Maximo |

Formato JSON para codigo:

```json
{
  "leyenda": "ICS",
  "configuracion_escala": [
    {"rango_min": 0.4, "rango_max": 20.0, "hex": "#FFFF99", "categoria": "Bajo"},
    {"rango_min": 20.1, "rango_max": 27.0, "hex": "#B2FF66", "categoria": "Moderado-Bajo"},
    {"rango_min": 27.1, "rango_max": 33.1, "hex": "#66FF33", "categoria": "Moderado"},
    {"rango_min": 33.2, "rango_max": 39.8, "hex": "#4CD164", "categoria": "Moderado-Alto"},
    {"rango_min": 39.9, "rango_max": 48.6, "hex": "#40A485", "categoria": "Alto"},
    {"rango_min": 48.7, "rango_max": 60.6, "hex": "#2D82A6", "categoria": "Muy Alto"},
    {"rango_min": 60.7, "rango_max": 80.0, "hex": "#2A4B8C", "categoria": "Extremo"},
    {"rango_min": 80.1, "rango_max": 335.1, "hex": "#1A1C78", "categoria": "Extremo Maximo"}
  ]
}
```

## 14. Diccionario de variables IPM (Indice de Pobreza Multidimensional)

15 variables de incidencia a nivel manzana, provenientes de `IPM - Variables (incidencias).xlsx`:

| Codigo | Descripcion | Obs |
| :--- | :--- | :--- |
| `analf_` | Analfabetismo (%) | ~9.512 manzanas |
| `bajo_` | Bajo logro educativo (%) | ~13.484 manzanas |
| `infancia_` | Barreras para servicios de cuidado de primera infancia (%) | ~6.487 manzanas |
| `inasis_` | Inasistencia escolar (%) | ~7.435 manzanas |
| `rezago_` | Rezago escolar (%) | ~12.210 manzanas |
| `trab_infan_` | Trabajo infantil (%) | ~2.662 manzanas |
| `depen_` | Dependencia economica (%) | ~13.415 manzanas |
| `infor_` | Informalidad (%) | ~13.686 manzanas |
| `salud_` | Barreras de acceso a servicios de salud (%) | ~7.932 manzanas |
| `asegu_` | Sin aseguramiento a salud (%) | ~13.187 manzanas |
| `haci_` | Hacinamiento critico (%) | ~9.228 manzanas |
| `pared_` | Material inadecuado de las paredes exteriores (%) | ~1.425 manzanas |
| `excre_` | Eliminacion inadecuada de excretas (%) | ~2.008 manzanas |
| `pisos_` | Material inadecuado de los pisos (%) | ~1.065 manzanas |
| `agua_` | Sin acceso a fuentes de agua mejorada (%) | ~1.511 manzanas |

Agrupacion por dimensiones IPM:

| Dimension | Variables |
| :--- | :--- |
| Educacion | `analf_`, `bajo_`, `infancia_`, `inasis_`, `rezago_` |
| Trabajo | `trab_infan_`, `depen_`, `infor_` |
| Salud | `salud_`, `asegu_` |
| Vivienda | `haci_`, `pared_`, `pisos_` |
| Servicios | `agua_`, `excre_` |

Variable mas critica: `infor_` (Informalidad >82% promedio).
Segunda mas critica: `bajo_` (Bajo logro educativo >37% promedio).

## 15. Notebook `02_analisis_ipm_variables.ipynb` - Estructura y cambios

20 celdas (0 markdown + 19 code). Fuente: `IPM - Variables (incidencias).xlsx`.

| Cell | Tipo | Descripcion |
| :--- | :--- | :--- |
| 0 | md | # Analisis Exploratorio de Variables IPM |
| 1 | code | Montar Google Drive (Colab) |
| 2 | code | Instalar dependencias (pandas, geopandas, matplotlib, seaborn, openpyxl) |
| 3 | code | Clonar repositorio desde GitHub |
| 4 | code | Importar librerias (`os, sys, warnings, pandas, numpy, matplotlib, seaborn, geopandas`) |
| 5 | code | Definir rutas: `BASE_DIR`, `DATA_DIR`, archivo Excel |
| 6 | code | Definir `diccionario` de 15 variables (codigo -> nombre legible) |
| 7 | code | Cargar Excel, concatenar todos los sheets en `df_ipm_vars`, renombrar columnas quitando prefijos |
| 8 | code | `df_ipm_vars.head()` |
| 9 | code | Estadisticas descriptivas (`df_ipm_vars.describe()`) |
| 10 | code | Barplot - Incidencia promedio por variable (matplotlib, ordenado descendente) |
| 11 | code | Boxplots por variable (seaborn `sns.boxplot`) |
| 12 | code | Manzanas con incidencia >0% por variable (barra horizontal) |
| 13 | code | Mapa de calor de correlacion entre variables (`sns.heatmap`) |
| 14 | code | Top 10 manzanas con mayor incidencia acumulada |
| 15 | code | Agrupacion por dimensiones (Educacion, Trabajo, Salud, Vivienda, Servicios) - boxplot comparativo |
| 16 | code | Variables mas criticas - ranking horizontal con `means.nlargest()` |
| 17 | code | **Histogramas** 2x3 de las 6 variables mas criticas (con media y mediana) |
| 18 | code | **Ranking completo** tabular con barra de color + conclusiones clave |
| 19 | code | Resumen ejecutivo (prints) |

**Cambios aplicados**: Las celdas 17-18 originales intentaban hacer merge geometrico (`cod_mzn` vs `COD_MZN`) y spatial join con comunas, pero fallaban porque los codigos manzana del Excel (24 chars) no coinciden con los del shapefile ICS (22 chars, `COD_MZN`). Se reemplazaron por analisis puramente tabular (histogramas + ranking) que no depende de geometrias. El error activo era `IndexError: index 0 out of bounds for axis 0 with size 0` en `comuna_plot.plot(kind='barh')` al obtener 0 filas del merge.
