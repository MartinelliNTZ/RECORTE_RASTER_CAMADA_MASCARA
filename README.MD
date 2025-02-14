# Recorte de Rasters Usando Máscara Vetorial

Este script Python realiza o recorte de arquivos raster (.tif, .tiff) usando um arquivo vetorial no formato Shapefile (.shp) contendo polígonos. O script garante que os dados sejam processados corretamente e gera novos arquivos raster recortados na pasta de saída.

## 📌 Funcionalidades
- Identifica e carrega automaticamente arquivos raster e um shapefile contendo polígonos.
- Verifica se os sistemas de referência espacial (SRC) são compatíveis.
- Recorta os rasters de acordo com o polígono do shapefile.
- Salva os rasters recortados em uma pasta específica.

## 🛠 Bibliotecas Necessárias
Antes de rodar o script, certifique-se de que as seguintes bibliotecas estão instaladas:

```bash
pip install rasterio fiona numpy
```

## 📂 Estrutura de Diretórios
O script espera que os arquivos estejam organizados da seguinte forma:
```
|-- Pasta_do_Script
    |-- RASTER          # Contém os arquivos raster (.tif, .tiff)
    |-- SHP             # Contém o arquivo shapefile (.shp) com os polígonos
    |-- RESULTADO       # Pasta onde os rasters recortados serão salvos
```

## 🚀 Como Usar
1. **Coloque os arquivos raster na pasta** `RASTER`.
2. **Adicione o shapefile poligonal na pasta** `SHP`.
3. **Certifique-se de que todos os arquivos estão no mesmo SRC (Sistema de Referência de Coordenadas).**
4. **Limpe a pasta `RESULTADO`** (caso tenha arquivos antigos).
5. **Execute o script:**

```bash
python recortar_raster_v*.py
```

## ⚠️ Observações
- O script processa apenas o primeiro arquivo `.shp` encontrado na pasta `SHP`.
- Se os sistemas de referência do shapefile e dos rasters forem diferentes, o raster será ignorado.
- Os arquivos resultantes terão os mesmos nomes dos rasters originais, mas recortados de acordo com o polígono.

## 📝 Exemplo de Saída
```
Diretório atual: /caminho/para/o/script - 2025-02-13 10:00:00
Arquivo SHP encontrado: SHP/limite_talhao.shp - 2025-02-13 10:00:02
Arquivos RASTER encontrados: 3 - 2025-02-13 10:00:05
Processando arquivo RASTER: RASTER/mapa_umidade.tif - 2025-02-13 10:00:08
Recorte realizado com sucesso - 2025-02-13 10:00:12
Arquivo de saída salvo: RESULTADO/mapa_umidade.tif - 2025-02-13 10:00:15
Processamento concluído com sucesso - 2025-02-13 10:00:20
```

## 📄 Licença
Este projeto é de código aberto e pode ser usado livremente para fins educacionais e comerciais.

