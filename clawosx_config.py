"""
ClawOSX 配置工具 - AI API Key / 消息渠道 / 服务启停
Python 3 内置库，零外部依赖
"""
import socket
import json
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import webbrowser

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
        messagebox.showerror("错误", "Windows-Start.bat 未找到")
        return False
    try:
        subprocess.Popen(
            ["cmd", "/c", START_BAT],
            cwd=SCRIPT_DIR,
            shell=True,
            creationflags=0x08000000
        )
        return True
    except Exception as e:
        messagebox.showerror("错误", str(e))
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

# === 明亮颜色主题 ===
BG = "#f0f2f5"
CARD = "#ffffff"
ACCENT = "#0066cc"
GREEN = "#28a745"
RED = "#dc3545"
YELLOW = "#f0a500"
TEXT = "#1a1a1a"
TEXT_SEC = "#6c757d"
BORDER = "#dee2e6"
ENTRY_BG = "#e9ecef"

# === 主窗口 ===
root = tk.Tk()
root.title("ClawOSX 配置工具")
root.geometry("480x720")
root.minsize(400, 620)
root.configure(bg=BG)

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

# === 组件工具 ===
def card(parent):
    f = tk.Frame(parent, bg=CARD, bd=1, relief="solid", highlightcolor=BORDER,
                 highlightthickness=1, highlightbackground=BORDER)
    f.pack(fill="x", padx=16, pady=6)
    return f

def section_title(parent, text):
    tk.Label(parent, text=text, fg=ACCENT, bg=CARD,
             font=("Microsoft YaHei UI", 10, "bold"), anchor="w").pack(fill="x", pady=(10, 6), padx=2)

def field(parent, label_text, entry_width=28, show=""):
    f = tk.Frame(parent, bg=CARD)
    f.pack(fill="x", pady=3)
    tk.Label(f, text=label_text, fg=TEXT_SEC, bg=CARD,
             font=("Microsoft YaHei UI", 9), width=11, anchor="w").pack(side="left", padx=(0, 6))
    e = tk.Entry(f, bg=ENTRY_BG, fg=TEXT, font=("Microsoft YaHei UI", 10),
                  insertbackground=TEXT, bd=0, highlightthickness=0,
                  width=entry_width)
    e.pack(side="left")
    if show:
        e.configure(show=show)
    return e

def btn(parent, text, cmd, bg=ACCENT, fg="#ffffff", padx=10):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=("Microsoft YaHei UI", 9, "bold"), bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  pady=5, padx=padx)
    b.pack(side="left", padx=(0, 6))
    return b

def status_bar(parent):
    f = tk.Frame(parent, bg=CARD)
    f.pack(fill="x", pady=4)
    dot = tk.Frame(f, width=10, height=10, bg=TEXT_SEC)
    dot.pack(side="left", padx=(0, 8), pady=4)
    dot.config(highlightthickness=0)
    lbl = tk.Label(f, text="检测中...", fg=TEXT_SEC, bg=CARD, font=("Microsoft YaHei UI", 10))
    lbl.pack(side="left")
    port_lbl = tk.Label(f, text="", fg=TEXT_SEC, bg=CARD, font=("Microsoft YaHei UI", 9))
    port_lbl.pack(side="right")
    return dot, lbl, port_lbl

# === 标题区 ===
tk.Label(scrollable, text="ClawOSX", fg=TEXT, bg=BG,
         font=("Microsoft YaHei UI", 26, "bold")).pack(pady=(18, 2))
tk.Label(scrollable, text="U盘便携 AI 助手  ·  v1.0", fg=TEXT_SEC, bg=BG,
         font=("Microsoft YaHei UI", 9)).pack(pady=(0, 14))

# === 服务状态 ===
sc = card(scrollable)
status_dot, status_lbl, status_port_lbl = status_bar(sc)
tk.Frame(sc, bg=BORDER, height=1).pack(fill="x", pady=(4, 6))

btn_frame = tk.Frame(sc, bg=CARD)
btn_frame.pack(fill="x")
btn(btn_frame, "刷新", lambda: update_status(), bg=BORDER, fg=TEXT)
stop_btn_ref = btn(btn_frame, "停止", lambda: do_stop(), bg=RED, fg="#ffffff")
start_btn_ref = btn(btn_frame, "启动", lambda: do_start(), bg=GREEN, fg="#ffffff")

# 开始聊天按钮（运行后才显示）
chat_btn_frame = tk.Frame(sc, bg=CARD)
chat_btn_frame.pack(fill="x", pady=(0, 4))
chat_btn = tk.Button(chat_btn_frame, text="开始聊天", command=lambda: open_browser(),
                    bg=GREEN, fg="#ffffff",
                    font=("Microsoft YaHei UI", 13, "bold"), bd=0, cursor="hand2",
                    activebackground=GREEN, activeforeground="#ffffff",
                    pady=8)
chat_btn.pack(fill="x", ipady=4)
chat_btn_frame.pack_forget()  # 初始隐藏

def open_browser():
    port = get_port()
    webbrowser.open(f"http://127.0.0.1:{port}/")

def update_status():
    port = get_port()
    running = check_port_open(port)
    status_dot.configure(bg=GREEN if running else RED)
    status_lbl.configure(text="运行中" if running else "已停止",
                         fg=GREEN if running else TEXT_SEC)
    status_port_lbl.configure(text=f"端口 {port}" if running else "")
    if running:
        chat_btn_frame.pack(fill="x", pady=(0, 4))
    else:
        chat_btn_frame.pack_forget()

def do_stop():
    status_dot.configure(bg=YELLOW)
    status_lbl.configure(text="正在停止...", fg=YELLOW)
    status_port_lbl.configure(text="")
    chat_btn_frame.pack_forget()
    start_btn_ref.configure(state="disabled")
    stop_btn_ref.configure(state="disabled")
    stop_service()
    root.after(1200, lambda: (
        update_status(),
        start_btn_ref.configure(state="normal"),
        stop_btn_ref.configure(state="normal")
    ))

def do_start():
    status_dot.configure(bg=YELLOW)
    status_lbl.configure(text="正在启动...", fg=YELLOW)
    status_port_lbl.configure(text="")
    start_btn_ref.configure(state="disabled")
    stop_btn_ref.configure(state="disabled")
    chat_btn_frame.pack_forget()
    start_service()

    def poll_wait():
        running = check_port_open(get_port())
        if running:
            port = get_port()
            status_dot.configure(bg=GREEN)
            status_lbl.configure(text="运行中", fg=GREEN)
            status_port_lbl.configure(text=f"端口 {port}")
            start_btn_ref.configure(state="normal")
            stop_btn_ref.configure(state="normal")
            chat_btn_frame.pack(fill="x", pady=(0, 4))
            webbrowser.open(f"http://127.0.0.1:{port}/")
        else:
            start_btn_ref.configure(state="normal")
            stop_btn_ref.configure(state="normal")
            update_status()

    root.after(2500, poll_wait)

# === AI 配置 ===
ac = card(scrollable)
section_title(ac, "AI 配置")

ai_provider_var = tk.StringVar(value="minimax")
pf = tk.Frame(ac, bg=CARD)
pf.pack(fill="x", pady=(0, 4))
for val, txt in [("minimax", "MiniMax"), ("openai", "OpenAI"),
                 ("deepseek", "DeepSeek"), ("custom", "自定义")]:
    tk.Radiobutton(pf, text=txt, variable=ai_provider_var, value=val,
                   bg=CARD, fg=TEXT, activebackground=CARD, cursor="hand2",
                   selectcolor=ENTRY_BG, font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(0, 10))

apikey_e = field(ac, "API Key")
model_e = field(ac, "模型", entry_width=20)

# === 消息渠道 ===
cc = card(scrollable)
section_title(cc, "消息渠道")

# 飞书
feishu_en_var = tk.BooleanVar(value=False)
fe = tk.Frame(cc, bg=ENTRY_BG)
fe.pack(fill="x", pady=(0, 4))
fh = tk.Frame(fe, bg=ENTRY_BG)
fh.pack(fill="x", padx=12, pady=(8, 4))
tk.Label(fh, text="飞书", fg=TEXT, bg=ENTRY_BG, font=("Microsoft YaHei UI", 10, "bold")).pack(side="left")
tk.Checkbutton(fh, variable=feishu_en_var, bg=ENTRY_BG, activebackground=ENTRY_BG,
               cursor="hand2", onvalue=True, offvalue=False,
               selectcolor=ACCENT, indicatoron=False).pack(side="right")
fd = tk.Frame(fe, bg=ENTRY_BG)
fd.pack(fill="x", padx=12, pady=(0, 8))
tk.Label(fd, text="App ID", fg=TEXT_SEC, bg=ENTRY_BG, font=("Microsoft YaHei UI", 8), width=8).pack(side="left")
feishu_id_e = tk.Entry(fd, bg=BG, fg=TEXT, font=("Microsoft YaHei UI", 9),
                       insertbackground=TEXT, bd=0, highlightthickness=0, width=22)
feishu_id_e.pack(side="left")
tk.Label(fd, text="App Secret", fg=TEXT_SEC, bg=ENTRY_BG, font=("Microsoft YaHei UI", 8), width=9).pack(side="left", padx=(8, 0))
feishu_sec_e = tk.Entry(fd, bg=BG, fg=TEXT, font=("Microsoft YaHei UI", 9),
                        insertbackground=TEXT, bd=0, highlightthickness=0,
                        width=14, show="*")
feishu_sec_e.pack(side="left")

# Telegram
tg_en_var = tk.BooleanVar(value=False)
te = tk.Frame(cc, bg=ENTRY_BG)
te.pack(fill="x", pady=(0, 4))
th = tk.Frame(te, bg=ENTRY_BG)
th.pack(fill="x", padx=12, pady=(8, 4))
tk.Label(th, text="Telegram", fg=TEXT, bg=ENTRY_BG, font=("Microsoft YaHei UI", 10, "bold")).pack(side="left")
tk.Checkbutton(th, variable=tg_en_var, bg=ENTRY_BG, activebackground=ENTRY_BG,
               cursor="hand2", onvalue=True, offvalue=False,
               selectcolor=ACCENT, indicatoron=False).pack(side="right")
td = tk.Frame(te, bg=ENTRY_BG)
td.pack(fill="x", padx=12, pady=(0, 8))
tk.Label(td, text="Bot Token", fg=TEXT_SEC, bg=ENTRY_BG, font=("Microsoft YaHei UI", 8), width=8).pack(side="left")
tg_token_e = tk.Entry(td, bg=BG, fg=TEXT, font=("Microsoft YaHei UI", 9),
                       insertbackground=TEXT, bd=0, highlightthickness=0,
                       width=28, show="*")
tg_token_e.pack(side="left")

# 保存按钮
sf = tk.Frame(cc, bg=CARD, pady=4)
sf.pack(fill="x")
save_btn = btn(sf, "保存配置", lambda: save_all(), bg=ACCENT, fg="#ffffff", padx=16)

# === 加载 & 保存 ===
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
        messagebox.showwarning("警告", "API Key 不能为空")
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
    messagebox.showinfo("已保存", "配置保存成功")

# === 底部 ===
tk.Label(scrollable, text="所有数据保存在 U 盘", fg=TEXT_SEC, bg=BG,
         font=("Microsoft YaHei UI", 8)).pack(pady=14)

load_config()
update_status()

def poll():
    update_status()
    root.after(4000, poll)

root.after(1500, poll)
root.mainloop()