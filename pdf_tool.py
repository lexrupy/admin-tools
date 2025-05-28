from email.mime import application
import os
import glob
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = argparse.ArgumentParser(description="Split and Merge PDF Files")

parser.add_argument("-j", "--join", nargs="+", help="Join PDF Files")
parser.add_argument("-s", "--split", help="Split PDF per page")

args = vars(parser.parse_args())


def pdf_splitter(path):
    outdir = os.path.dirname(path)
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path, strict=False)
    npages = pdf.getNumPages()
    if npages > 1:
        for page in range(npages):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            p_name = page + 1
            output_filename = "{}_p{}.pdf".format(fname, p_name)

            n = 1
            while os.path.exists(output_filename):
                output_filename = "{}_p{}({}).pdf".format(fname, p_name, n)
                n += 1

            with open(os.path.join(outdir, output_filename), "wb") as out:
                pdf_writer.write(out)
            print("Created: {}".format(output_filename))


def pdf_merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()
    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output_path, "wb") as fh:
        pdf_writer.write(fh)


if args["split"]:
    for file in glob.glob(args["split"]):
        pdf_splitter(file)

    exit(0)

if args["join"]:
    import tkinter as tk
    from tkinter import simpledialog
    from tkinter.messagebox import askyesno

    application_window = tk.Tk()
    application_window.withdraw()

    file_list = []
    for entry in args["join"]:
        file_list += glob.glob(entry)
    file_list.sort()
    out_dir = os.path.dirname(file_list[0])
    out_filename = os.path.splitext(os.path.basename(file_list[0]))[0]
    answer = simpledialog.askstring(
        "Personalizar nome do arquivo de saída",
        "Informe o nome do arquivo",
        initialvalue=out_filename + "_junto.pdf",
    )
    out_filename = os.path.join(out_dir, answer)
    overwite = True
    if os.path.exists(out_filename):
        ovewrite = askyesno(
            title="Confirmação", message="O arquivo já existe. Sobrescrever?"
        )
    if overwite:
        pdf_merger(out_filename, file_list)
