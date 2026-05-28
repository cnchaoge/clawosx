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

# === 设计规范 ===
BG = "#F4F6F9"
CARD_BG = "#FFFFFF"
PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#D97706"
TEXT = "#111827"
TEXT_SEC = "#6B7280"
BORDER = "#E2E8F0"
INPUT_BG = "#F8FAFC"
INPUT_FOCUS = "#EFF6FF"
DISABLED = "#D1D5DB"
INNER_BG = "#F8FAFC"

# === 主窗口 ===
root = tk.Tk()
root.title("ClawOSX 配置工具")
root.geometry("560x820")
root.minsize(500, 720)
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
    f = tk.Frame(parent, bg=CARD_BG, bd=1, relief="solid",
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="x", pady=5)
    return f

def section_title(parent, text):
    """标题 + 左边蓝色竖线"""
    title_f = tk.Frame(parent, bg=CARD_BG)
    title_f.pack(fill="x", pady=(14, 8), padx=20)
    accent = tk.Frame(title_f, width=3, bg=PRIMARY)
    accent.pack(side="left", padx=(0, 8), fill="y")
    accent.config(highlightthickness=0)
    tk.Label(title_f, text=text, fg=PRIMARY, bg=CARD_BG,
             font=("Microsoft YaHei UI", 9, "bold"),
             anchor="w").pack(side="left")

def sep(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=(6, 4))

def entry_field(parent, label, width=28):
    f = tk.Frame(parent, bg=CARD_BG)
    f.pack(fill="x", pady=2)
    tk.Label(f, text=label, fg=TEXT_SEC, bg=CARD_BG,
             font=("Microsoft YaHei UI", 9), width=10, anchor="w").pack(side="left", padx=(20, 6))
    e = tk.Entry(f, bg=INPUT_BG, fg=TEXT, font=("Microsoft YaHei UI", 10),
                  insertbackground=TEXT, bd=0, relief="flat",
                  highlightthickness=1, highlightcolor=PRIMARY,
                  highlightbackground=BORDER, width=width)
    e.pack(side="left")
    # Focus effects
    def on_focus_in(_):
        e.config(bg=INPUT_FOCUS, relief="groove")
    def on_focus_out(_):
        e.config(bg=INPUT_BG, relief="flat")
    e.bind("<FocusIn>", on_focus_in)
    e.bind("<FocusOut>", on_focus_out)
    return e

def btn(parent, text, cmd, bg=PRIMARY, fg="#ffffff", padx=14):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=("Microsoft YaHei UI", 10, "bold"), bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  pady=5, padx=padx)
    b.pack(side="left", padx=(0, 6))
    def on_enter(e):
        if bg == PRIMARY:
            b.config(bg=PRIMARY_HOVER)
        elif bg == SUCCESS:
            b.config(bg="#147a3e")
        elif bg == DANGER:
            b.config(bg="#b91c1c")
        elif bg == DISABLED:
            b.config(bg="#c4c9d1")
        else:
            b.config(bg="#d1d5db")
    def on_leave(e):
        b.config(bg=bg)
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    return b

# === 标题区（无卡片） ===
tk.Label(scrollable, text="ClawOSX", fg=TEXT, bg=BG,
         font=("Microsoft YaHei UI", 24, "bold")).pack(pady=(20, 2))
tk.Label(scrollable, text="U盘便携 AI 助手  ·  v1.0", fg=TEXT_SEC, bg=BG,
         font=("Microsoft YaHei UI", 10)).pack(pady=(0, 14))

# === 服务状态卡片 ===
sc = card(scrollable)

# 状态行
status_row = tk.Frame(sc, bg=CARD_BG)
status_row.pack(fill="x", padx=20, pady=(12, 4))
status_dot_wrap = tk.Frame(status_row, width=14, height=14, bg=CARD_BG)
status_dot_wrap.pack(side="left", padx=(0, 10))
status_dot_wrap.config(highlightthickness=0)
dot_canvas = tk.Canvas(status_dot_wrap, width=14, height=14, bg=CARD_BG,
                        bd=0, highlightthickness=0)
dot_canvas.pack()
dot_oval = dot_canvas.create_oval(1, 1, 13, 13, fill=TEXT_SEC, outline=TEXT_SEC)
status_lbl = tk.Label(status_row, text="检测中...", fg=TEXT_SEC, bg=CARD_BG,
                       font=("Microsoft YaHei UI", 10, "normal"))
status_lbl.pack(side="left")
port_lbl = tk.Label(status_row, text="", fg=TEXT_SEC, bg=CARD_BG,
                     font=("Microsoft YaHei UI", 9))
port_lbl.pack(side="right")

sep(sc)

# 操作按钮行
btn_row = tk.Frame(sc, bg=CARD_BG)
btn_row.pack(fill="x", padx=20, pady=8)
btn(btn_row, "刷新", lambda: update_status(), bg=BORDER, fg=TEXT)
stop_btn_ref = btn(btn_row, "停止", lambda: do_stop(), bg=DANGER, fg="#ffffff")
start_btn_ref = btn(btn_row, "启动", lambda: do_start(), bg=SUCCESS, fg="#ffffff")

# 开始聊天按钮
chat_btn_frame = tk.Frame(sc, bg=CARD_BG)
chat_btn_frame.pack(fill="x", padx=20, pady=(0, 12))
chat_btn = tk.Button(chat_btn_frame, text="开始聊天", command=lambda: open_browser(),
                    bg=SUCCESS, fg="#ffffff",
                    font=("Microsoft YaHei UI", 12, "bold"), bd=0, cursor="hand2",
                    activebackground=SUCCESS, activeforeground="#ffffff",
                    pady=8)
chat_btn.pack(fill="x", ipady=5)
chat_btn_frame.pack_forget()  # 初始隐藏

def open_browser():
    port = get_port()
    webbrowser.open(f"http://127.0.0.1:{port}/")

def set_dot_color(color):
    dot_canvas.itemconfig(dot_oval, fill=color, outline=color)

def update_status():
    port = get_port()
    running = check_port_open(port)
    set_dot_color(SUCCESS if running else TEXT_SEC)
    status_lbl.configure(text="运行中" if running else "已停止",
                         fg=SUCCESS if running else TEXT_SEC)
    port_lbl.configure(text=f"端口 {port}" if running else "")
    if running:
        chat_btn_frame.pack(fill="x", padx=20, pady=(0, 12))
    else:
        chat_btn_frame.pack_forget()

def do_stop():
    set_dot_color(WARNING)
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
    set_dot_color(WARNING)
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
            set_dot_color(SUCCESS)
            status_lbl.configure(text="运行中", fg=SUCCESS)
            port_lbl.configure(text=f"端口 {port}")
            start_btn_ref.configure(state="normal")
            stop_btn_ref.configure(state="normal")
            chat_btn_frame.pack(fill="x", padx=20, pady=(0, 12))
            webbrowser.open(f"http://127.0.0.1:{port}/")
        else:
            start_btn_ref.configure(state="normal")
            stop_btn_ref.configure(state="normal")
            update_status()

    root.after(2500, poll_wait)

# === AI 配置卡片 ===
ac = card(scrollable)
section_title(ac, "AI 配置")

# Provider 选项卡
pf = tk.Frame(ac, bg=CARD_BG)
pf.pack(fill="x", padx=20, pady=(0, 10))

ai_provider_var = tk.StringVar(value="minimax")
provider_options = [
    ("minimax", "MiniMax"),
    ("openai", "OpenAI"),
    ("deepseek", "DeepSeek"),
    ("custom", "自定义"),
]

provider_frames = {}
def select_provider(val):
    ai_provider_var.set(val)
    for k, f in provider_frames.items():
        if k == val:
            f.config(bg=INPUT_FOCUS, bd=0, relief="flat",
                     highlightbackground=PRIMARY, highlightthickness=1)
        else:
            f.config(bg=INPUT_BG, bd=0, relief="flat",
                     highlightbackground=BORDER, highlightthickness=1)

for val, txt in provider_options:
    f = tk.Frame(pf, bg=INPUT_BG, bd=1, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(side="left", padx=(0, 6))
    provider_frames[val] = f
    lbl = tk.Label(f, text=txt, fg=TEXT_SEC, bg=INPUT_BG,
                    font=("Microsoft YaHei UI", 9), padx=12, pady=5,
                    cursor="hand2")
    lbl.pack()
    def on_click(e, v=val):
        select_provider(v)
        # Update label colors
        for k, ff in provider_frames.items():
            l = ff.winfo_children()[0]
            if k == v:
                l.config(fg=PRIMARY, bg=INPUT_FOCUS)
                ff.config(bg=INPUT_FOCUS, highlightbackground=PRIMARY)
            else:
                l.config(fg=TEXT_SEC, bg=INPUT_BG)
                ff.config(bg=INPUT_BG, highlightbackground=BORDER)
    lbl.bind("<Button-1>", on_click)
    f.bind("<Button-1>", lambda e, v=val: on_click(e, v))

# 初始状态
select_provider("minimax")
on_click(None, "minimax")

apikey_e = entry_field(ac, "API Key")
model_e = entry_field(ac, "模型", width=20)

# === 消息渠道卡片 ===
cc = card(scrollable)
section_title(cc, "消息渠道")

def channel_section(parent, name, id_label, sec_label, id_key, sec_key):
    """可复用的渠道配置区块"""
    box = tk.Frame(parent, bg=INNER_BG, bd=1, relief="flat",
                   highlightbackground=BORDER, highlightthickness=1)
    box.pack(fill="x", padx=20, pady=(0, 8))

    header = tk.Frame(box, bg=INNER_BG)
    header.pack(fill="x", padx=12, pady=(10, 4))
    tk.Label(header, text=name, fg=TEXT, bg=INNER_BG,
             font=("Microsoft YaHei UI", 10, "bold")).pack(side="left")

    enable_var = tk.BooleanVar(value=False)
    toggle_frame = tk.Frame(header, bg=INNER_BG)
    toggle_frame.pack(side="right")
    toggle_track = tk.Frame(toggle_frame, width=36, height=20, bg=DISABLED)
    toggle_track.pack(side="left", pady=3)
    toggle_track.config(highlightthickness=0)
    toggle_thumb = tk.Frame(toggle_track, width=14, height=14,
                             bg="#ffffff", bd=0)
    toggle_thumb.pack(side="left", padx=3, pady=3)
    toggle_thumb.config(highlightthickness=0)

    def update_toggle():
        if enable_var.get():
            toggle_track.config(bg=PRIMARY)
            toggle_thumb.pack(side="right")
        else:
            toggle_track.config(bg=DISABLED)
            toggle_thumb.pack(side="left")

    def on_toggle():
        enable_var.set(not enable_var.get())
        update_toggle()

    toggle_frame.bind("<Button-1>", lambda e: on_toggle())
    toggle_track.bind("<Button-1>", lambda e: on_toggle())
    toggle_thumb.bind("<Button-1>", lambda e: on_toggle())

    fields = tk.Frame(box, bg=INNER_BG)
    fields.pack(fill="x", padx=12, pady=(0, 10))
    id_e = entry_field(fields, id_label)
    sec_e = entry_field(fields, sec_label, width=18)
    sec_e.config(show="*")
    return enable_var, id_e, sec_e

feishu_en_var, feishu_id_e, feishu_sec_e = channel_section(
    cc, "飞书", "App ID", "App Secret", "appId", "appSecret")
tg_en_var, tg_token_e = None, None

def tg_channel_section(parent, name, token_label, token_key):
    box = tk.Frame(parent, bg=INNER_BG, bd=1, relief="flat",
                   highlightbackground=BORDER, highlightthickness=1)
    box.pack(fill="x", padx=20, pady=(0, 8))
    header = tk.Frame(box, bg=INNER_BG)
    header.pack(fill="x", padx=12, pady=(10, 4))
    tk.Label(header, text=name, fg=TEXT, bg=INNER_BG,
             font=("Microsoft YaHei UI", 10, "bold")).pack(side="left")
    enable_var = tk.BooleanVar(value=False)
    toggle_frame = tk.Frame(header, bg=INNER_BG)
    toggle_frame.pack(side="right")
    toggle_track = tk.Frame(toggle_frame, width=36, height=20, bg=DISABLED)
    toggle_track.pack()
    toggle_track.config(highlightthickness=0)
    toggle_thumb = tk.Frame(toggle_track, width=14, height=14, bg="#ffffff", bd=0)
    toggle_thumb.pack(side="left", padx=3, pady=3)
    toggle_thumb.config(highlightthickness=0)

    def update_toggle():
        if enable_var.get():
            toggle_track.config(bg=PRIMARY)
            toggle_thumb.pack(side="right")
        else:
            toggle_track.config(bg=DISABLED)
            toggle_thumb.pack(side="left")

    def on_toggle():
        enable_var.set(not enable_var.get())
        update_toggle()

    toggle_frame.bind("<Button-1>", lambda e: on_toggle())
    toggle_track.bind("<Button-1>", lambda e: on_toggle())
    toggle_thumb.bind("<Button-1>", lambda e: on_toggle())

    fields = tk.Frame(box, bg=INNER_BG)
    fields.pack(fill="x", padx=12, pady=(0, 10))
    token_e = entry_field(fields, token_label, width=32)
    token_e.config(show="*")
    return enable_var, token_e

tg_en_var, tg_token_e = tg_channel_section(cc, "Telegram", "Bot Token", "botToken")

# 保存按钮
save_row = tk.Frame(cc, bg=CARD_BG)
save_row.pack(fill="x", pady=(0, 14))
save_btn = btn(save_row, "保存配置", lambda: save_all(), bg=PRIMARY, fg="#ffffff", padx=20)

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

# Init
load_config()
update_status()

def poll():
    update_status()
    root.after(4000, poll)

root.after(1500, poll)
root.mainloop()