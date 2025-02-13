import os
import glob
import rasterio
from rasterio.mask import mask
from datetime import datetime
import fiona
import warnings
import numpy as np
warnings.filterwarnings("ignore", category=UserWarning)


# Define o diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Diretório atual: {current_dir} - {datetime.now()}")

# Define o diretório de saída
output_dir = os.path.join(current_dir, "RESULTADO")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print(f"Diretório de saída: {output_dir} - {datetime.now()}")

# Define o diretório de entrada SHP
shp_dir = os.path.join(current_dir, "SHP")
print(f"Diretório SHP: {shp_dir} - {datetime.now()}")

# Define o diretório de entrada RASTER
raster_dir = os.path.join(current_dir, "RASTER")
print(f"Diretório RASTER: {raster_dir} - {datetime.now()}")

# Encontra o arquivo SHP
shp_file = glob.glob(os.path.join(shp_dir, "*.shp"))[0]
print(f"Arquivo SHP encontrado: {shp_file} - {datetime.now()}")

with fiona.open(shp_file, 'r') as shp:
    # Lê a geometria do polígono
    feature = next(iter(shp))
    polygon = feature.geometry
    print(f"Geometria do polígono: {polygon} - {datetime.now()}")

    # Imprime o SRC do polígono
    print(f"SRC do polígono: {shp.crs} - {datetime.now()}")
# Encontra todos os arquivos RASTER
raster_files = glob.glob(os.path.join(raster_dir, "*.tiff")) + \
               glob.glob(os.path.join(raster_dir, "*.TIFF")) + \
               glob.glob(os.path.join(raster_dir, "*.tif")) + \
               glob.glob(os.path.join(raster_dir, "*.TIF"))
print(f"Arquivos RASTER encontrados: {len(raster_files)} - {datetime.now()}")

# Processa cada arquivo RASTER
for raster_file in raster_files:
    print(f"Processando arquivo RASTER: {raster_file} - {datetime.now()}")

    # Abre o arquivo RASTER
    with rasterio.open(raster_file) as raster:
        # Imprime o SRC do RASTER
        print(f"SRC do RASTER: {raster.crs} - {datetime.now()}")

        # Verifica se os SRCs são iguais
        if raster.crs != shp.crs:
            print(f"SRCs não são iguais! - {datetime.now()}")
            continue

        # Recorta o RASTER pelo polígono
        out_image, out_transform = mask(raster, [polygon], crop=True)
        out_image = np.where(out_image == -9999, 0, out_image)
        print(f"Recorte realizado com sucesso - {datetime.now()}")

        # Cria o nome do arquivo de saída
        output_file = os.path.join(output_dir, os.path.basename(raster_file))
        print(f"Arquivo de saída: {output_file} - {datetime.now()}")

        # Salva o arquivo de saída
        with rasterio.open(output_file, 'w', driver='GTiff',
                           height=out_image.shape[1], width=out_image.shape[2],
                           count=out_image.shape[0], dtype=out_image.dtype,
                           nodata=0) as dst:
            dst.write(out_image)
            dst.crs = raster.crs
            dst.transform = out_transform
        print(f"Arquivo de saída salvo com sucesso - {datetime.now()}")

print(f"Processamento concluído com sucesso - {datetime.now()}")