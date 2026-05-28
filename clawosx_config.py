"""
ClawOSX Config Tool - Simple GUI for AI API Key, Channels, Service Start/Stop
Requirements: Python 3.x (Windows自带), 零外部依赖
"""
import socket
import json
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# === 配置路径 ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OPENCLAW_JSON = os.path.join(SCRIPT_DIR, "data", ".openclaw", "openclaw.json")
PORT_FILE = os.path.join(SCRIPT_DIR, "data", ".openclaw", "port.txt")
START_BAT = os.path.join(SCRIPT_DIR, "Windows-Start.bat")
DEFAULT_PORT = 18789

# === 工具函数 ===
def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_port():
    if os.path.exists(PORT_FILE):
        try:
            with open(PORT_FILE, "r") as f:
                return int(f.read().strip())
        except:
            pass
    return DEFAULT_PORT

def check_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect(("127.0.0.1", port))
        sock.close()
        return True
    except:
        return False

def start_service():
    if not os.path.exists(START_BAT):
        messagebox.showerror("Error", "Windows-Start.bat not found")
        return False
    try:
        subprocess.Popen(
            ["cmd", "/c", START_BAT],
            cwd=SCRIPT_DIR,
            shell=True,
            creationflags=0x08000000  # CREATE_NO_WINDOW
        )
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def stop_service():
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "node.exe"],
            capture_output=True,
            creationflags=0x08000000
        )
        return True
    except:
        return False

# === 颜色主题 ===
BG = "#0f1117"
CARD = "#161b22"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
RED = "#f85149"
YELLOW = "#d29922"
WHITE = "#e6edf3"
GRAY = "#8b949e"
DARK_GRAY = "#484f58"
ENTRY_BG = "#21262d"

root = tk.Tk()
root.title("ClawOSX")
root.geometry("480x700")
root.minsize(400, 600)
root.configure(bg=BG)

# 可滚动画布
canvas = tk.Canvas(root, bg=BG, highlightthickness=0, bd=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview, width=6)
scrollable = tk.Frame(canvas, bg=BG)

scrollable.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# === 小工具 ===
def card(parent, padx=16, pady=6):
    f = tk.Frame(parent, bg=CARD, bd=0)
    f.pack(fill="x", padx=padx, pady=pady)
    return f

def section_title(parent, text):
    tk.Label(parent, text=text, fg=ACCENT, bg=CARD,
             font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", pady=(10, 6), padx=2)

def sep(parent):
    tk.Frame(parent, bg=BG, height=1).pack(fill="x", pady=(4, 4))

def field(parent, label_text, entry_width=28, show=""):
    f = tk.Frame(parent, bg=CARD)
    f.pack(fill="x", pady=3)
    tk.Label(f, text=label_text, fg=GRAY, bg=CARD,
             font=("Segoe UI", 9), width=11, anchor="w").pack(side="left", padx=(0, 6))
    e = tk.Entry(f, bg=ENTRY_BG, fg=WHITE, font=("Segoe UI", 10),
                  insertbackground=WHITE, bd=0, highlightthickness=0,
                  width=entry_width)
    e.pack(side="left")
    if show:
        e.configure(show=show)
    return e

def btn(parent, text, cmd, bg=ACCENT, fg="#0d1117", padx=10):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  pady=5, padx=padx)
    b.pack(side="left", padx=(0, 6))
    return b

def status_bar(parent):
    f = tk.Frame(parent, bg=CARD)
    f.pack(fill="x", pady=4)
    dot = tk.Frame(f, width=8, height=8, bg=GRAY)
    dot.pack(side="left", padx=(0, 8), pady=4)
    lbl = tk.Label(f, text="Unknown", fg=GRAY, bg=CARD, font=("Segoe UI", 10))
    lbl.pack(side="left")
    port_lbl = tk.Label(f, text="", fg=DARK_GRAY, bg=CARD, font=("Segoe UI", 9))
    port_lbl.pack(side="right")
    return dot, lbl, port_lbl

# === 顶部 ===
tk.Label(scrollable, text="ClawOSX", fg=WHITE, bg=BG,
         font=("Segoe UI", 26, "bold")).pack(pady=(18, 2))
tk.Label(scrollable, text="USB Portable AI Agent  ·  v1.0", fg=GRAY, bg=BG,
         font=("Segoe UI", 9)).pack(pady=(0, 14))

# === 服务状态 ===
sc = card(scrollable)
status_dot, status_lbl, status_port_lbl = status_bar(sc)
tk.Frame(sc, bg=BG, height=1).pack(fill="x", pady=(4, 6))

btn_frame = tk.Frame(sc, bg=CARD)
btn_frame.pack(fill="x")
btn(btn_frame, "Refresh", lambda: update_status(), bg=DARK_GRAY, fg=WHITE)
stop_btn = btn(btn_frame, "Stop", lambda: do_stop(), bg=RED, fg=WHITE)
start_btn = btn(btn_frame, "Start", lambda: do_start(), bg=GREEN, fg="#0d1117")

def update_status():
    port = get_port()
    running = check_port_open(port)
    status_dot.configure(bg=GREEN if running else RED)
    status_lbl.configure(text="Running" if running else "Stopped",
                         fg=GREEN if running else GRAY)
    status_port_lbl.configure(text=f"port {port}" if running else "")

def do_stop():
    stop_service()
    root.after(1200, update_status)

def do_start():
    start_service()
    root.after(2500, update_status)

# === AI 配置 ===
ac = card(scrollable)
section_title(ac, "AI CONFIG")

ai_provider_var = tk.StringVar(value="minimax")
pf = tk.Frame(ac, bg=CARD)
pf.pack(fill="x", pady=(0, 4))
for val, txt in [("minimax", "MiniMax"), ("openai", "OpenAI"),
                 ("deepseek", "DeepSeek"), ("custom", "Custom")]:
    tk.Radiobutton(pf, text=txt, variable=ai_provider_var, value=val,
                   bg=CARD, fg=WHITE, activebackground=CARD, cursor="hand2",
                   selectcolor=ENTRY_BG, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))

apikey_e = field(ac, "API Key")
model_e = field(ac, "Model", entry_width=20)

# === 消息渠道 ===
cc = card(scrollable)
section_title(cc, "MESSAGE CHANNELS")

# Feishu
feishu_en_var = tk.BooleanVar(value=False)
fe = tk.Frame(cc, bg=ENTRY_BG, padx=12, pady=8)
fe.pack(fill="x", pady=(0, 4))
fh = tk.Frame(fe, bg=ENTRY_BG)
fh.pack(fill="x")
tk.Label(fh, text="Feishu", fg=WHITE, bg=ENTRY_BG, font=("Segoe UI", 10, "bold")).pack(side="left")
tk.Checkbutton(fh, variable=feishu_en_var, bg=ENTRY_BG, activebackground=ENTRY_BG,
               cursor="hand2", onvalue=True, offvalue=False,
               selectcolor=ACCENT, indicatoron=False).pack(side="right")
fd = tk.Frame(fe, bg=ENTRY_BG)
fd.pack(fill="x", pady=(4, 0))
tk.Label(fd, text="App ID", fg=GRAY, bg=ENTRY_BG, font=("Segoe UI", 8), width=8).pack(side="left")
feishu_id_e = tk.Entry(fd, bg=BG, fg=WHITE, font=("Segoe UI", 9),
                       insertbackground=WHITE, bd=0, highlightthickness=0, width=22)
feishu_id_e.pack(side="left")
tk.Label(fd, text="App Secret", fg=GRAY, bg=ENTRY_BG, font=("Segoe UI", 8), width=9).pack(side="left", padx=(8, 0))
feishu_sec_e = tk.Entry(fd, bg=BG, fg=WHITE, font=("Segoe UI", 9),
                        insertbackground=WHITE, bd=0, highlightthickness=0,
                        width=14, show="*")
feishu_sec_e.pack(side="left")

# Telegram
tg_en_var = tk.BooleanVar(value=False)
te = tk.Frame(cc, bg=ENTRY_BG, padx=12, pady=8)
te.pack(fill="x", pady=(0, 4))
th = tk.Frame(te, bg=ENTRY_BG)
th.pack(fill="x")
tk.Label(th, text="Telegram", fg=WHITE, bg=ENTRY_BG, font=("Segoe UI", 10, "bold")).pack(side="left")
tk.Checkbutton(th, variable=tg_en_var, bg=ENTRY_BG, activebackground=ENTRY_BG,
               cursor="hand2", onvalue=True, offvalue=False,
               selectcolor=ACCENT, indicatoron=False).pack(side="right")
td = tk.Frame(te, bg=ENTRY_BG)
td.pack(fill="x", pady=(4, 0))
tk.Label(td, text="Bot Token", fg=GRAY, bg=ENTRY_BG, font=("Segoe UI", 8), width=8).pack(side="left")
tg_token_e = tk.Entry(td, bg=BG, fg=WHITE, font=("Segoe UI", 9),
                       insertbackground=WHITE, bd=0, highlightthickness=0,
                       width=28, show="*")
tg_token_e.pack(side="left")

# Save
sf = tk.Frame(cc, bg=CARD, pady=(4, 4))
sf.pack(fill="x")
save_btn = btn(sf, "Save All", lambda: save_all(), bg=ACCENT, fg="#0d1117", padx=16)

# === Load & Save ===
def load_config():
    cfg = load_json(OPENCLAW_JSON)
    providers = cfg.get("models", {}).get("providers", {})
    for k, v in providers.items():
        ai_provider_var.set(k)
        apikey_e.insert(0, v.get("apiKey", ""))
        model_e.insert(0, v.get("model", ""))
        break
    feishu = cfg.get("channels", {}).get("feishu", {})
    if feishu.get("appId"):
        feishu_en_var.set(feishu.get("enabled", False))
        feishu_id_e.insert(0, feishu.get("appId", ""))
        feishu_sec_e.insert(0, feishu.get("appSecret", ""))
    tg = cfg.get("channels", {}).get("telegram", {})
    if tg.get("botToken"):
        tg_en_var.set(tg.get("enabled", False))
        tg_token_e.insert(0, tg.get("botToken", ""))

def save_all():
    cfg = load_json(OPENCLAW_JSON)
    if "models" not in cfg:
        cfg["models"] = {"mode": "merge", "providers": {}}
    if "providers" not in cfg["models"]:
        cfg["models"]["providers"] = {}
    provider = ai_provider_var.get()
    apikey = apikey_e.get().strip()
    if not apikey:
        messagebox.showwarning("Warning", "API Key cannot be empty")
        return
    cfg["models"]["providers"] = {
        provider: {
            "apiKey": apikey,
            "model": model_e.get().strip()
        }
    }
    cfg["channels"] = cfg.get("channels", {})
    cfg["channels"]["feishu"] = {
        "enabled": feishu_en_var.get(),
        "appId": feishu_id_e.get().strip(),
        "appSecret": feishu_sec_e.get().strip()
    }
    cfg["channels"]["telegram"] = {
        "enabled": tg_en_var.get(),
        "botToken": tg_token_e.get().strip()
    }
    save_json(OPENCLAW_JSON, cfg)
    messagebox.showinfo("Saved", "Configuration saved")

# === 底部 ===
tk.Label(scrollable, text="All data stored on USB drive", fg=DARK_GRAY, bg=BG,
         font=("Segoe UI", 8)).pack(pady=14)

# Init
load_config()
update_status()

def poll():
    update_status()
    root.after(4000, poll)

root.after(1500, poll)
root.mainloop()