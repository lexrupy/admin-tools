import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfMerger
import sys
import os


class PDFMergeDialog(tk.Toplevel):
    def __init__(self, parent, input_files):
        super().__init__(parent)
        self.title("admin-tools Mesclar PDFs")
        self.input_files = input_files
        self.output_file = "output.pdf"

        self.create_widgets()
        self.fill_listbox()

    def create_widgets(self):
        # Frame para conter a Listbox e os botões de movimento
        list_frame = tk.Frame(self)
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Botões de movimento
        button_move_frame = tk.Frame(list_frame)
        button_move_frame.pack(side=tk.LEFT, padx=(0, 5), fill=tk.Y)

        self.button_move_up = tk.Button(
            button_move_frame, text="↑", command=self.move_up
        )
        self.button_move_up.pack(side=tk.TOP, pady=(0, 5))

        self.button_move_down = tk.Button(
            button_move_frame, text="↓", command=self.move_down
        )
        self.button_move_down.pack(side=tk.TOP)

        # Listbox para exibir os arquivos selecionados
        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Button-1>", self.on_select)

        # Barra de rolagem para a Listbox
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Caixa de entrada para o nome do arquivo de saída
        self.entry_output_file = tk.Entry(self)
        self.entry_output_file.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))
        self.entry_output_file.insert(0, self.output_file)

        # Botões de ação
        action_frame = tk.Frame(self)
        action_frame.pack(side=tk.BOTTOM, pady=(5, 10), padx=10, anchor=tk.E)

        self.button_cancel = tk.Button(
            action_frame, text="Cancelar", command=self.cancel
        )
        self.button_cancel.pack(side=tk.RIGHT, padx=5)

        self.button_merge = tk.Button(action_frame, text="Mesclar", command=self.merge)
        self.button_merge.pack(side=tk.RIGHT)

        # Configuração de tamanho mínimo da janela
        self.minsize(540, 230)

    def fill_listbox(self):
        for file in self.input_files:
            self.listbox.insert(tk.END, file)

    def on_select(self, event):
        # Atualiza a seleção ao clicar na Listbox
        self.listbox.select_clear(0, tk.END)
        self.listbox.activate(self.listbox.nearest(event.y))
        self.listbox.selection_set(self.listbox.nearest(event.y))

    def move_up(self):
        # Move o item selecionado da Listbox para cima
        current_index = self.listbox.curselection()
        if current_index:
            current_index = int(current_index[0])
            if current_index > 0:
                item = self.listbox.get(current_index)
                self.listbox.delete(current_index)
                self.listbox.insert(current_index - 1, item)
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(current_index - 1)

    def move_down(self):
        # Move o item selecionado da Listbox para baixo
        current_index = self.listbox.curselection()
        if current_index:
            current_index = int(current_index[0])
            if current_index < self.listbox.size() - 1:
                item = self.listbox.get(current_index)
                self.listbox.delete(current_index)
                self.listbox.insert(current_index + 1, item)
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(current_index + 1)

    def cancel(self):
        # Fecha a janela e encerra o programa
        self.destroy()
        sys.exit()

    def merge(self):
        output_path = os.path.dirname(self.input_files[self.listbox.index(0)])
        # Obtém o nome do arquivo de saída da entrada do usuário
        self.output_file = self.entry_output_file.get()

        self.output_file = os.path.join(output_path, self.output_file)

        # Verifica se há arquivos na lista
        if self.listbox.size() == 0:
            messagebox.showerror("Erro", "Nenhum arquivo para mesclar.")
            return

        # Mescla os arquivos PDF
        merger = PdfMerger()
        for index in range(self.listbox.size()):
            merger.append(self.input_files[self.listbox.index(index)])
        merger.write(self.output_file)
        merger.close()

        messagebox.showinfo("Concluído", "Os arquivos foram mesclados com sucesso!")
        self.destroy()


def main():
    # Receber lista de arquivos como argumento
    input_files = sys.argv[1:]

    # Criar uma janela TKinter
    root = tk.Tk()
    root.withdraw()

    # Exibir o diálogo de mesclagem de PDFs
    dialog = PDFMergeDialog(root, input_files)
    dialog.mainloop()


if __name__ == "__main__":
    main()
