import os
import glob
import rasterio
from rasterio.mask import mask
from rasterio.windows import from_bounds
from datetime import datetime
import fiona
import warnings
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning)

# Diretórios
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "RESULTADO")
shp_dir = os.path.join(current_dir, "SHP")
raster_dir = os.path.join(current_dir, "RASTER")

# Cria a pasta de saída se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Encontra o arquivo SHP
shp_file = glob.glob(os.path.join(shp_dir, "*.shp"))[0]

with fiona.open(shp_file, 'r') as shp:
    feature = next(iter(shp))
    polygon = feature["geometry"]
    shp_crs = shp.crs
    bounds = shp.bounds  # Obtém a extensão do shapefile

# Encontra todos os arquivos RASTER
raster_files = glob.glob(os.path.join(raster_dir, "*.tif")) + \
               glob.glob(os.path.join(raster_dir, "*.TIF")) + \
               glob.glob(os.path.join(raster_dir, "*.tiff")) + \
               glob.glob(os.path.join(raster_dir, "*.TIFF"))

# Processa cada arquivo RASTER
for raster_file in raster_files:
    with rasterio.open(raster_file) as raster:
        raster_crs = raster.crs
        if raster_crs != shp_crs:
            print(f"SRCs não coincidem! Pulando {raster_file}")
            continue

        # Obtém a resolução do raster
        res_x, res_y = raster.res
        minx, miny, maxx, maxy = bounds

        # Calcula o número de pixels para igualar a extensão do vetor
        width = int((maxx - minx) / res_x)
        height = int((maxy - miny) / abs(res_y))

        # Aplica a máscara de recorte
        out_image, out_transform = mask(raster, [polygon], crop=True, nodata=0)

        # Redimensiona para a extensão do vetor
        new_window = from_bounds(minx, miny, maxx, maxy, raster.transform)

        # Cria o arquivo de saída
        output_file = os.path.join(output_dir, os.path.basename(raster_file))
        with rasterio.open(output_file, 'w', driver='GTiff',
                           height=height, width=width,
                           count=raster.count, dtype=out_image.dtype,
                           transform=new_window, crs=raster.crs, nodata=0) as dst:
            dst.write(out_image)

        print(f"✅ Arquivo salvo: {output_file}")

print("🎯 Processamento concluído!")
