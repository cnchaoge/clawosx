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

# === 配色 ===
BG = "#F4F6F9"
PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
SUCCESS = "#16A34A"
SUCCESS_HOVER = "#147a3e"
DANGER = "#DC2626"
DANGER_HOVER = "#b91c1c"
WARNING = "#D97706"
TEXT = "#111827"
TEXT_SEC = "#6B7280"
DIVIDER = "#E2E8F0"
INPUT_BG = "#FFFFFF"
INPUT_FOCUS = "#EFF6FF"
TOGGLE_OFF = "#D1D5DB"
PILL_BG = "#F1F5F9"
PILL_ACTIVE_BG = "#EFF6FF"
PILL_ACTIVE_BORDER = "#2563EB"

# === 主窗口 ===
root = tk.Tk()
root.title("ClawOSX 配置工具")
root.geometry("540x800")
root.minsize(480, 680)
root.configure(bg=BG)

canvas = tk.Canvas(root, bg=BG, highlightthickness=0, bd=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview, width=6)
scrollable = tk.Frame(canvas, bg=BG)

scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
canvas.bind_all("<MouseWheel>", on_mousewheel)

# === 通用组件 ===
def section(parent, label_text):
    """无边框全宽区块，顶部有标题+分隔线"""
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", pady=(0, 0))

    tk.Label(f, text=label_text, fg=TEXT, bg=BG,
             font=("Microsoft YaHei UI", 13, "bold"),
             anchor="w").pack(fill="x", padx=20, pady=(20, 6))

    tk.Frame(f, bg=DIVIDER, height=1).pack(fill="x", padx=20)
    return f

def entry_field(parent, label, width=28, show=""):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", padx=20, pady=3)
    tk.Label(f, text=label, fg=TEXT_SEC, bg=BG,
             font=("Microsoft YaHei UI", 10), width=10, anchor="w").pack(side="left")
    e = tk.Entry(f, bg=INPUT_BG, fg=TEXT, font=("Microsoft YaHei UI", 10),
                  insertbackground=TEXT, bd=1, relief="solid",
                  highlightthickness=0, width=width)
    e.pack(side="left")
    if show:
        e.config(show=show)
    def on_focus_in(_):
        e.config(bg=INPUT_FOCUS, bd=1, relief="solid",
                 highlightbackground=PRIMARY, highlightthickness=1)
    def on_focus_out(_):
        e.config(bg=INPUT_BG, bd=1, relief="solid",
                 highlightbackground=DIVIDER, highlightthickness=1)
    e.bind("<FocusIn>", on_focus_in)
    e.bind("<FocusOut>", on_focus_out)
    e.config(highlightbackground=DIVIDER, highlightthickness=1, relief="solid", bd=1)
    return e

def action_btn(parent, text, cmd, bg=PRIMARY, fg="#ffffff", expand=False):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=("Microsoft YaHei UI", 10, "bold"), bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  pady=7, padx=14)
    if expand:
        b.pack(fill="x", padx=20, pady=(0, 8))
    else:
        b.pack(side="left", padx=(0, 8))
    return b

# === 标题 ===
tk.Label(scrollable, text="ClawOSX", fg=TEXT, bg=BG,
         font=("Microsoft YaHei UI", 26, "bold")).pack(pady=(20, 2))
tk.Label(scrollable, text="U盘便携 AI 助手  ·  v1.0", fg=TEXT_SEC, bg=BG,
         font=("Microsoft YaHei UI", 10)).pack(pady=(0, 16))

# === 服务状态 ===
sc = section(scrollable, "服务状态")

status_inner = tk.Frame(sc, bg=BG)
status_inner.pack(fill="x", padx=20, pady=(10, 4))

dot_canvas = tk.Canvas(status_inner, width=12, height=12, bg=BG, bd=0, highlightthickness=0)
dot_canvas.pack(side="left", padx=(0, 8), pady=(4, 0))
dot_oval = dot_canvas.create_oval(0, 0, 11, 11, fill=TEXT_SEC, outline=TEXT_SEC)

status_lbl = tk.Label(status_inner, text="检测中...", fg=TEXT_SEC, bg=BG,
                       font=("Microsoft YaHei UI", 11, "normal"))
status_lbl.pack(side="left")
port_lbl = tk.Label(status_inner, text="", fg=TEXT_SEC, bg=BG,
                     font=("Microsoft YaHei UI", 10))
port_lbl.pack(side="right")

btn_row = tk.Frame(sc, bg=BG)
btn_row.pack(fill="x", padx=20, pady=(0, 4))
action_btn(btn_row, "刷新", lambda: update_status(), bg=PILL_BG, fg=TEXT)
stop_btn_ref = action_btn(btn_row, "停止", lambda: do_stop(), bg=DANGER, fg="#ffffff")
start_btn_ref = action_btn(btn_row, "启动", lambda: do_start(), bg=SUCCESS, fg="#ffffff")

# 开始聊天按钮
chat_btn_frame = tk.Frame(sc, bg=BG)
chat_btn_frame.pack(fill="x", padx=20, pady=(0, 8))
chat_btn = tk.Button(chat_btn_frame, text="开始聊天", command=lambda: open_browser(),
                    bg=SUCCESS, fg="#ffffff",
                    font=("Microsoft YaHei UI", 12, "bold"), bd=0, cursor="hand2",
                    activebackground=SUCCESS, activeforeground="#ffffff",
                    pady=9)
chat_btn.pack(fill="x")
chat_btn_frame.pack_forget()

def open_browser():
    port = get_port()
    webbrowser.open(f"http://127.0.0.1:{port}/")

def set_dot(color):
    dot_canvas.itemconfig(dot_oval, fill=color, outline=color)

def update_status():
    port = get_port()
    running = check_port_open(port)
    set_dot(SUCCESS if running else TEXT_SEC)
    status_lbl.configure(text="运行中" if running else "已停止",
                         fg=SUCCESS if running else TEXT_SEC)
    port_lbl.configure(text=f"端口 {port}" if running else "")
    if running:
        chat_btn_frame.pack(fill="x", padx=20, pady=(0, 8))
    else:
        chat_btn_frame.pack_forget()

def do_stop():
    set_dot(WARNING)
    status_lbl.configure(text="正在停止...", fg=WARNING)
    port_lbl.configure(text="")
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
    set_dot(WARNING)
    status_lbl.configure(text="正在启动...", fg=WARNING)
    port_lbl.configure(text="")
    start_btn_ref.configure(state="disabled")
    stop_btn_ref.configure(state="disabled")
    chat_btn_frame.pack_forget()
    start_service()

    def poll_wait():
        running = check_port_open(get_port())
        if running:
            port = get_port()
            set_dot(SUCCESS)
            status_lbl.configure(text="运行中", fg=SUCCESS)
            port_lbl.configure(text=f"端口 {port}")
            start_btn_ref.configure(state="normal")
            stop_btn_ref.configure(state="normal")
            chat_btn_frame.pack(fill="x", padx=20, pady=(0, 8))
            webbrowser.open(f"http://127.0.0.1:{port}/")
        else:
            start_btn_ref.configure(state="normal")
            stop_btn_ref.configure(state="normal")
            update_status()

    root.after(2500, poll_wait)

# === AI 配置 ===
ac = section(scrollable, "AI 配置")

ai_provider_var = tk.StringVar(value="minimax")
provider_options = [
    ("minimax", "MiniMax"),
    ("openai", "OpenAI"),
    ("deepseek", "DeepSeek"),
    ("custom", "自定义"),
]

pill_row = tk.Frame(ac, bg=BG)
pill_row.pack(fill="x", padx=20, pady=(8, 6))

pill_frames = {}
pill_labels = {}

def select_provider(val):
    ai_provider_var.set(val)
    for k in pill_frames:
        if k == val:
            pill_frames[k].config(bg=PILL_ACTIVE_BG, bd=1,
                                  highlightbackground=PILL_ACTIVE_BORDER,
                                  highlightthickness=1)
            pill_labels[k].config(fg=PRIMARY)
        else:
            pill_frames[k].config(bg=PILL_BG, bd=0,
                                  highlightbackground=DIVIDER,
                                  highlightthickness=1)
            pill_labels[k].config(fg=TEXT_SEC)

for val, txt in provider_options:
    f = tk.Frame(pill_row, bg=PILL_BG, bd=1, relief="flat",
                 highlightbackground=DIVIDER, highlightthickness=1)
    f.pack(side="left", padx=(0, 6))
    pill_frames[val] = f
    l = tk.Label(f, text=txt, fg=TEXT_SEC, bg=PILL_BG,
                  font=("Microsoft YaHei UI", 10), padx=16, pady=6, cursor="hand2")
    l.pack()
    pill_labels[val] = l
    def on_click(e, v=val):
        select_provider(v)
    l.bind("<Button-1>", on_click)
    f.bind("<Button-1>", lambda e, v=val: on_click(e, v))

select_provider("minimax")

apikey_e = entry_field(ac, "API Key")
model_e = entry_field(ac, "模型", width=20)

# === 消息渠道 ===
cc = section(scrollable, "消息渠道")

def channel_block(parent, name, id_label, sec_label):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", padx=20, pady=(8, 0))

    header = tk.Frame(f, bg=BG)
    header.pack(fill="x", pady=(0, 6))
    tk.Label(header, text=name, fg=TEXT, bg=BG,
             font=("Microsoft YaHei UI", 11, "bold")).pack(side="left")

    enable_var = tk.BooleanVar(value=False)
    toggle = tk.Frame(header, width=40, height=22, bg=TOGGLE_OFF, cursor="hand2")
    toggle.pack(side="right")
    toggle.config(highlightthickness=0)
    thumb = tk.Frame(toggle, width=14, height=14, bg="#ffffff", bd=0)
    thumb.pack(side="left", padx=4, pady=4)
    thumb.config(highlightthickness=0)

    def update_toggle():
        if enable_var.get():
            toggle.config(bg=PRIMARY)
            thumb.pack(side="right")
        else:
            toggle.config(bg=TOGGLE_OFF)
            thumb.pack(side="left")

    def on_toggle(e=None):
        enable_var.set(not enable_var.get())
        update_toggle()

    toggle.bind("<Button-1>", on_toggle)
    thumb.bind("<Button-1>", on_toggle)

    id_e = entry_field(f, id_label)
    sec_e = entry_field(f, sec_label, width=18)
    sec_e.config(show="*")
    return enable_var, id_e, sec_e

def tg_block(parent, name, token_label):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", padx=20, pady=(8, 0))

    header = tk.Frame(f, bg=BG)
    header.pack(fill="x", pady=(0, 6))
    tk.Label(header, text=name, fg=TEXT, bg=BG,
             font=("Microsoft YaHei UI", 11, "bold")).pack(side="left")

    enable_var = tk.BooleanVar(value=False)
    toggle = tk.Frame(header, width=40, height=22, bg=TOGGLE_OFF, cursor="hand2")
    toggle.pack(side="right")
    toggle.config(highlightthickness=0)
    thumb = tk.Frame(toggle, width=14, height=14, bg="#ffffff", bd=0)
    thumb.pack(side="left", padx=4, pady=4)
    thumb.config(highlightthickness=0)

    def update_toggle():
        if enable_var.get():
            toggle.config(bg=PRIMARY)
            thumb.pack(side="right")
        else:
            toggle.config(bg=TOGGLE_OFF)
            thumb.pack(side="left")

    def on_toggle(e=None):
        enable_var.set(not enable_var.get())
        update_toggle()

    toggle.bind("<Button-1>", on_toggle)
    thumb.bind("<Button-1>", on_toggle)

    token_e = entry_field(f, token_label, width=34)
    token_e.config(show="*")
    return enable_var, token_e

feishu_en_var, feishu_id_e, feishu_sec_e = channel_block(cc, "飞书", "App ID", "App Secret")
tg_en_var, tg_token_e = tg_block(cc, "Telegram", "Bot Token")

# 保存按钮
save_sec = tk.Frame(scrollable, bg=BG)
save_sec.pack(fill="x", pady=(16, 8))
action_btn(save_sec, "保存配置", lambda: save_all(), bg=PRIMARY, fg="#ffffff", expand=True)

# === 加载 & 保存 ===
def load_config():
    cfg = load_json(OPENCLAW_JSON)
    providers = cfg.get("models", {}).get("providers", {})
    for k, v in providers.items():
        ai_provider_var.set(k)
        select_provider(k)
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
         font=("Microsoft YaHei UI", 8)).pack(pady=12)

load_config()
update_status()

def poll():
    update_status()
    root.after(4000, poll)

root.after(1500, poll)
root.mainloop()