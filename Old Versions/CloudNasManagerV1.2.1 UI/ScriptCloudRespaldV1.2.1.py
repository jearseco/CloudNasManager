#!/usr/bin/env python3
"""
CloudNasManager v1.2.1 - GUI app (Tkinter)
- Primera vez pide IP del NAS y la guarda en servers.json
- Lista servidores con estado (Activo / N/A)
- Permite agregar/eliminar servidores
- Seleccionar carpeta local de origen
- Realizar copia ahora: copia la carpeta seleccionada a \\<IP>\DatosPrincipales\Respaldos
- Guarda last_backup por servidor en servers.json
- Copias se ejecutan en hilo para no bloquear la UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
import threading
import time
import shutil
import subprocess
import platform
from datetime import datetime

SERVERS_FILE = "servers.json"
DEFAULT_INTERVAL_MIN = 30  # default automatic interval (unused auto loop here)

# Utility: load/save servers
def load_servers():
    if os.path.exists(SERVERS_FILE):
        try:
            with open(SERVERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_servers(servers):
    with open(SERVERS_FILE, "w", encoding="utf-8") as f:
        json.dump(servers, f, indent=2, ensure_ascii=False)

# Ensure platform is Windows for UNC operations (but app will still run on others for testing)
IS_WINDOWS = platform.system().lower() == "windows"

# Try to check if UNC path exists; optionally map with credentials (if provided)
def check_share_access(ip, share_name="DatosPrincipales", username=None, password=None, timeout=2):
    """
    Return True if \\ip\share_name exists (accessible), False otherwise.
    If username/password provided, attempt temporary 'net use' mapping to test (windows only).
    """
    unc = rf"\\{ip}\{share_name}"
    # fast try direct existence
    if os.path.exists(unc):
        return True
    # If Windows and credentials provided, attempt net use to authenticate then check
    if IS_WINDOWS and username:
        try:
            # delete any existing connection to that UNC
            subprocess.run(["net", "use", unc, "/delete", "/y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            # connect
            cmd = ["net", "use", unc, password, f"/user:{username}"]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            # check
            exists = os.path.exists(unc)
            # disconnect
            subprocess.run(["net", "use", unc, "/delete", "/y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return exists
        except Exception:
            return False
    # Last resort: try to ping ip (not definitive), or return False
    return False

# Perform a folder copy in background
def copy_to_server(origen, ip, callback=None, username=None, password=None):
    """
    Copy origen directory to \\ip\DatosPrincipales\Respaldos\{NombreOrigen}\YYYY-MM-DD_HH-MM-SS
    callback(status, message) optional called with progress.
    """
    if not origen or not os.path.exists(origen):
        if callback:
            callback(False, "Ruta de origen no válida.")
        return

    share_root = rf"\\{ip}\DatosPrincipales"
    backup_root = rf"{share_root}\Respaldos"

    try:
        # If credentials provided and on Windows, try mapping before copy
        mapped = False
        if IS_WINDOWS and username:
            try:
                subprocess.run(["net", "use", share_root, "/delete", "/y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                subprocess.run(["net", "use", share_root, password, f"/user:{username}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                mapped = True
            except Exception:
                mapped = False

        # ensure backup_root exists (create dirs)
        os.makedirs(backup_root, exist_ok=True)

        # create folder name based on origen basename and timestamp
        base_name = os.path.basename(origen.rstrip("\\/"))
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        destino = os.path.join(backup_root, base_name, timestamp)
        os.makedirs(destino, exist_ok=True)

        # walk and copy
        total = 0
        for root, dirs, files in os.walk(origen):
            rel = os.path.relpath(root, origen)
            dest_dir = os.path.join(destino, rel) if rel != "." else destino
            os.makedirs(dest_dir, exist_ok=True)
            for f in files:
                src = os.path.join(root, f)
                dst = os.path.join(dest_dir, f)
                # copy if new or modified
                if (not os.path.exists(dst)) or (os.path.getmtime(src) > os.path.getmtime(dst)):
                    shutil.copy2(src, dst)
                    total += 1
                    if callback:
                        callback(True, f"Copiado: {os.path.relpath(dst, destino)}")
        if callback:
            callback(True, f"Copia finalizada. Archivos copiados: {total}")
        # unmap if mapped
        if mapped:
            subprocess.run(["net", "use", share_root, "/delete", "/y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return destino
    except PermissionError as pe:
        if callback:
            callback(False, f"Acceso denegado: {pe}")
    except Exception as e:
        if callback:
            callback(False, f"Error: {e}")

# --- GUI App ---
class CloudNasManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CloudNasManager v1.2.1 UI by Jose Barragàn")
        self.root.geometry("800x500")
        self.servers = load_servers()  # list of dicts: {name, ip, username?, password?, last_backup?}
        self.selected_origin = ""
        self._build_ui()
        # If no servers, prompt on startup
        if not self.servers:
            self._prompt_add_server()
        self._refresh_tree_async()

    def _build_ui(self):
        # Top frame: toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill="x", padx=8, pady=6)

        btn_add = tk.Button(toolbar, text="Agregar servidor/IP", command=self._prompt_add_server)
        btn_add.pack(side="left", padx=4)
        btn_remove = tk.Button(toolbar, text="Eliminar servidor", command=self._remove_selected_server)
        btn_remove.pack(side="left", padx=4)
        btn_refresh = tk.Button(toolbar, text="Actualizar estados", command=self._refresh_tree_async)
        btn_refresh.pack(side="left", padx=4)

        tk.Label(toolbar, text="Intervalo (min):").pack(side="left", padx=8)
        self.interval_var = tk.IntVar(value=DEFAULT_INTERVAL_MIN)
        tk.Spinbox(toolbar, from_=1, to=1440, width=5, textvariable=self.interval_var).pack(side="left")

        # Middle: Treeview (servers) + Detail panel
        mid = tk.Frame(self.root)
        mid.pack(fill="both", expand=True, padx=8, pady=6)

        # Treeview
        tree_frame = tk.Frame(mid)
        tree_frame.pack(side="left", fill="y", padx=(0,8))

        self.tree = ttk.Treeview(tree_frame, columns=("ip", "status", "last"), show="headings", height=15)
        self.tree.heading("ip", text="IP")
        self.tree.heading("status", text="Estado")
        self.tree.heading("last", text="Última copia")
        self.tree.column("ip", width=140)
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("last", width=160, anchor="center")
        self.tree.pack(side="left", fill="y")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Detail panel
        detail = tk.Frame(mid)
        detail.pack(side="right", fill="both", expand=True)

        self.lbl_name = tk.Label(detail, text="Servidor: ---", font=("Arial", 12, "bold"))
        self.lbl_name.pack(anchor="w", pady=(4,0))
        self.lbl_ip = tk.Label(detail, text="IP: ---")
        self.lbl_ip.pack(anchor="w")
        self.lbl_status = tk.Label(detail, text="Estado: ---")
        self.lbl_status.pack(anchor="w")
        self.lbl_last = tk.Label(detail, text="Última copia: ---")
        self.lbl_last.pack(anchor="w")

        tk.Label(detail, text="Directorio a copiar:").pack(anchor="w", pady=(10,0))
        self.entry_origen = tk.Entry(detail, width=50)
        self.entry_origen.pack(anchor="w", pady=(2,4))
        tk.Button(detail, text="Seleccionar carpeta", command=self._select_folder).pack(anchor="w")

        # Buttons
        btn_frame = tk.Frame(detail)
        btn_frame.pack(fill="x", pady=12)
        tk.Button(btn_frame, text="REALIZAR COPIA AHORA", bg="black", fg="white", command=self._on_backup_now).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Abrir carpeta destino", command=self._open_dest_folder).pack(side="left", padx=4)

        # Log box
        tk.Label(detail, text="Registro:").pack(anchor="w")
        self.log_text = tk.Text(detail, height=8, state="disabled")
        self.log_text.pack(fill="both", expand=True, pady=(4,0))

        # Populate tree
        self._populate_tree()

    def _log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", line)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _populate_tree(self):
        # clear
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, s in enumerate(self.servers):
            ip = s.get("ip")
            status = s.get("status", "N/A")
            last = s.get("last_backup", "---")
            # display status text (we'll color rows using tags)
            self.tree.insert("", "end", iid=str(idx), values=(ip, status, last))
            # set tag color
            tag = f"row{idx}"
            if status.lower().startswith("activo") or status == "Activo" or status == "ACTIVO":
                self.tree.tag_configure(tag, background="#e6fff0")  # pale green
            else:
                self.tree.tag_configure(tag, background="#f0f0f0")  # light gray
            self.tree.item(str(idx), tags=(tag,))

    def _prompt_add_server(self):
        ip = simpledialog.askstring("Agregar NAS", "Introduce la IP del servidor NAS (ej: 192.168.101.9):", parent=self.root)
        if not ip:
            return
        # Optional: ask for name and optional credentials
        name = simpledialog.askstring("Nombre", "Nombre para este servidor (opcional):", parent=self.root)
        if not name:
            name = f"ServidorNAS{len(self.servers)+1}"
        # Credentials (optional)
        user = simpledialog.askstring("Usuario (opcional)", "Usuario SMB (dejar vacío para acceso invitado):", parent=self.root)
        pwd = None
        if user:
            pwd = simpledialog.askstring("Contraseña", "Contraseña SMB (opcional):", parent=self.root, show="*")
        # add and save
        new = {"name": name, "ip": ip, "username": user or "", "password": pwd or "", "status": "N/A", "last_backup": "---"}
        self.servers.append(new)
        save_servers(self.servers)
        self._populate_tree()
        # Immediately check status in background
        threading.Thread(target=self._check_and_update_status, args=(len(self.servers)-1,), daemon=True).start()
        self._log(f"Servidor agregado: {name} ({ip})")

    def _remove_selected_server(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Eliminar servidor", "Selecciona un servidor para eliminar.")
            return
        idx = int(sel[0])
        srv = self.servers.pop(idx)
        save_servers(self.servers)
        self._populate_tree()
        self._log(f"Servidor eliminado: {srv.get('name')} ({srv.get('ip')})")

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        srv = self.servers[idx]
        self.lbl_name.config(text=f"Servidor: {srv.get('name')}")
        self.lbl_ip.config(text=f"IP: {srv.get('ip')}")
        self.lbl_status.config(text=f"Estado: {srv.get('status')}")
        self.lbl_last.config(text=f"Última copia: {srv.get('last_backup', '---')}")
        # set origin entry if previously saved per server
        origen = srv.get("origin", "")
        self.entry_origen.delete(0, tk.END)
        if origen:
            self.entry_origen.insert(0, origen)

    def _select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_origen.delete(0, tk.END)
            self.entry_origen.insert(0, folder)
            # store chosen origin for selected server (if any)
            sel = self.tree.selection()
            if sel:
                idx = int(sel[0])
                self.servers[idx]["origin"] = folder
                save_servers(self.servers)

    def _on_backup_now(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un servidor primero.")
            return
        idx = int(sel[0])
        srv = self.servers[idx]
        origen = self.entry_origen.get().strip()
        if not origen or not os.path.exists(origen):
            messagebox.showerror("Error", "Selecciona una carpeta de origen válida.")
            return
        # disable button to avoid double clicks (simple)
        threading.Thread(target=self._backup_thread, args=(idx, origen), daemon=True).start()

    def _backup_thread(self, idx, origen):
        srv = self.servers[idx]
        ip = srv.get("ip")
        user = srv.get("username") or None
        pwd = srv.get("password") or None
        def cb(success, message):
            self._log(message)
        self._log(f"Iniciando copia a {ip} desde {origen} ...")
        result = copy_to_server(origen, ip, callback=cb, username=user, password=pwd)
        if result:
            # success: update last_backup and status
            self.servers[idx]["last_backup"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.servers[idx]["status"] = "Activo"
            save_servers(self.servers)
            self._populate_tree()
            self._log(f"Backup guardado en: {result}")
        else:
            # assume failure -> check access to set status N/A
            ok = check_share_access(ip)
            self.servers[idx]["status"] = "Activo" if ok else "N/A"
            save_servers(self.servers)
            self._populate_tree()

    def _open_dest_folder(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Abrir destino", "Selecciona un servidor primero.")
            return
        idx = int(sel[0])
        srv = self.servers[idx]
        ip = srv.get("ip")
        path = rf"\\{ip}\DatosPrincipales\Respaldos"
        try:
            if IS_WINDOWS:
                os.startfile(path)
            else:
                messagebox.showinfo("Abrir destino", f"Ruta destino: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ruta: {e}")

    # Background status check for all servers
    def _refresh_tree_async(self):
        threading.Thread(target=self._refresh_all_statuses, daemon=True).start()

    def _refresh_all_statuses(self):
        for idx in range(len(self.servers)):
            self._check_and_update_status(idx)
        self._populate_tree()
        self._log("Actualización de estados completada.")

    def _check_and_update_status(self, idx):
        srv = self.servers[idx]
        ip = srv.get("ip")
        user = srv.get("username") or None
        pwd = srv.get("password") or None
        ok = check_share_access(ip, share_name="DatosPrincipales", username=user, password=pwd)
        srv["status"] = "Activo" if ok else "N/A"
        save_servers(self.servers)
        # update UI (must be done on main thread)
        self.root.after(1, self._populate_tree)

def main():
    root = tk.Tk()
    app = CloudNasManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
