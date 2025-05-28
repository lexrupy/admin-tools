import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfFileMerger
import sys
import os
import tkinterdnd2 as tkdnd

class PDFMergeDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mesclar PDFs")
        self.input_files = []
        self.output_file = "output.pdf"

        self.create_widgets()

    def create_widgets(self):
        # Listbox para exibir os arquivos selecionados
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.listbox.drop_target_register(tkdnd.DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)

        # Barra de rolagem para a Listbox
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Caixa de entrada para o nome do arquivo de saída
        self.entry_output_file = tk.Entry(self)
        self.entry_output_file.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))
        self.entry_output_file.insert(0, self.output_file)

        # Botões
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=(5, 10))
        self.button_cancel = tk.Button(button_frame, text="Cancelar", command=self.cancel)
        self.button_cancel.pack(side=tk.LEFT, padx=(0, 5))
        self.button_merge = tk.Button(button_frame, text="Mesclar", command=self.merge)
        self.button_merge.pack(side=tk.LEFT)

    def on_drop(self, event):
        # Adiciona os arquivos arrastados para a lista de arquivos
        dropped_files = self.tk.splitlist(event.data)
        for file in dropped_files:
            if os.path.splitext(file)[1].lower() == ".pdf":
                self.input_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def cancel(self):
        # Fecha a janela e encerra o programa
        self.destroy()
        sys.exit()

    def merge(self):
        # Obtém o nome do arquivo de saída da entrada do usuário
        self.output_file = self.entry_output_file.get()

        # Mescla os arquivos PDF
        merger = PdfFileMerger()
        for file in self.input_files:
            merger.append(file)
        merger.write(self.output_file)
        merger.close()

        messagebox.showinfo("Concluído", "Os arquivos foram mesclados com sucesso!")
        self.destroy()

def main():
    dialog = PDFMergeDialog()
    dialog.mainloop()

if __name__ == "__main__":
    main()

