# Índice de Condición Social (ICS) — Pobreza Multidimensional

Análisis geoespacial del **Índice de Condición Social (ICS)** y su relación con el **Índice de Pobreza Multidimensional (IPM)** a nivel de manzana en el distrito de Santiago de Cali, Colombia.

## Contexto

El ICS es un proxy del nivel de ingresos de los hogares que combina **clima educativo** (años promedio de educación de miembros ≥15 años) e **índice de hacinamiento** (personas por cuarto, incluyendo sala y comedor). Su fórmula es:

```
ICS = Clima educativo / Índice de hacinamiento
```

A partir de la posición relativa de los hogares en la estructura socioeconómica distrital, se reclasifica en seis estratos:

| ICS | Categoría  | Hogares  |
|-----|------------|----------|
| 1   | Muy baja   | 10% inferior |
| 2   | Baja       | 15%      |
| 3   | Media-baja | 25%      |
| 4   | Media      | 25%      |
| 5   | Media-alta | 15%      |
| 6   | Alta       | 10% superior |

## Estructura del proyecto

```
indice_Pobreza/
├── agent/              # Contexto y base de conocimiento para agentes de IA
│   ├── context/        # Glosario, zonas de estudio, contexto del proyecto
│   ├── knowledge_base/ # Guía metodológica de referencia
│   └── prompts/        # System prompts para agentes
├── data/               # Shapefiles y GeoJSON de ICS e IPM por manzana
├── docs/               # Documentación metodológica
├── notebooks_py/       # Notebooks de exploración y análisis (Colab-ready)
├── outputs/            # Resultados y seguimiento del proyecto
├── requirements.txt
└── environment.yml
```

## Datos

Los shapefiles en `data/` contienen geometrías a nivel de **manzana** con:

- **ICS**: Índice de Condición Social y sus componentes (clima educativo, hacinamiento)
- **IPM**: Índice de Pobreza Multidimensional
- **Comunas**: División político-administrativa de Cali
- **Barrios**: Límites de barrios con indicadores sociales históricos

Sistema de referencia: MAGNA-SIRGAS / Colombia Oeste (EPSG:3115).

## Uso

### Local

```bash
conda env create -f environment.yml
conda activate indice_ingresos_operacionales
```

### Google Colab

Abrir `notebooks_py/01_exploracion_ics_ipm.ipynb` desde:

1. https://colab.research.google.com/
2. `File → Open notebook → GitHub`
3. Repositorio: `j0rg3c45/Pobreza_multidimensional_y_condicion_social`

## Referencias

- Barbary et al. (1999); Barbary & Raberono (2002); Dureau et al. (2007, 2012); Salas Vanegas (2008)
- Metodología completa en [`docs/metodologia.md`](docs/metodologia.md)
