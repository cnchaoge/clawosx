"""
ClawOSX Config Tool - Simple GUI for AI API Key, Channels, Service Start/Stop
Requirements: Python 3.x (Windows自带), 零外部依赖
"""
import socket
import json
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

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
    """检测端口是否被占用（判断服务是否在运行）"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect(("127.0.0.1", port))
        sock.close()
        return True
    except:
        return False

def service_status():
    port = get_port()
    return check_port_open(port)

def start_service():
    if not os.path.exists(START_BAT):
        messagebox.showerror("Error", "Windows-Start.bat not found")
        return False
    try:
        subprocess.Popen(
            ["cmd", "/c", START_BAT],
            cwd=SCRIPT_DIR,
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW
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
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    except:
        return False

# === Tkinter GUI ===
root = tk.Tk()
root.title("ClawOSX Config")
root.geometry("520x620")
root.resizable(False, False)
root.configure(bg="#1a1a2e")

# 颜色
BG = "#1a1a2e"
CARD_BG = "#16213e"
ACCENT = "#00d4ff"
GREEN = "#00ff88"
RED = "#e94560"
WHITE = "#eee"
GRAY = "#666"

def card(parent, **kwargs):
    f = tk.Frame(parent, bg=CARD_BG, bd=0, highlightthickness=0, **kwargs)
    f.pack(fill="x", pady=0, padx=0)
    return f

def section(parent, text):
    tk.Frame(parent, bg=CARD_BG, height=2).pack(fill="x", pady=(0,0))
    f = tk.Frame(parent, bg=CARD_BG)
    f.pack(fill="x", pady=(12, 8), padx=16)
    tk.Label(f, text=text, fg=ACCENT, bg=CARD_BG, font=("Segoe UI", 11, "bold")).pack(anchor="w")
    return f

def row(parent):
    f = tk.Frame(parent, bg=CARD_BG)
    f.pack(fill="x", pady=4)
    return f

def label(parent, text, width=10):
    l = tk.Label(parent, text=text, fg="#999", bg=CARD_BG, font=("Segoe UI", 10), anchor="w", width=width)
    l.pack(side="left", padx=(0, 8))
    return l

def entry(parent, show="", width=30):
    e = tk.Entry(parent, bg="#0f3460", fg=WHITE, font=("Segoe UI", 11),
                 insertbackground=WHITE, bd=0, highlightthickness=0, width=width)
    e.pack(side="left", fill="x", expand=True, padx=0)
    if show:
        e.configure(show=show)
    return e

def btn(parent, text, cmd, bg=ACCENT, fg="#1a1a2e"):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg, pady=6)
    b.pack(side="left", padx=(0, 8))
    return b

def toggle(parent, var, cmd=None):
    f = tk.Frame(parent, bg=CARD_BG)
    f.pack(side="right")
    c = tk.Checkbutton(f, variable=var, command=cmd, bg=CARD_BG,
                       activebackground=CARD_BG, cursor="hand2",
                       onvalue=True, offvalue=False,
                       selectcolor="#0f3460", indicatoron=False)
    c.pack()
    return c

# 状态显示
def status_widget(parent):
    f = tk.Frame(parent, bg=CARD_BG)
    f.pack(fill="x", pady=(0, 8))
    dot = tk.Frame(f, width=12, height=12, bg=GRAY)
    dot.pack(side="left", padx=(0, 8))
    dot.configure(bg=RED)
    lbl = tk.Label(f, text="Stopped", fg=GRAY, bg=CARD_BG, font=("Segoe UI", 11))
    lbl.pack(side="left")
    return dot, lbl

# === 主界面 ===
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True)

# 标题
tk.Label(main, text="ClawOSX", fg=WHITE, bg=BG,
         font=("Segoe UI", 28, "bold")).pack(pady=(20, 4))
tk.Label(main, text="USB Portable AI Agent", fg=GRAY, bg=BG,
         font=("Segoe UI", 10)).pack(pady=(0, 16))

# === 服务状态 ===
sc = tk.Frame(main, bg=CARD_BG)
sc.pack(fill="x", padx=16, pady=(0, 12))
section(sc, "SERVICE STATUS")
sf = tk.Frame(sc, bg=CARD_BG)
sf.pack(fill="x", padx=16, pady=(0, 12))
dot = tk.Frame(sf, width=12, height=12, bg=GRAY)
dot.pack(side="left", padx=(0, 8))
status_lbl = tk.Label(sf, text="Checking...", fg=GRAY, bg=CARD_BG, font=("Segoe UI", 11))
status_lbl.pack(side="left")
port_lbl = tk.Label(sf, text="", fg=GRAY, bg=CARD_BG, font=("Segoe UI", 9))
port_lbl.pack(side="right")
btnf = tk.Frame(sc, bg=CARD_BG)
btnf.pack(fill="x", padx=16, pady=(0, 12))
refresh_btn = btn(btnf, "Refresh", lambda: update_status())
stop_btn = btn(btnf, "Stop", lambda: do_stop(), bg=RED, fg=WHITE)
start_btn = btn(btnf, "Start", lambda: do_start(), bg=GREEN, fg="#1a1a2e")

def update_status():
    port = get_port()
    running = check_port_open(port)
    dot.configure(bg=GREEN if running else RED)
    status_lbl.configure(text="Running" if running else "Stopped", fg=GREEN if running else GRAY)
    port_lbl.configure(text=f"port {port}")

def do_stop():
    stop_service()
    root.after(1000, update_status)

def do_start():
    start_service()
    root.after(2000, update_status)

# === AI Config ===
ac = tk.Frame(main, bg=CARD_BG)
ac.pack(fill="x", pady=(0, 12), padx=16)
section(ac, "AI CONFIG")
af = tk.Frame(ac, bg=CARD_BG)
af.pack(fill="x", padx=16, pady=(0, 12))

ai_provider_var = tk.StringVar(value="minimax")
tk.Label(af, text="Provider", fg="#999", bg=CARD_BG, font=("Segoe UI", 10), anchor="w", width=10).pack(anchor="w")
pf = tk.Frame(af, bg=CARD_BG)
pf.pack(fill="x", pady=(4, 8))
for val, txt in [("minimax","MiniMax"),("openai","OpenAI"),("deepseek","DeepSeek"),("custom","Custom")]:
    r = tk.Radiobutton(pf, text=txt, variable=ai_provider_var, value=val, bg=CARD_BG, fg=WHITE,
                       activebackground=CARD_BG, cursor="hand2", selectcolor="#0f3460", font=("Segoe UI", 10))
    r.pack(side="left", padx=(0, 12))

tk.Label(af, text="API Key", fg="#999", bg=CARD_BG, font=("Segoe UI", 10), anchor="w", width=10).pack(anchor="w")
apikey_e = entry(af)
tk.Label(af, text="Model", fg="#999", bg=CARD_BG, font=("Segoe UI", 10), anchor="w", width=10).pack(anchor="w", pady=(8,0))
model_e = entry(af)

# === Message Channels ===
cc = tk.Frame(main, bg=CARD_BG)
cc.pack(fill="x", pady=(0, 12), padx=16)
section(cc, "MESSAGE CHANNELS")

# Feishu
fc = tk.Frame(cc, bg="#0f3460", bd=0)
fc.pack(fill="x", pady=(0, 8))
fh = tk.Frame(fc, bg="#0f3460")
fh.pack(fill="x", padx=12, pady=(8, 4))
tk.Label(fh, text="Feishu", fg="#ccc", bg="#0f3460", font=("Segoe UI", 11, "bold")).pack(side="left")
feishu_en_var = tk.BooleanVar(value=False)
tk.Checkbutton(fh, variable=feishu_en_var, bg="#0f3460", activebackground="#0f3460",
               cursor="hand2", onvalue=True, offvalue=False).pack(side="right")
fd = tk.Frame(fc, bg="#0f3460")
fd.pack(fill="x", padx=12, pady=(0, 8))
tk.Label(fd, text="App ID", fg="#999", bg="#0f3460", font=("Segoe UI", 9), width=10).pack(side="left")
feishu_id_e = entry(fd, width=25)
tk.Label(fd, text="App Secret", fg="#999", bg="#0f3460", font=("Segoe UI", 9), width=10).pack(side="left", pady=(4,0))
feishu_sec_e = entry(fd, show="*", width=25)

# Telegram
tc = tk.Frame(cc, bg="#0f3460", bd=0)
tc.pack(fill="x", pady=(0, 8))
th = tk.Frame(tc, bg="#0f3460")
th.pack(fill="x", padx=12, pady=(8, 4))
tk.Label(th, text="Telegram", fg="#ccc", bg="#0f3460", font=("Segoe UI", 11, "bold")).pack(side="left")
tg_en_var = tk.BooleanVar(value=False)
tk.Checkbutton(th, variable=tg_en_var, bg="#0f3460", activebackground="#0f3460",
               cursor="hand2", onvalue=True, offvalue=False).pack(side="right")
td = tk.Frame(tc, bg="#0f3460")
td.pack(fill="x", padx=12, pady=(0, 8))
tk.Label(td, text="Bot Token", fg="#999", bg="#0f3460", font=("Segoe UI", 9), width=10).pack(side="left")
tg_token_e = entry(td, show="*", width=30)

# Save
sf2 = tk.Frame(cc, bg=CARD_BG)
sf2.pack(fill="x", pady=(0, 4), padx=16)
save_btn = btn(sf2, "Save All", lambda: save_all(), bg=ACCENT, fg="#1a1a2e")

# Footer
tk.Label(main, text="All data stored on USB drive", fg="#444", bg=BG,
         font=("Segoe UI", 9)).pack(pady=12)

# === Load & Save ===
def load_config():
    cfg = load_json(OPENCLAW_JSON)
    # AI
    providers = cfg.get("models", {}).get("providers", {})
    for k, v in providers.items():
        ai_provider_var.set(k)
        apikey_e.insert(0, v.get("apiKey", ""))
        model_e.insert(0, v.get("model", ""))
        break
    # Feishu
    feishu = cfg.get("channels", {}).get("feishu", {})
    if feishu.get("appId"):
        feishu_en_var.set(feishu.get("enabled", False))
        feishu_id_e.insert(0, feishu.get("appId", ""))
        feishu_sec_e.insert(0, feishu.get("appSecret", ""))
    # Telegram
    tg = cfg.get("channels", {}).get("telegram", {})
    if tg.get("botToken"):
        tg_en_var.set(tg.get("enabled", False))
        tg_token_e.insert(0, tg.get("botToken", ""))

def save_all():
    # 构建配置
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
    messagebox.showinfo("Saved", "Configuration saved successfully")

# Init
load_config()
update_status()

# 定期刷新状态
def poll():
    update_status()
    root.after(3000, poll)

root.after(1000, poll)
root.mainloop()