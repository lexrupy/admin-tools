#!/bin/bash

# Verifica se um arquivo foi passado como parâmetro
if [ -z "$1" ]; then
    zenity --error --text="Você deve fornecer um arquivo .dav como parâmetro."
    exit 1
fi

input="$1"

# Verifica se o arquivo existe
if [ ! -f "$input" ]; then
    zenity --error --text="Arquivo não encontrado: $input"
    exit 1
fi

# Gera nome de saída com extensão .mp4
output="${input%.*}.mp4"

# Cria uma função que faz a conversão
convert_file() {
    ffmpeg -i "$input" -c:v copy -c:a copy "$output" 2> /dev/null
}

# Executa a conversão em background com barra pulsante
(
    convert_file
    echo "100"
) | zenity --progress \
           --pulsate \
           --no-cancel \
           --auto-close \
           --title="Conversão de Vídeo" \
           --text="Aguarde a conversão do arquivo $(basename "$input")..."

# Verifica se o comando foi bem-sucedido
if [ $? -eq 0 ]; then
    zenity --info --text="Arquivo convertido com sucesso: $(basename "$output")"
else
    zenity --error --text="Ocorreu um erro durante a conversão."
fi

