# Contexto para agente - Proyecto ITT

Este agente apoya consulta, interpretacion y explicacion del **Indice de Transformacion Territorial (ITT)** dentro del repositorio `itt-transformacion-territorial`.

## Objetivo del proyecto

Calcular el ITT para zonas de intervencion urbana en Cali y comparar resultados entre zonas.

## Zonas del repo

- ITT Roosevelt.
- Avenida Ciudad de Cali.
- Barrio Obrero.

## Estado actual

- `01_itt_roosevelt.ipynb`: implementado con estructura homologada a Barrio Obrero y `ref_min/ref_max` fijos.
- `02_itt_avenida_ciudad_de_cali.ipynb`: implementado, pero aun usa min-max relativo en la normalizacion de indicadores reales.
- `03_itt_barrio_obrero.ipynb`: implementado y alineado con `ref_min/ref_max` fijos. Periodo 2023-2026 (Q1 2026 real, sin Proxy).
- `04_itt_pulmon_oriente_2026.ipynb`: salida parcial de seguimiento.
- `05_comparativo_itt_zonas.ipynb`: plantilla comparativa.

## Regla metodologica para agentes

La referencia metodologica vigente del proyecto esta en:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`

Los agentes deben asumir como correcto:

- Uso de `ref_min/ref_max` fijos.
- Referentes provisionales para dimensiones sin datos propios.
- Necesidad de escalar refs segun tamano de zona.

Los agentes no deben asumir como vigente:

- Min-max relativo como metodo recomendado general.

## Uso esperado por el agente

El agente debe diferenciar entre:

- Metodologia vigente.
- Implementacion ya migrada.
- Implementacion pendiente de migrar.
- Datos presentes en el repo.
- Datos esperados pero no versionados.

## Seguimiento reciente

- Roosevelt ya dispone de datos fuente en `data/itt_roosevelt/`.
- Se revisaron errores de consistencia por `ano` y `año`; la convencion vigente en Roosevelt es `año`.
- Se agregaron Excel de vivienda en `data/referencia/` para evaluar si `Entorno Urbano` puede dejar de depender de un referente fijo.
- `03_itt_barrio_obrero.ipynb` ya usa experimentalmente `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx` para recalcular `Entorno Urbano` con `Comuna 9` como proxy territorial.
- Barrio Obrero ahora tiene datos DATIC hasta 2026 Q1: `DATIC_homicidios_2023_2026T1_Barrio_O.geojson`, `DATIC_hurtos_2023_2026T1_Barrio_O.geojson`, `DATIC_violencia_intrafamiliar_2023_2026T1_Barrio_O.geojson`, `DATIC_comparendos_2023_2026T1_Barrio_O.geojson`.
- Barrio Obrero: analisis anual solo 2023-2025; serie trimestral incluye Q1 2026 real; NO usa Proxy para Q2-Q4 2026.
- Barrio Obrero: heatmaps y barras trimestrales con gradiente claro a oscuro por dimension. Trimestres sin datos (Q2-Q4 2026) muestran `-` en heatmaps. 2026 solo barra en Q1.
  - Seguridad: azul `['#90CAF9', '#42A5F5', '#1565C0', '#003366']`
  - Movilidad: naranja `['#FFCC80', '#FB8C00', '#E65100', '#4E2600']`
  - Cohesion: purpura `['#CE93D8', '#8E24AA', '#4A148C', '#1A0033']`
- Ese insumo de `Entorno Urbano` es un corte anual `2024`; la visualizacion reciente recomendada es un `heatmap` de componentes del deficit cualitativo.
- Para Pulmon de Oriente 2026, se implemento deduplicacion por fecha+coordenada y generacion de valores Proxy para Q2, Q3 y Q4 basados en promedio historico trimestral 2023-2025.
- Los valores Proxy se marcan con doble asterisco (`**`) en todas las salidas.
- Referencia metodologica completa: `docs/05_nota_metodologica_proxy_2026.md`.
- **Nuevo:** `notebooks_py/03_indice_vulnerabilidad_multidimensional.ipynb` calcula el IVM (Indice de Vulnerabilidad Multidimensional) por manzana combinando ICS + IPM + 15 variables IPM. Usa ref_min/ref_max fijos, paleta Okabe-Ito, heatmaps cividis, graficas linea+relleno. Exporta GeoJSON y CSV por comuna.
- **Nuevo:** `notebooks_py/04_mapeo_ipm_roosevelt.ipynb` genera mapas geoespaciales de las 5 variables IPM mas criticas en el corredor Roosevelt (Buffer 100m). Usa escala semantica de 8 categorias con paleta cividis (accesible daltonismo), fondo de manzanas catastrales, poligono del area de estudio destacado, y celda de descarga del GeoJSON via Colab.
- **Nuevo:** `notebooks_py/05_mapeo_ipm_barrio_obrero.ipynb` genera mapas geoespaciales de las 5 variables IPM mas criticas en Barrio Obrero. Misma estructura que Roosevelt. Usa el nuevo poligono `Geojson_Barrio_Obrero_cambioArea.geojson` (16 manzanas).
- **Nuevo:** `notebooks_py/08_mapeo_ipm_ciudad_paraiso.ipynb` genera mapas geoespaciales de las 5 variables IPM mas criticas en Ciudad Paraiso, mas un mapa de ICS. Replica el Estandar Maestro de Mapeo (notebook 04 Roosevelt). Usa SOLO fuentes GeoJSON (IPM, ICS, manzanas catastrales, poligono). Filtra 33 manzanas IPM y 33 ICS por centroide dentro del poligono `poligono_ciudad_Paraiso.geojson`, cruza IPM<->ICS por `COD_MZN` y exporta `outputs/ciudad_paraiso/IPM_ciudad_paraiso.geojson` e `ICS_ciudad_paraiso.geojson`. IPM global promedio = 26.52, ICS promedio = 23.07.
- **Cambio de poligono Barrio Obrero:** Todos los notebooks (01, 03, 05) ahora usan `Geojson_Barrio_Obrero_cambioArea.geojson` en vez del poligono original. La nueva area incluye 16 manzanas IPM (antes 9).
- **Paletas accesibles daltonismo:** Se utilizan paletas optimizadas (Colorblind-friendly). La paleta **Viridis** es el estándar para el IPM, mientras que **Cividis** se utiliza para el ICS para permitir una diferenciación visual clara en mapas comparativos.
- **Nuevo:** El `notebooks_py/02_analisis_ipm_variables.ipynb` fue actualizado para incluir un **Análisis de Severidad (IPM > 0)**. Este cálculo promedia las 15 variables de incidencia únicamente en manzanas que presentan pobreza, permitiendo entender la profundidad de la carencia en los hogares afectados.
- **IPM Global comparativo (Severidad IPM > 0):** Cali Urbana = 15.28, Cali Rural = 38.33, Barrio Obrero = 13.18 (11 mzn con dato), Roosevelt = 7.51 (21 mzn con dato).
- **Hallazgo crítico Barrio Obrero:** Presenta una severidad de **Informalidad del 93.1%**, superando el promedio urbano.
- **Hallazgo crítico Roosevelt:** Presenta una severidad de **Sin Aseguramiento en Salud del 22.7%**, superando el promedio urbano.
- **Brecha Rural:** La severidad rural es crítica en infraestructura básica (Eliminación de excretas: 41.9% y Agua mejorada: 27.0%).
- **Correccion escala IPM (tope 335.1 -> 100.0):** Se valido con los datos (`Mzn_ipm_variables.geojson`) que el IPM va de 0 a 100 (max real = 100.0 en 58 manzanas; 0 manzanas > 100). El valor `335.1` que aparecia como tope de la ultima categoria ("Extremo Maximo") era un error: corresponde al rango maximo del ICS (clima educativo / hacinamiento, que si puede superar 100), copiado por error a la escala del IPM. Se corrigio a `80.1 - 100.0` en los notebooks de mapas `05_mapeo_ipm_barrio_obrero`, `06_mapeo_ipm_pulmon_oriente`, `07_mapeo_ipm_ciudad_de_cali` (el `08_mapeo_ipm_ciudad_paraiso` ya estaba en 100.0) y en la documentacion (`docs/contexto_ipm_ics.md`, `contexto_agente_master.md` secciones 14 y 17.3). Los 4 notebooks fueron re-ejecutados sin errores. NO se toco el `335.1` del notebook `03_indice_vulnerabilidad_multidimensional` porque alli describe correctamente el rango del ICS.
- **Analisis de atipicos IPM (validado):** Por metodo IQR, limite superior Q3+1.5*IQR = 42.75; 673 manzanas (4.30%) lo superan. Son valores altos pero validos (zonas muy pobres reales), no errores de dato. Distribucion: <=33.3 = 9840 mzn, 33.3-50 = 796, 50-80 = 300, 80-100 = 90, >100 = 0.
- **IPM de Cali urbano:** La fila "Cali" de las tablas comparativas se corrigio para representar SOLO la zona urbana (antes incluia todo el distrito). Filtrando manzanas con `ZONA='Urbana'` (cruce con GeoJSON ICS): 12.787 manzanas, IPM promedio = 12.59 (severidad urbana >0 = 15.28). El valor anterior 16.60 era la severidad del total del distrito.
- **Doc interpretacion IPM:** `docs/contexto_ipm_ics.md` incluye seccion "2b. Como se interpreta el valor del IPM" (analogia tasa de reprobados, truco de las dos etapas 33% vs IPM final, y escala de referencia estandar Colombia urbana de 4 niveles). Las tablas comparativas IPM se simplificaron a `Zona | Manzanas | IPM Promedio` (sin columnas de severidad, min, max).
