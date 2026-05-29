
import os
from datetime import datetime
import pandas as pd
import geopandas as gpd

# Rutas de datos maestros
PATH_IPM_VARS = 'indice_Pobreza/data/geojson_ipm/Mzn_ipm_variables.geojson'
PATH_ICS = 'indice_Pobreza/data/geojosn_ICS/ics_mzn.geojson'
DIR_POLYS = 'indice_Pobreza/data/geojson_poligonos_territorio_ITT'

# Sistema de Referencia de Coordenadas (CRS) para cálculos de área en Colombia
# MAGNA-SIRGAS / Origen Nacional (EPSG:9377)
CRS_PROYECTADO = "EPSG:9377"

# Columnas de interés (estandarizadas)
COLS = ['ANALF_', 'BAJO_', 'INFANCIA_', 'INASIS_', 'REZAGO_', 'TRAB_INFAN', 
        'DEPEN_', 'INFOR_', 'SALUD_', 'ASEGU_', 'HACI_', 'PARED_', 
        'EXCRE_', 'PISOS_', 'AGUA_', 'ipm']

def get_severity_stats(gdf):
    # Solo manzanas con IPM > 0
    gdf_filtered = gdf[gdf['ipm'] > 0]
    if len(gdf_filtered) == 0:
        return pd.Series(0.0, index=COLS), 0
    return gdf_filtered[COLS].mean(), len(gdf_filtered)

# 1. Cargar datos maestros
print("Cargando datos maestros...")
gdf_vars = gpd.read_file(PATH_IPM_VARS)
gdf_ics = gpd.read_file(PATH_ICS)

# 2. Identificar Urbana/Rural
gdf_vars['COD_DANE'] = gdf_vars['COD_DANE'].astype(str)
gdf_ics['cod_dane_a'] = gdf_ics['cod_dane_a'].astype(str)
full_cali = gdf_vars.merge(gdf_ics[['cod_dane_a', 'ZONA']], left_on='COD_DANE', right_on='cod_dane_a', how='left')

# Pre-calcular centroides para spatial join
gdf_vars_centroid = gdf_vars.copy()
gdf_vars_centroid['geometry'] = gdf_vars_centroid.centroid

results_stats = {}
results_counts = {}
results_areas = []

# 3. Calcular para Cali Urbana y Rural (Línea Base)
stats_urb, n_urb = get_severity_stats(full_cali[full_cali['ZONA'] == 'Urbana'])
stats_rur, n_rur = get_severity_stats(full_cali[full_cali['ZONA'] == 'Rural'])
results_stats['Cali Urbana'] = stats_urb
results_counts['Cali Urbana'] = n_urb
results_stats['Cali Rural'] = stats_rur
results_counts['Cali Rural'] = n_rur

# 4. Procesar polígonos de estudio dinámicamente
print("Procesando zonas de estudio ITT y calculando áreas...")
poly_files = [f for f in os.listdir(DIR_POLYS) if f.endswith('.geojson')]
all_tramos_cc = []

for file in sorted(poly_files):
    path = os.path.join(DIR_POLYS, file)
    name = file.replace('poligono_', '').replace('.geojson', '').replace('_Buffer_100', '').replace('_', ' ').title()
    
    poly = gpd.read_file(path).to_crs(gdf_vars.crs)
    
    # Cálculo de área proyectada
    poly_projected = poly.to_crs(CRS_PROYECTADO)
    area_m2 = poly_projected.area.sum()
    area_ha = area_m2 / 10000
    
    results_areas.append({'Zona/Tramo': name, 'Área (m2)': area_m2, 'Área (Ha)': area_ha})
    
    gdf_zone = gpd.sjoin(gdf_vars_centroid, poly, predicate='within')
    gdf_zone_full = gdf_vars.loc[gdf_zone.index]
    
    stats, n = get_severity_stats(gdf_zone_full)
    results_stats[name] = stats
    results_counts[name] = n
    
    if 'Ciudad De Cali T' in name:
        all_tramos_cc.append(poly)

# 5. Consolidado Ciudad de Cali
if all_tramos_cc:
    print("Calculando consolidado Ciudad de Cali...")
    gdf_cc_combined = pd.concat(all_tramos_cc)
    cc_combined_projected = gdf_cc_combined.to_crs(CRS_PROYECTADO)
    area_cc_m2 = cc_combined_projected.area.sum()
    area_cc_ha = area_cc_m2 / 10000
    
    results_areas.append({'Zona/Tramo': 'Ciudad De Cali (Total)', 'Área (m2)': area_cc_m2, 'Área (Ha)': area_cc_ha})
    
    gdf_cc_total = gpd.sjoin(gdf_vars_centroid, gdf_cc_combined, predicate='within')
    gdf_cc_total = gdf_cc_total[~gdf_cc_total.index.duplicated(keep='first')]
    gdf_cc_full = gdf_vars.loc[gdf_cc_total.index]
    
    stats_cc, n_cc = get_severity_stats(gdf_cc_full)
    results_stats['Ciudad De Cali (Total)'] = stats_cc
    results_counts['Ciudad De Cali (Total)'] = n_cc

# 6. Preparación de Reportes
df_areas = pd.DataFrame(results_areas).round(2).sort_values(by='Zona/Tramo')
df_res = pd.DataFrame(results_stats).round(2)

# 7. Guardar y Finalizar
output_dir = 'indice_Pobreza/outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

reporte_path = os.path.join(output_dir, 'reporte_consolidado_pobreza_y_areas.txt')
csv_ipm_path = os.path.join(output_dir, 'comparativa_severidad_ipm_itt_completa.csv')
csv_areas_path = os.path.join(output_dir, 'resumen_areas_territorios_itt.csv')

with open(reporte_path, 'w', encoding='utf-8') as f:
    f.write("=====================================================================\n")
    f.write("REPORTE CONSOLIDADO: POBREZA MULTIDIMENSIONAL Y ÁREAS TERRITORIALES\n")
    f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=====================================================================\n\n")
    
    f.write("1. RESUMEN DE ÁREAS GEOGRÁFICAS\n")
    f.write("---------------------------------------------------------------------\n")
    f.write("Proyección: Magna-SIRGAS / Origen Nacional (EPSG:9377)\n\n")
    f.write(df_areas.to_string(index=False, justify='left', formatters={
        'Área (m2)': '{:,.2f}'.format,
        'Área (Ha)': '{:,.2f}'.format
    }))
    f.write("\n\n")
    
    f.write("2. CONTEO DE MANZANAS CON SEVERIDAD (IPM > 0)\n")
    f.write("---------------------------------------------------------------------\n")
    for zone, count in results_counts.items():
        if count > 0:
            f.write(f"{zone:.<35} {count} manzanas\n")
    f.write("\n")
    
    f.write("3. ESTADÍSTICAS DE SEVERIDAD (PROMEDIOS IPM > 0)\n")
    f.write("---------------------------------------------------------------------\n")
    f.write("Nota: Los valores representan el porcentaje de privación en cada dimensión.\n\n")
    f.write(df_res.T.to_string())
    f.write("\n\n=====================================================================\n")
    f.write("Fin del Reporte\n")

df_res.to_csv(csv_ipm_path, float_format='%.2f')
df_areas.to_csv(csv_areas_path, index=False, float_format='%.2f')

print(f"\nReportes generados con éxito en la carpeta '{output_dir}':")
print(f"- {os.path.basename(reporte_path)} (Lectura humana)")
print(f"- {os.path.basename(csv_ipm_path)}")
print(f"- {os.path.basename(csv_areas_path)}")
