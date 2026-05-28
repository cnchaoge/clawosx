# AGENTS.md — ClawOSX Project

## 项目背景

ClawOSX 是一款 U 盘便携 AI Agent，基于 OpenClaw 框架，插上任何 Windows 电脑双击即跑，数据全在 U 盘不依赖宿主机。

## 技术架构

```
Windows-Start.bat
    ↓ 设置环境变量
    ↓ 启动 node + openclaw.mjs gateway run
    ↓
OpenClaw Gateway (WebSocket, 端口 18789)
    ↓
浏览器打开 Dashboard (http://127.0.0.1:18789)
```

## 关键路径

| 路径 | 说明 |
|------|------|
| `app/runtime/node-win-x64/node.exe` | Portable Node.js 22.x |
| `app/core/node_modules/openclaw/openclaw.mjs` | OpenClaw 入口 |
| `data/.openclaw/openclaw.json` | 配置文件 |
| `data/memory/` | AI 记忆目录 |
| `data/logs/` | 运行日志 |

## 环境变量

| 变量 | 值 |
|------|-----|
| `OPENCLAW_HOME` | `%DATA_DIR%` |
| `OPENCLAW_STATE_DIR` | `%DATA_DIR%\.openclaw` |
| `OPENCLAW_CONFIG_PATH` | `%DATA_DIR%\.openclaw\openclaw.json` |
| `OPENCLAW_DISABLE_BONJOUR` | `1` |

## 入口命令

```batch
node app\core\node_modules\openclaw\openclaw.mjs gateway run --allow-unconfigured --force --port 18789
```

## 目录结构

```
clawosx/
├── Windows-Setup.bat      # 首次：下载 Node.js + 安装 OpenClaw
├── Windows-Start.bat      # 日常：启动 Gateway
├── OPENCLAW_VERSION       # 2026.5.26
├── README.md
├── AGENTS.md
├── LICENSE
├── .gitignore
└── data/                   # 运行时生成，不进 git
    └── .openclaw/
```

## Coding 规范

- Batch 脚本：UTF-8 with BOM 编码，`chcp 65001`
- 环境变量用 `set "VAR=value"` 避免空格问题
- 路径用 `%~dp0` 获取脚本所在目录
- 错误处理：`if errorlevel 1` 或 `if %errorlevel%==0`
- 中文提示用方括号：`[OK]` / `[ERROR]` / `[下载]`

## 构建说明

### 生成 release zip（不含 app/runtime 和 app/core）

```bash
cd clawosx
zip -r clawosx-portable-windows-v1.0.zip . -x "app/*" "data/*" ".git/*"
```

用户下载后：
1. 解压到 U 盘
2. 双击 Windows-Setup.bat
3. 等待下载 Node.js + OpenClaw
4. 双击 Windows-Start.bat 启动

### 完整 release（含预装 Node.js 但不含 node_modules）

由于 OpenClaw npm 包较大，不建议打包进 release，让用户自己 Setup 下载。

## 已知限制

- v1.0 仅支持 Windows
- 首次 Setup 需要网络连接
- 无预装 Skills
- 无自动更新