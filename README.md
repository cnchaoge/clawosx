# ClawOSX v1.0

> U 盘便携 AI Agent — 插上即用，数据随身走

**基于 OpenClaw 的便携式 AI 助手，运行在 U 盘上，不依赖宿主机环境。**

---

## 特性

- **即插即用** — 双击脚本即可启动，无需安装
- **数据随身** — 所有数据存在 U 盘，换电脑数据完全一致
- **轻量化** — 最小化 ~180MB（包含 Node.js + OpenClaw）
- **配置简单** — Python GUI 界面，配置 AI Key 和消息渠道

---

## 系统要求

- Windows 10/11
- U 盘（建议 8GB 以上，NTFS 或 exFAT 格式）
- 网络连接（首次 Setup 需要）
- Python 3（Windows 10+ 自带，Setup 脚本会自动检测）

---

## 快速开始

### 1. 下载并解压

下载最新 release，解压到 U 盘根目录：

```
U 盘:/
└── ClawOSX/
    ├── Windows-Setup.bat     ← 首次运行先点这个
    ├── Windows-Start.bat     ← 之后每次运行点这个
    └── ClawOSX-Config.bat   ← 配置 AI Key / 消息渠道（双击运行）
```

### 2. 首次 Setup（需要网络）

双击 `Windows-Setup.bat`，等待下载 Node.js 和 OpenClaw（约 1-3 分钟）。

### 3. 配置 AI

双击 `ClawOSX-Config.bat`，在 GUI 界面填写：
- AI Provider 和 API Key
- 消息渠道（飞书 / Telegram，可选）
- 点击 Save All 保存

### 4. 启动

双击 `Windows-Start.bat`，浏览器自动打开 Dashboard。

---

## 数据说明

所有数据保存在 U 盘 `data/` 目录：

```
data/
└── .openclaw/
    ├── openclaw.json   # 配置文件（含 API Key）
    ├── memory/          # AI 记忆
    └── logs/            # 运行日志
```

**备份方法**：直接拷贝整个 `data/` 目录即可。

---

## 常见问题

### ClawOSX-Config.bat 报错"找不到 Python"？

Windows 10/11 自带 Python。如果提示未安装，从 python.org 下载安装后重新插入 U 盘即可。

### 下载失败？

确保网络畅通，或手动使用 VPN。

### 启动报错"找不到 Node.js"？

请重新运行 `Windows-Setup.bat`。

### 端口被占用？

脚本会自动尝试 18789~18799，如果全部被占用请关闭其他程序。

### U 盘拔下后数据还在吗？

数据全部在 U 盘 `data/` 目录，拔盘带走，数据不会丢失。

---

## 版本

- 当前版本：v1.0.0
- OpenClaw：2026.5.26
- Node.js：v22.22.1

---

## 免责声明

本软件按原样提供，不提供任何明示或暗示的保证。使用者需自行承担使用风险。配置 API Key 前请确认来源可靠。

---

## License

MIT