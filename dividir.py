import PyPDF2
import sys
import os


def dividir_pdf(input_pdf_path):
    # Verifica se o arquivo PDF de entrada existe
    if not os.path.isfile(input_pdf_path):
        print(f"Erro: O arquivo '{input_pdf_path}' não foi encontrado.")
        return

    # Extrai o nome do arquivo (sem extensão) e cria o diretório de saída
    output_dir = os.path.splitext(input_pdf_path)[0]
    os.makedirs(output_dir, exist_ok=True)

    with open(input_pdf_path, "rb") as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        num_pages = len(pdf_reader.pages)

        # Divide o PDF página por página
        for i, page in enumerate(pdf_reader.pages, start=1):
            output_pdf_path = os.path.join(output_dir, f"pagina{i}.pdf")
            with open(output_pdf_path, "wb") as output_file:
                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(page)
                pdf_writer.write(output_file)

    print(
        f"O arquivo '{input_pdf_path}' foi dividido em {num_pages} páginas e salvo em '{output_dir}'."
    )


def main():
    if len(sys.argv) < 2:
        print("Uso: python dividir.py <arquivo_pdf1> [<arquivo_pdf2> ...]")
        return

    for input_pdf_path in sys.argv[1:]:
        dividir_pdf(input_pdf_path)


if __name__ == "__main__":
    main()
