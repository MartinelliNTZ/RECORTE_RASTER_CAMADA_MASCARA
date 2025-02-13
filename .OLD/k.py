from qgis.core import QgsProject, QgsLayoutExporter, QgsLayoutItemLabel
from qgis.PyQt.QtCore import QDateTime
import os
import pandas as pd

# Definir variáveis
pasta_raiz = "C:\PYTHON_TESTES\IMPRESSAO_FERTILIDADE"
talhao = 'SR01'
ano = '2024'
raster_directory = os.path.join(pasta_raiz, "raster")
log_directory = os.path.join(pasta_raiz, "log")
output_directory = os.path.join(pasta_raiz, "saidas")

# Criar diretórios de log e saída se não existirem
os.makedirs(log_directory, exist_ok=True)
os.makedirs(output_directory, exist_ok=True)

# Criar log
log_file_name = f"log_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmm')}.txt"
log_file_path = os.path.join(log_directory, log_file_name)

# Hora inicial
start_time = QDateTime.currentDateTime()
with open(log_file_path, 'w') as log_file:
    log_file.write(f"Início do script: {start_time.toString()}\n")

# Carregar a planilha com os dados dos rasters
planilha_path = os.path.join(raster_directory, "MEDIAS_RASTER.xlsx")
df = pd.read_excel(planilha_path)

# Carrega o projeto atual
project = QgsProject.instance()
layouts = project.layoutManager().layouts()

not_found = []
total_files = 0

# Processa cada arquivo raster na pasta
for index, row in df.iterrows():
    total_files += 1
    arquivo = row['Arquivo']
    tipo_mapa = os.path.splitext(arquivo)[0]  # Nome do arquivo sem extensão
    tipo_mapa_ano = f"Mapa de {tipo_mapa} - Ano {ano}"

    # Atualiza as variáveis de mínima, máxima e média
    minimo = f"Minimo: {row['Minimo']:.2f}"
    maximo = f"Maximo: {row['Maximo']:.2f}"
    media = f"Media: {row['Media']:.2f}"
    empresa_fazenda_talhao = f"Rodolfo Schlatter - Faz. Santana Rios - {talhao}"

    # Verifica se o layout existe
    layout_found = False
    for layout in layouts:
        if f"_{tipo_mapa}_" in layout.name():
            layout_found = True
            
            # Atualiza o nome do layout
            new_layout_name = f"{talhao}_MAPA_DE_{tipo_mapa}_{ano}"
            layout.setName(new_layout_name)
            print(f"Layout encontrado e renomeado para: {new_layout_name}")

            # Função para atualizar o texto do rótulo pela parte fixa do texto
            def update_label_by_fixed_text(layout, fixed_text, new_text):
                for item in layout.items():
                    if isinstance(item, QgsLayoutItemLabel) and fixed_text in item.text():
                        item.setText(new_text)
                        item.adjustSizeToText()
                        print(f"Atualizando rótulo: '{item.text()}' para '{new_text}'")
                        break

            # Atualiza os rótulos com os novos valores
            update_label_by_fixed_text(layout, "Rodolfo Schlatter - Faz. Santana Rios", empresa_fazenda_talhao)
            update_label_by_fixed_text(layout, "Mapa de", tipo_mapa_ano)
            update_label_by_fixed_text(layout, "Minimo:", minimo)
            update_label_by_fixed_text(layout, "Maximo:", maximo)
            update_label_by_fixed_text(layout, "Media:", media)  # Atualiza o rótulo de média
            update_label_by_fixed_text(layout, "Área:", "Área: 165,74 ha | Amostras: 43 | Grid: 4 hectares")  # Substitua conforme necessário
            update_label_by_fixed_text(layout, "Laboratorio:", "Laboratorio: LabSolo UFT | Camada: 00-20cm")  # Substitua conforme necessário
            update_label_by_fixed_text(layout, "Elaborado em:", f"Elaborado em: {QDateTime.currentDateTime().toString('dd/MM/yyyy')}")
            update_label_by_fixed_text(layout, "Responsável Técnico:", "Responsável Técnico: Matheus A. S. Martinelli")  # Substitua conforme necessário
            update_label_by_fixed_text(layout, "Dep. de GEO (Coords. Fabiano Muller)", "Dep. de GEO (Coords. Fabiano Muller)")  # Substitua conforme necessário
            update_label_by_fixed_text(layout, "Sistema de coordenadas - SIRGAS 2000", "Sistema de coordenadas - SIRGAS 2000")  # Substitua conforme necessário

            # Define o caminho para salvar o arquivo
            output_pdf = os.path.join(output_directory, f"{new_layout_name}.pdf")
            output_png = os.path.join(output_directory, f"{new_layout_name}.png")
            
            # Exporta o layout para um arquivo PDF
            exporter = QgsLayoutExporter(layout)
            result_pdf = exporter.exportToPdf(output_pdf, QgsLayoutExporter.PdfExportSettings())

            # Verifica se a exportação para PDF foi bem-sucedida
            if result_pdf == QgsLayoutExporter.Success:
                print(f"Exportação para PDF bem-sucedida: {output_pdf}")
            else:
                print("Erro ao exportar para PDF.")

            # Exporta o layout para um arquivo PNG
            result_png = exporter.exportToImage(output_png, QgsLayoutExporter.ImageExportSettings())

            # Verifica se a exportação para PNG foi bem-sucedida
            if result_png == QgsLayoutExporter.Success:
                print(f"Exportação para PNG bem-sucedida: {output_png}")
            else:
                print("Erro ao exportar para PNG.")
            break

    if not layout_found:
        not_found.append(tipo_mapa)

# Hora de saída
end_time = QDateTime.currentDateTime()
with open(log_file_path, 'a') as log_file:
    log_file.write(f"Layouts não encontrados: {', '.join(not_found)}\n")
    log_file.write(f"Fim do script: {end_time.toString()}\n")
    log_file.write(f"Total de arquivos processados: {total_files}\n")

print("Processamento concluído.")
