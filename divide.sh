#!/bin/bash

# Ativar o ambiente virtual (virtualenv)
source .venv/bin/activate

# Solicitar ao usuário que insira o nome do arquivo PDF
read -p "Arraste o arquivo PDF aqui: " PDF_FILE

# Remover as aspas simples do nome do arquivo PDF
PDF_FILE="${PDF_FILE//\'}"
# Executar o script Python com o arquivo PDF como argumento
python divide.py "$PDF_FILE"

# Desativar o ambiente virtual após a execução do script Python
deactivate
