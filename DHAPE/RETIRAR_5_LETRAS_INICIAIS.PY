import os

# Diretório da pasta atual
dir_atual = os.getcwd()

# Nome do script
nome_script = os.path.basename(__file__)

# Lista todos os arquivos no diretório atual
arquivos = os.listdir(dir_atual)

# Itera sobre cada arquivo
for arquivo in arquivos:
    # Verifica se o item é um arquivo (não uma pasta) e não é o script atual
    if os.path.isfile(os.path.join(dir_atual, arquivo)) and arquivo != nome_script:
        # Verifica se o arquivo tem pelo menos 5 caracteres no nome
        if len(arquivo) > 5:
            # Renomeia o arquivo, removendo as primeiras 5 letras
            os.rename(os.path.join(dir_atual, arquivo), os.path.join(dir_atual, arquivo[5:]))

print("Arquivos renomeados com sucesso!")
