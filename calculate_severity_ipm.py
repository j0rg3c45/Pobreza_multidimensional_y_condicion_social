
import pandas as pd
import geopandas as gpd

# Rutas de datos maestros
PATH_IPM_VARS = 'indice_Pobreza/data/IPM_GEO/Mzn_ipm_variables.shp'
PATH_ICS = 'indice_Pobreza/data/Mzn_ics.shp'

# Rutas de polígonos de estudio
PATH_POLY_BO = 'indice_Pobreza/data/Geojson_Barrio_Obrero/Geojson_Barrio_Obrero_cambioArea.geojson'
PATH_POLY_RV = 'indice_Pobreza/data/Geojson_Roosevelt/tramos_Roosevelt_Buffer_100.geojson'

# Columnas de interés (estandarizadas de Shapefile)
COLS = ['ANALF_', 'BAJO_', 'INFANCIA_', 'INASIS_', 'REZAGO_', 'TRAB_INFAN', 
        'DEPEN_', 'INFOR_', 'SALUD_', 'ASEGU_', 'HACI_', 'PARED_', 
        'EXCRE_', 'PISOS_', 'AGUA_', 'ipm']

def get_severity_stats(gdf):
    # Solo manzanas con IPM > 0
    gdf_filtered = gdf[gdf['ipm'] > 0]
    return gdf_filtered[COLS].mean(), len(gdf_filtered)

# 1. Cargar datos maestros
print("Cargando datos maestros...")
gdf_vars = gpd.read_file(PATH_IPM_VARS)
gdf_ics = gpd.read_file(PATH_ICS)

# 2. Identificar Urbana/Rural
gdf_vars['COD_DANE'] = gdf_vars['COD_DANE'].astype(str)
gdf_ics['cod_dane_a'] = gdf_ics['cod_dane_a'].astype(str)
full_cali = gdf_vars.merge(gdf_ics[['cod_dane_a', 'ZONA']], left_on='COD_DANE', right_on='cod_dane_a', how='left')

# 3. Cargar polígonos y realizar Spatial Join para asegurar que usamos los datos del maestro
print("Procesando zonas de estudio...")
poly_bo = gpd.read_file(PATH_POLY_BO).to_crs(gdf_vars.crs)
poly_rv = gpd.read_file(PATH_POLY_RV).to_crs(gdf_vars.crs)

# Spatial Join (manzanas dentro de los polígonos)
# Usamos 'centroid' para evitar problemas con manzanas que tocan el borde
gdf_vars_centroid = gdf_vars.copy()
gdf_vars_centroid['geometry'] = gdf_vars_centroid.centroid

gdf_bo = gpd.sjoin(gdf_vars_centroid, poly_bo, predicate='within')
# Volvemos a la geometría original si es necesario, pero para medias no importa
gdf_bo = gdf_vars.loc[gdf_bo.index]

gdf_rv = gpd.sjoin(gdf_vars_centroid, poly_rv, predicate='within')
gdf_rv = gdf_vars.loc[gdf_rv.index]

# 4. Calcular Estadísticas
stats_urb, n_urb = get_severity_stats(full_cali[full_cali['ZONA'] == 'Urbana'])
stats_rur, n_rur = get_severity_stats(full_cali[full_cali['ZONA'] == 'Rural'])
stats_bo, n_bo = get_severity_stats(gdf_bo)
stats_rv, n_rv = get_severity_stats(gdf_rv)

# 5. Formatear y mostrar
df_res = pd.DataFrame({
    'Cali Urbana': stats_urb,
    'Cali Rural': stats_rur,
    'Barrio Obrero': stats_bo,
    'Roosevelt': stats_rv
})

print(f"\n--- CONTEO DE MANZANAS (IPM > 0) ---")
print(f"Cali Urbana: {n_urb} | Cali Rural: {n_rur} | Barrio Obrero: {n_bo} | Roosevelt: {n_rv}")
print("\n--- PROMEDIOS DE SEVERIDAD (IPM > 0) ---")
print(df_res.round(2))

# Guardar a CSV para referencia
df_res.to_csv('comparativa_severidad_ipm.csv')
