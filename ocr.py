#!/usr/bin/env python3

import subprocess
import os
import sys
import tempfile
import shutil

import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.withdraw()


# Exibe uma janela de espera
progress = tk.Toplevel()
progress.title("Aguarde")
progress.geometry("300x100")
progress.resizable(False, False)

label = tk.Label(progress, text="Convertendo PDF para texto...\nPor favor, aguarde.")
label.pack(expand=True, pady=20)

# Atualiza a janela antes de iniciar os processos
progress.update()


def erro(msg):
    print(f"Erro: {msg}", file=sys.stderr)
    sys.exit(1)


if len(sys.argv) < 2:
    erro("Uso: python3 ocr_context.py <arquivo.pdf ou imagem>")

ARQUIVO = os.path.abspath(sys.argv[1])
EXT = os.path.splitext(ARQUIVO)[1].lower()
BASE = os.path.splitext(ARQUIVO)[0]
DIR_ORIG = os.path.dirname(ARQUIVO)
NOME_ARQ = os.path.basename(BASE)
LANG = "por"

# Cria diretório temporário
TMPDIR = tempfile.mkdtemp()
os.chdir(TMPDIR)

# Converte PDF ou copia imagem
FILES = []
if EXT == ".pdf":
    print("Convertendo PDF para imagens...")
    subprocess.run(["pdftoppm", ARQUIVO, "pagina", "-png"], check=True)
    FILES = sorted(
        f for f in os.listdir() if f.startswith("pagina-") and f.endswith(".png")
    )
else:
    print("Usando imagem diretamente...")
    ext_sem_ponto = EXT.lstrip(".")
    shutil.copy(ARQUIVO, f"input.{ext_sem_ponto}")
    FILES = [f"input.{ext_sem_ponto}"]

OUTPUT_TXT = os.path.join(DIR_ORIG, f"{NOME_ARQ}_OCR.txt")
OUTPUT_PDF = os.path.join(DIR_ORIG, f"{NOME_ARQ}_OCR.pdf")

# Apaga OCR anterior se existir
for f in [OUTPUT_TXT, OUTPUT_PDF]:
    if os.path.exists(f):
        os.remove(f)

PDFS = []

# Executa OCR em cada imagem
with open(OUTPUT_TXT, "w") as txt_out:
    for IMG in FILES:
        print(f"Fazendo OCR em {IMG}...")
        OUT_BASE = os.path.splitext(IMG)[0]

        subprocess.run(["tesseract", IMG, OUT_BASE, "-l", LANG, "pdf"], check=True)
        subprocess.run(
            ["tesseract", IMG, "stdout", "-l", LANG], stdout=txt_out, check=True
        )

        PDFS.append(f"{OUT_BASE}.pdf")

# Junta os PDFs
if len(PDFS) > 1:
    print("Unindo PDFs OCR...")
    subprocess.run(["pdfunite"] + PDFS + [OUTPUT_PDF], check=True)
else:
    shutil.move(PDFS[0], OUTPUT_PDF)

# Move TXT para destino
shutil.move(OUTPUT_TXT, os.path.join(DIR_ORIG, os.path.basename(OUTPUT_TXT)))

print("OCR concluído!")
print("Arquivos gerados:")
print(f" - {OUTPUT_TXT}")
print(f" - {OUTPUT_PDF}")

# Limpa temporário
shutil.rmtree(TMPDIR)


# Fecha a janela de progresso
progress.destroy()

# Mostra mensagem final
# messagebox.showinfo("OCR Concluído", f"Texto salvo em:\n{OUTPUT_TXT}")
