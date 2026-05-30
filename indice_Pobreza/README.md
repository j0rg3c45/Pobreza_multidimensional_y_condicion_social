# Índice de Pobreza Multidimensional (IPM) y Condición Social - Cali

Análisis geoespacial avanzado del **Índice de Pobreza Multidimensional (IPM)** y su correlación con el **Índice de Condición Social (ICS)** a nivel de manzana en el Distrito Especial de Santiago de Cali, Colombia.

Este proyecto prioriza la identificación de carencias críticas y la severidad de la pobreza en territorios estratégicos para la intervención social.

## 📍 Zonas de Estudio Prioritarias

El análisis se centra en cuatro áreas clave del desarrollo urbano y la transformación territorial:

1.  **Barrio Obrero:** Análisis de severidad en un sector histórico con alta informalidad (93.1%).
2.  **Corredor Roosevelt (Buffer 100m):** Evaluación del impacto de barreras en salud (22.7%) y servicios.
3.  **Pulmón de Oriente:** Integración de indicadores de vulnerabilidad en el sector del Oriente de Cali.
4.  **Ciudad de Cali (Referente Distrital):** Línea base comparativa que abarca los 8 tramos del corredor principal.

## 📊 Metodología y Enfoque

### IPM (Prioridad)
Se analizan 15 variables de incidencia agrupadas en dimensiones de educación, salud, vivienda y mercado laboral. El enfoque principal es el **Análisis de Severidad (IPM > 0)**, el cual promedia las carencias únicamente en los hogares que ya presentan condiciones de pobreza, permitiendo entender la profundidad de la exclusión.

### ICS (Índice de Condición Social)
Proxy del nivel de ingresos basado en el **clima educativo** y el **índice de hacinamiento**. Se utiliza para clasificar las manzanas en 6 categorías socioeconómicas y correlacionar la vulnerabilidad con el IPM.

### Estándares Técnicos
- **Accesibilidad:** Uso estricto de la paleta **Cividis** (colorblind-friendly).
- **Cartografía:** Mapas dinámicos con fondo de manzanas catastrales atenuado y contornos destacados para áreas de estudio.
- **Visualización:** Regla de contraste dinámico para etiquetas (blanco sobre color, negro sobre cero).
- **Idioma:** Español técnico colombiano y codificación UTF-8.

## 📂 Estructura del Repositorio

```
indice_Pobreza/
├── agent/              # Contexto y base de conocimiento para agentes de IA
│   ├── context/        # Glosario, zonas de estudio y reglas geoinformáticas
│   ├── knowledge_base/ # Guía ITT y Notas Metodológicas
│   └── prompts/        # Prompts especializados
├── data/               # GeoJSONs y polígonos (IPM, ICS, Manzanas, Tramos)
├── docs/               # Documentación metodológica profunda
├── notebooks_py/       # Notebooks de análisis (01-05) optimizados para Colab
├── outputs/            # Mapas, reportes y estadísticas consolidadas
├── requirements.txt
└── environment.yml
```

## 🚀 Notebooks Principales

- `01_exploracion_ics_ipm.ipynb`: Análisis global, promedios por comuna y mapas de corredores unificados.
- `03_indice_vulnerabilidad_multidimensional.ipynb`: Cálculo del IVM (ICS + IPM).
- `04_mapeo_ipm_roosevelt.ipynb`: Cartografía detallada del sector Roosevelt.
- `05_mapeo_ipm_barrio_obrero.ipynb`: Cartografía detallada del Barrio Obrero (16 manzanas).

## 🛠️ Uso

### Local (con `uv` o `conda`)
```bash
# Recomendado: uv
uv run jupyter notebook
```

### Google Colab
Abrir los notebooks directamente desde el repositorio de GitHub: `j0rg3c45/Pobreza_multidimensional_y_condicion_social`.

---
*Desarrollado como parte del proyecto de Gobierno de Datos y Data Stewardship para el análisis de la pobreza en Cali.*
