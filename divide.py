import PyPDF2
import re
from datetime import datetime
import locale
import sys
import os
import tkinter as tk
from tkinter import simpledialog, messagebox


locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


def extrair_data_pagina(pagina):
    # Extrair texto da página
    texto = pagina.extract_text()

    # Procurar por uma data no texto usando RegExp
    padrao = (
        r"(?i)(?:"
        r"(?:(?:segunda|terça|quarta|quinta|sexta|sábado|domingo)[-,\s])?"
        r"\d{1,2} de "
        r"(janeiro|fevereiro|março|abril|maio|"
        r"junho|julho|agosto|setembro|outubro|"
        r"novembro|dezembro)"
        r" de \d{4})"
    )
    match = re.search(padrao, texto)

    if match:
        data = match.group(0)
        return data
    else:
        return ""


def dividir_pdf_em_pares(input_pdf_path, prefixo=""):
    with open(input_pdf_path, "rb") as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        num_paginas = len(pdf_reader.pages)

        for i in range(0, num_paginas, 2):
            if i + 1 < num_paginas:
                texto_data = extrair_data_pagina(pdf_reader.pages[i])
                if texto_data:
                    try:
                        # Tentar converter o texto da data em um objeto
                        # datetime
                        data = datetime.strptime(texto_data, "%d de %B de %Y")
                    except ValueError:
                        # Em caso de falha na conversão, ignore esta página
                        continue

                    # Se a conversão for bem-sucedida, use a data para nomear
                    # o arquivo

                    output_pdf_path = os.path.join(
                        os.path.dirname(input_pdf_path),
                        f"{prefixo} {data.strftime('%d%b%y').upper()}.pdf",
                    )
                    with open(output_pdf_path, "wb") as output_file:
                        pdf_writer = PyPDF2.PdfWriter()
                        pdf_writer.add_page(pdf_reader.pages[i])
                        pdf_writer.add_page(pdf_reader.pages[i + 1])
                        pdf_writer.write(output_file)
    # Mostrar mensagem de conclusão
    messagebox.showinfo("Processo concluído", "Arquivos Gerados com Sucesso!")


def obter_prefixo():
    root = tk.Tk()
    root.withdraw()
    prefixo = simpledialog.askstring(
        "Prefixo do Nome do Arquivo",
        "Insira o prefixo para o nome do arquivo:",
        initialvalue="Alim - 4CIA - Ituporanga",
    )
    return prefixo


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <arquivo_pdf>")
        sys.exit(1)

    input_pdf_path = sys.argv[1]
    prefixo = obter_prefixo() or ""
    if not prefixo:
        print("Prefixo do nome do arquivo não fornecido.")

    dividir_pdf_em_pares(input_pdf_path, prefixo)
