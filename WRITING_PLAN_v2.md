# ClawOSX v1.0 MVP — Writing Plan v2

> 基于 Codex v1 审查反馈 + u-claw 参考方案，确定的最简实现路径。

---

## 背景

ClawOSX 目标：打造一款基于 OpenClaw 的 U 盘便携 AI Agent，插上任何 Windows 电脑，双击即跑，数据全在 U 盘，不依赖宿主机环境。

---

## 核心方案

### 技术选型

| 组件 | 选择 | 说明 |
|------|------|------|
| 运行时 | OpenClaw | npm 包，直接 `node openclaw.mjs gateway run` |
| Node.js | Portable Node.js 22.x | 解压即用，不依赖宿主机 |
| 启动脚本 | Windows Batch (.bat) | 双击即可运行，无需命令行 |
| 数据 | U 盘存储 | 环境变量指向 U 盘路径 |
| 前端 | 无 | 直接使用 OpenClaw 内置 Dashboard |
| 版本 | OpenClaw `2026.5.26` | 固定版本，release 时更新 |

### 关键设计

1. **双击启动**：`Windows-Start.bat` → 设置环境变量 → 启动 Gateway → 浏览器打开 Dashboard
2. **数据隔离**：所有 `.openclaw` 数据存在 U 盘 `data/` 目录，拔盘带走
3. **首次 Setup**：`Windows-Setup.bat` 下载 Node.js + 安装 OpenClaw，之后日常用 `Windows-Start.bat`
4. **无 Config.html**：用户直接访问 OpenClaw Dashboard 配置 AI Provider
5. **无预装 Skills**：v1 纯 Gateway，不装任何 Skill

---

## 目录结构

```
clawosx/
├── Windows-Setup.bat       # 首次运行：下载 Node.js + 安装 OpenClaw
├── Windows-Start.bat      # 日常启动：设置环境变量 + 跑 Gateway
├── OPENCLAW_VERSION       # 版本号 2026.5.26
├── README.md              # 用户使用说明
├── AGENTS.md              # 给 AI 看的项目说明
├── LICENSE                # MIT
├── .gitignore
└── data/                   # （Setup 后自动生成）
    └── .openclaw/          # openclaw.json 配置
```

```
# Setup 后生成的目录（app/ 不进 git）
app/
├── core/                  # OpenClaw + node_modules
│   ├── package.json
│   └── node_modules/
└── runtime/
    └── node-win-x64/      # Portable Node.js 22.x
        ├── node.exe
        └── ...
```

**注意**：`app/` 目录和 `data/` 目录由 Setup 脚本自动生成，**不提交到 Git**。

---

## 环境变量策略

`Windows-Start.bat` 设置：

```batch
set "UCLAW_DIR=%~dp0"
set "APP_DIR=%UCLAW_DIR%app"
set "DATA_DIR=%UCLAW_DIR%data"
set "STATE_DIR=%DATA_DIR%\.openclaw"

set "OPENCLAW_HOME=%DATA_DIR%"
set "OPENCLAW_STATE_DIR=%STATE_DIR%"
set "OPENCLAW_CONFIG_PATH=%STATE_DIR%\openclaw.json"
set "OPENCLAW_DISABLE_BONJOUR=1"
```

---

## 脚本详解

### Windows-Setup.bat

**作用**：首次运行时下载 Node.js + 安装 OpenClaw + 初始化 data 目录

**流程**：
1. 检测 `app/runtime/node-win-x64/node.exe` 是否已存在 → 已存在则跳过 Node.js 下载
2. 从国内镜像 `npmmirror.com/mirrors/node` 下载 Node.js 22.x win-x64 zip
3. 解压到 `app/runtime/node-win-x64/`
4. `npm install openclaw@2026.5.26 --prefix app/core --registry npmmirror`
5. 初始化 `data/` 目录结构
6. 创建默认 `openclaw.json`（gateway mode=local）
7. 完成后提示"可以运行 Windows-Start.bat 了"

**错误处理**：
- 网络失败：提示重试，说明需要网络
- 磁盘空间不足：提前检测，提示至少需要 500MB
- 解压失败：提示检查是否安装了压缩工具

---

### Windows-Start.bat

**作用**：日常启动，双击即跑

**流程**：
1. 设置环境变量（OPENCLAW_HOME / STATE_DIR / CONFIG_PATH）
2. 创建必要目录（data/、data/.openclaw/、memory/、backups/）
3. 找空闲端口（18789 → 18799）
4. 启动 OpenClaw Gateway：`node app/core/node_modules/openclaw/openclaw.mjs gateway run --port %PORT% --force`
5. 等待 3 秒
6. 浏览器打开 `http://127.0.0.1:%PORT%/#token=uclaw`
7. 显示"不要关闭此窗口"，保持前台运行

**进程管理**：
- 关闭窗口 → SIGTERM → 等待 2s → SIGKILL
- Gateway 异常退出 → 显示错误信息，pause 等待用户确认

**数据目录初始化**：
```batch
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%STATE_DIR%" mkdir "%STATE_DIR%"
if not exist "%DATA_DIR%\memory" mkdir "%DATA_DIR%\memory"
if not exist "%DATA_DIR%\backups" mkdir "%DATA_DIR%\backups"
if not exist "%DATA_DIR%\logs" mkdir "%DATA_DIR%\logs"
```

**首次运行默认配置**（仅当 openclaw.json 不存在时）：
```json
{"gateway":{"mode":"local","auth":{"token":"uclaw"}}}
```

---

## 功能范围

### v1.0 MVP 做

| 功能 | 说明 |
|------|------|
| 双击启动 | Windows-Start.bat 双击，浏览器打开 Dashboard |
| 数据随身 | 所有数据在 U 盘 data/ 目录，拔盘带走 |
| 多 AI Provider | Dashboard 配置，支持 OpenAI/DeepSeek/Kimi 等 |
| 记忆持久化 | 写入 data/.openclaw/，重启后记忆保留 |
| 跨电脑使用 | 同一 U 盘插到不同 Windows PC，功能一致 |
| 多端口探测 | 18789 被占用时自动尝试 18790~18799 |

### v1.0 MVP 不做

- Config.html（直接用 Dashboard 配置）
- 任何预装 Skills
- macOS 支持
- 自动更新
- 多账号/多渠道
- 图形设置界面

---

## 验收标准

| # | 标准 | 测试方法 |
|---|------|----------|
| 1 | 双击 Windows-Start.bat → 浏览器打开 Dashboard，Agent 能回复 | U 盘插上电脑，双击运行 |
| 2 | 对话里说"记住我叫超哥"，关掉重启，问"我叫什么"能答对 | 重启验证记忆持久化 |
| 3 | U 盘拔下插到另一台 Windows PC → data/ 完整 → 功能一致 | 换电脑测试 |
| 4 | 18789 被占用时自动用 18790 | 占用 18789 后启动，应自动跳到 18790 |
| 5 | 不依赖宿主机 Python/Node.js | 在完全干净的 Windows 上测试 |
| 6 | Setup 完成后，文件结构符合预期 | 检查 app/core/ 和 app/runtime/ 是否完整 |

---

## 文件说明

### Windows-Setup.bat

```batch
# 核心变量
set "NODE_VERSION=v22.22.1"
set "OPENCLAW_VERSION=2026.5.26"
set "NODE_MIRROR=https://npmmirror.com/mirrors/node"
set "NPM_MIRROR=https://registry.npmmirror.com"

# 只下载当前平台（Windows x64），不下载 Mac 版本
```

### Windows-Start.bat

```batch
# 关键环境变量
set "OPENCLAW_HOME=%DATA_DIR%"
set "OPENCLAW_STATE_DIR=%STATE_DIR%"
set "OPENCLAW_CONFIG_PATH=%STATE_DIR%\openclaw.json"
set "OPENCLAW_DISABLE_BONJOUR=1"

# 启动命令
node app/core/node_modules/openclaw/openclaw.mjs gateway run --port %PORT% --force
```

### OPENCLAW_VERSION

```
2026.5.26
```

### README.md 内容

- 简介：ClawOSX 是什么
- 安装：插上 U 盘 → 运行 Windows-Setup.bat → 运行 Windows-Start.bat
- 首次配置：在 Dashboard 配置 AI Provider
- 数据说明：数据在哪，如何备份
- 常见问题

### AGENTS.md 内容

- 项目背景
- 技术架构（OpenClaw Gateway 模式）
- 环境变量说明
- 关键文件路径
- Coding 规范

---

## 实施顺序

### Step 1: 项目初始化
- [ ] 创建 GitHub 仓库 `clawosx`
- [ ] 初始化本地目录结构
- [ ] 创建 OPENCLAW_VERSION 文件
- [ ] 编写 AGENTS.md / README.md / LICENSE / .gitignore

### Step 2: Windows-Setup.bat
- [ ] 下载 Node.js（国内镜像）
- [ ] 解压到 app/runtime/node-win-x64/
- [ ] npm install openclaw@2026.5.26
- [ ] 初始化 data/ 目录结构
- [ ] 错误处理和用户提示

### Step 3: Windows-Start.bat
- [ ] 环境变量设置
- [ ] 目录初始化
- [ ] 端口探测
- [ ] 启动 Gateway
- [ ] 浏览器打开 Dashboard
- [ ] 进程管理（退出处理）

### Step 4: 本地验证
- [ ] 在 Mac 上通过 Wine/虚拟机 或找一台 Windows 机器测试
- [ ] 验证 Setup 脚本
- [ ] 验证 Start 脚本
- [ ] 验证记忆持久化
- [ ] 验证跨电脑数据一致性

### Step 5: GitHub push
- [ ] 第一版 commit（不含 app/ 和 data/）
- [ ] 创建 GitHub Releases（附带 app/runtime/node-win-x64/ 作为 release asset）

---

## 技术风险 & 缓解

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| Windows 上 Node.js 下载失败 | 低 | 高 | 提示网络问题，说明需要稳定网络 |
| npm install 失败（依赖问题） | 低 | 高 | 用国内镜像，版本固定，减少依赖问题 |
| 端口全部被占用 | 极低 | 中 | 遍历 18789~18799，提示"无可用端口" |
| U 盘性能差导致启动慢 | 中 | 低 | 首次启动后 data 已存在，后续直接用 |
| OpenClaw 版本有 bug | 低 | 高 | 固定版本，release 前人工测试 |

---

## 预计体积

| 部分 | 大小 |
|------|------|
| Windows-Setup.bat + Windows-Start.bat | < 50KB |
| OpenClaw + node_modules | ~150MB |
| Node.js 22.x win-x64 | ~30MB |
| data/ 模板 | < 1MB |
| **总计** | **~180MB** |

建议 U 盘：8GB 以上

---

## 待补充说明

### release assets 策略

v1 release 建议附带 **预装好 Node.js 的完整 zip**，用户可以：
1. 下载 `clawosx-portable-windows-v1.0.zip`（~180MB）
2. 解压到 U 盘
3. 双击 `Windows-Start.bat` 直接跑

这样不需要 Setup 过程，一步到位。

---

**超哥确认后开始 Coding。**