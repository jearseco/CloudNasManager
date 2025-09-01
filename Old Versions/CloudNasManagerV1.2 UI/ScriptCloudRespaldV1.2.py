import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil
import json

# Archivo donde se guardan servidores
SERVERS_FILE = "servers.json"

def load_servers():
    if os.path.exists(SERVERS_FILE):
        with open(SERVERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_servers(servers):
    with open(SERVERS_FILE, "w") as f:
        json.dump(servers, f, indent=4)

def ask_server_ip():
    ip = simpledialog.askstring("Agregar NAS", "Introduce la IP del servidor NAS:")
    if ip:
        servers = load_servers()
        if ip not in [s["ip"] for s in servers]:
            servers.append({"name": f"ServidorNAS{len(servers)+1}", "ip": ip})
            save_servers(servers)
            messagebox.showinfo("Servidor agregado", f"NAS con IP {ip} agregado correctamente.")
        else:
            messagebox.showinfo("Servidor existente", "Ese servidor ya está registrado.")
    return load_servers()

def realizar_copia(origen, ip):
    if not origen:
        messagebox.showerror("Error", "Debes seleccionar una carpeta de origen.")
        return
    
    destino = f"\\\\{ip}\\DatosPrincipales\\Respaldos"
    
    try:
        shutil.copytree(origen, destino, dirs_exist_ok=True)
        messagebox.showinfo("Éxito", f"✅ Copia completada en {destino}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo copiar: {e}")

def main():
    root = tk.Tk()
    root.title("Gestor de Copias NAS")
    root.geometry("600x400")

    # Cargar servidores (si no hay, pedir uno)
    servers = load_servers()
    if not servers:
        servers = ask_server_ip()

    # Lista de servidores
    tk.Label(root, text="Servidores encontrados:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    server_list = tk.Listbox(root, height=5, width=30)
    server_list.grid(row=1, column=0, padx=10, pady=5)

    for s in servers:
        server_list.insert(tk.END, f"{s['name']} ({s['ip']})")

    # Labels info servidor
    lbl_nombre = tk.Label(root, text="Nombre: ---")
    lbl_nombre.grid(row=0, column=1, padx=10, sticky="w")
    lbl_ip = tk.Label(root, text="IP: ---")
    lbl_ip.grid(row=1, column=1, padx=10, sticky="w")

    # Carpeta origen
    tk.Label(root, text="Directorio a copiar:").grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_origen = tk.Entry(root, width=40)
    entry_origen.grid(row=3, column=1, padx=10, pady=5)

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            entry_origen.delete(0, tk.END)
            entry_origen.insert(0, carpeta)

    tk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta).grid(row=4, column=1, pady=5)

    # Acción al seleccionar servidor
    def on_select(event):
        selected = server_list.curselection()
        if selected:
            server = servers[selected[0]]
            lbl_nombre.config(text=f"Nombre: {server['name']}")
            lbl_ip.config(text=f"IP: {server['ip']}")

    server_list.bind("<<ListboxSelect>>", on_select)

    # Botón de copia
    def copiar_archivos():
        selected = server_list.curselection()
        if not selected:
            messagebox.showerror("Error", "Debes seleccionar un servidor NAS.")
            return
        server = servers[selected[0]]
        realizar_copia(entry_origen.get(), server['ip'])

    tk.Button(root, text="REALIZAR COPIA AHORA", bg="black", fg="white", command=copiar_archivos).grid(row=5, column=1, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
