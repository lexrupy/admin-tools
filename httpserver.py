import os
import sys
import threading
import subprocess
import re
import argparse
import socket
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import tkinter as tk
from tkinter import messagebox


class HTTPHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        return os.path.join(self.server.base_path, relpath)


class HTTPServer(BaseHTTPServer):
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        super().__init__(server_address, RequestHandlerClass)


def get_local_ips():
    """Obtém os endereços IP IPv4 das interfaces de rede no Linux usando o comando 'ip'."""
    ips = ["127.0.0.1"]
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True
        )
        matches = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)/', result.stdout)
        for ip in matches:
            if ip != "127.0.0.1":
                ips.append(ip)
    except Exception as e:
        print(f"Erro ao obter IPs via comando 'ip': {e}")
    return ips



def start_server(server):
    try:
        server.serve_forever()
    except Exception as e:
        print("Servidor encerrado:", e)


def create_gui(server, directory, port, ips):
    def stop_server():
        if messagebox.askyesno("Encerrar", "Deseja realmente encerrar o servidor?"):
            server.shutdown()
            root.destroy()

    root = tk.Tk()
    root.title("Servidor HTTP")
    root.geometry("600x400")


    tk.Label(root, text="HOSTNAME:"+socket.gethostname(), fg="red").pack()

    label = tk.Label(
        root,
        text=f"Servindo arquivos a partir de:\n{directory}\n\nPorta: {port}",
        padx=20,
        pady=10,
        justify="left"
    )
    label.pack()

    ip_label = tk.Label(root, text="Endereços disponíveis para acesso:", pady=5, font=("Helvetica", 10, "bold"))
    ip_label.pack()

    for ip in ips:
        tk.Label(root, text=f"http://{ip}:{port}", fg="blue").pack()

    stop_button = tk.Button(root, text="Encerrar servidor", command=stop_server, padx=10, pady=5)
    stop_button.pack(pady=15)

    root.protocol("WM_DELETE_WINDOW", stop_server)
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP server with GUI and custom base path.")
    parser.add_argument("directory", help="Directory to serve files from")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on (default: 8000)")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Erro: O diretório '{args.directory}' não existe.", file=sys.stderr)
        sys.exit(1)

    base_path = os.path.abspath(args.directory)
    server = HTTPServer(base_path, ("", args.port))

    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server, args=(server,), daemon=True)
    server_thread.start()

    print(f"Servidor iniciado em http://localhost:{args.port} servindo {base_path}")

    # Coleta IPs da máquina para exibição
    ips = get_local_ips()

    # Inicia interface gráfica
    create_gui(server, base_path, args.port, ips)

