# ClawOSX 开发流程

> 飞书便携 AI 助手 · U 盘即插即用 · v1.0

---

## 一、项目概述

### 定位
基于 OpenClaw/Hermes 的便携式 AI Agent 助手，部署在 U 盘上即插即用、随时带走。

### 目标
- **零宿主机依赖**：U盘插上任意 Windows 电脑就能跑
- **数据全在U盘**：配置、日志、数据库都在 U 盘，不留痕
- **一键启动**：双击脚本即可，不需要命令行

### 技术栈
- **运行时**：Node.js v22.22.1（portable，不依赖宿主机）
- **核心**：OpenClaw v2026.5.26
- **配置工具**：HTA（HTML Application，Windows 内置，零依赖）
- **平台**：Windows 10/11

### 核心文件

| 文件 | 作用 |
|------|------|
| `Windows-Setup.bat` | 安装脚本（双击在本地跑，创建 U 盘环境） |
| `Windows-Start.bat` | 启动 Gateway |
| `ClawOSX-Config.bat` | 启动配置工具 |
| `clawosx_config.hta` | 图形配置工具（零依赖 HTA） |

### 目录结构（U盘）

```
F:\clawosx\
├── app\runtime\node-win-x64\    # Node.js 便携版
│   ├── node.exe
│   ├── npm.cmd
│   └── node_modules\
│       └── openclaw\            # OpenClaw
│           ├── openclaw.mjs
│           └── dist\entry.mjs   # 编译后的入口
├── data\
│   ├── .openclaw\
│   │   ├── openclaw.json        # 配置文件
│   │   └── port.txt             # 端口号文件
│   └── logs\gateway.log
├── Windows-Start.bat
├── ClawOSX-Config.bat
└── clawosx_config.hta
```

---

## 二、开发环境搭建

### 步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/cnchaoge/clawosx
   cd clawosx
   ```

2. **准备本地文件**
   - `node-v22.22.1-win-x64.zip` → 放到项目根目录或 `C:\ClawOSX\`
   - `openclaw-main.zip` 或完整 openclaw 包 → 同上

3. **准备测试机**
   - 格式化 U 盘（FAT32 或 NTFS）
   - 将 `C:\ClawOSX\` 内容复制到测试机本地磁盘（不要直接放 U 盘）

4. **运行 Setup**
   ```
   C:\ClawOSX\Windows-Setup.bat
   ```

5. **启动测试**
   ```
   F:\clawosx\Windows-Start.bat
   ```
   Gateway 运行后访问 http://127.0.0.1:端口号

---

## 三、Setup 流程详解（Windows-Setup.bat）

### 流程图

```
本地 zip → 本地提取（C:\Temp） → 移动到 U 盘
           ↓
    提取 Node.js zip（本地磁盘，I/O 快）
           ↓
    重命名目录（node-v22.22.1-win-x64 → node-win-x64）
           ↓
    移动到 F:\clawosx\app\runtime\node-win-x64\
           ↓
    提取 OpenClaw 包 → 移动到 node_modules\openclaw\
           ↓
    复制 ClawOSX 脚本到 U 盘根目录
           ↓
    清理本地临时文件
```

---

## 四、启动流程详解（Windows-Start.bat）

### 流程图

```
读取 port.txt 的端口号
      ↓
启动 node.exe → gateway --port 端口号 --auth none
      ↓
写日志到 data\logs\gateway.log
      ↓
轮询 http://127.0.0.1:端口号/ 直到 ready
      ↓
打开浏览器
```

---

## 五、踩过的坑（完整记录）

### ⚠️ 坑 1：HTA 编码问题
**现象**：HTA 文件中的中文显示乱码。  
**原因**：HTA 文件保存编码与页面声明不一致。  
**解决**：确保文件使用 UTF-8 并正确声明 charset。

---

### ⚠️ 坑 2：PowerShell `-Command` 单引号问题
**现象**：`powershell -Command "Expand-Archive ... -DestinationPath '%LOCAL_TEMP%'"` 失败。  
**原因**：`-Command` 参数中的单引号和 `%VAR%` 在某些调用方式下展开失效。  
**解决**：使用绝对路径字符串，不用变量替换路径。

---

### ⚠️ 坑 3：Node.js zip 嵌套目录
**现象**：解压后目录是 `node-v22.22.1-win-x64/node-v22.22.1-win-x64/`（嵌套了一层）。  
**原因**：zip 包内部包含以版本号命名的顶层目录。  
**解决**：提取后检测目录名，重命名为 `node-win-x64` 后再使用。

---

### ⚠️ 坑 4：OpenClaw dist/entry.mjs 缺失
**现象**：从 GitHub 下载源码包后运行报错 `missing dist/entry.(m)js`。  
**原因**：GitHub 源码包里没有 `dist/` 目录（需要 npm install 编译后才能生成）。  
**解决**：必须用 `npm install` 安装 OpenClaw，不能直接用 GitHub 源码 zip。

---

### ⚠️ 坑 5：`netstat` 端口检测挂起
**现象**：`netstat -ano | findstr :18789` 在 USB 盘上运行时卡住无响应。  
**原因**：USB 盘 I/O 慢，`netstat` 扫描全部连接时超时。  
**解决**：改用 PowerShell 的 `TcpClient` 检测端口联通性。

---

### ⚠️ 坑 6：随机端口 RANDOM_PORT 计算错误
**现象**：端口始终是 1878xx，不随机。  
**原因**：`set "RANDOM_PORT=1878%%a:~-3"` 字符串截取在引号内失效。  
**解决**：使用 `set /a RANDOM_PORT=1878*1000 + %RANDOM% % 1000`。

---

### ⚠️ 坑 7：subprocess creationflags 被忽略
**现象**：Gateway 进程没有正确以 detached 模式运行。  
**原因**：`creationflags=0x08000000` 配合 `shell=True` 使用时被忽略。  
**解决**：移除 `shell=True`，使用 `creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW`。

---

### ⚠️ 坑 8：`save_all()` 硬编码端口
**现象**：每次保存配置都会把端口重置为 18789。  
**原因**：`save_all()` 写死了 `DEFAULT_PORT`，而不是读取实际端口。  
**解决**：读取 `port.txt` 中的实际端口再写入。

---

### ⚠️ 坑 9：`cmd /c` 执行 npm.cmd
**现象**：`node npm.cmd install ...` 报错 "Cannot find module"。  
**原因**：`npm.cmd` 是批处理文件，必须由 `cmd.exe` 执行，不能被 `node.exe` 调用。  
**解决**：`cmd /c "cd /d \"%NODE_TARGET%\" && npm.cmd install ..."`。

---

### ⚠️ 坑 10：GitHub 源码包问题（同坑 4）
**现象**：下载 `openclaw-main.zip` 后运行报错 `missing dist/entry.(m)js`。  
**原因**：同上，npm install 才能生成编译后的文件。  
**解决**：不要用 GitHub 源码包。

---

### ⚠️ 坑 11：U 盘 move 命令在脚本内失败
**现象**：手动在 cmd 里跑 `move ...\* ...` 成功，但在 batch 脚本里失败（"系统找不到指定的文件"）。  
**原因**：`for /f` 循环里使用 `%LOCAL_TEMP%` 变量时路径解析异常，且 `>nul 2>&1` 隐藏了所有错误输出。  
**解决**：
1. 不使用 `for /f` 循环，直接写死绝对路径
2. 去掉所有 `>nul 2>&1`，让错误输出可见
3. 每步 move 后立即检测目标文件是否存在

---

### ⚠️ 坑 12：npm 的 bin 目录在 move 时丢失
**现象**：手动跑 `move` 后 `npm.cmd` 内部报错 "Cannot find module npm-prefix.js"。  
**原因**：通过中间目录转存时，某些隐含文件或目录结构不完整。  
**解决**：改用 `powershell Expand-Archive` 直接解压到 U 盘目标目录，不经过中间 move。

---

### ⚠️ 坑 13：Python 空壳 WindowsApps
**现象**：Windows 10/11 自带的 Python 在 WindowsApps 目录，是空壳 stub。  
**原因**：微软商店版 Python 安装后指向 WindowsApps 里的空壳。  
**解决**：最终方案改用纯 HTA，不依赖 Python。

---

### ⚠️ 坑 14：HTA 文件在 setup 脚本的复制列表里遗漏
**现象**：setup 跑完，HTA 文件不在 U 盘上。  
**原因**：`clawosx_config.hta` 没有加入 `copy` 命令列表。  
**解决**：在 setup 脚本的复制步骤加上 `copy /y "%LOCAL_DIR%\clawosx_config.hta" "%UCLAW_DIR%\"`。

---

### ⚠️ 坑 15：wmic 无法检测 USB 盘符
**现象**：`wmic logicaldisk where "DriveType=2"` 返回空。  
**原因**：部分 Windows 环境下 wmic 的 USB 过滤失效。  
**解决**：硬编码 `USB_DRIVE=F`，或让用户输入。

---

### ⚠️ 坑 16：USB 盘符被其他程序占用
**现象**：脚本运行到一半，"系统找不到指定的文件"，但手动操作同一个路径成功。  
**原因**：杀毒软件或 Windows 自动扫描 USB 盘时短暂锁定。  
**解决**：每步操作后检测文件存在，不存在则延时重试（最多3次）。

---

## 六、测试标准

### 6.1 全新安装测试
1. 格式化 U 盘
2. 复制 setup 文件到 `C:\ClawOSX\`
3. 运行 `Windows-Setup.bat`
4. 确认无 ERROR 输出，每步都显示 [OK]
5. 检查 U 盘 `F:\clawosx\` 目录结构完整
6. 运行 `Windows-Start.bat`，确认 Gateway ready
7. 双击 `ClawOSX-Config.bat`，确认 HTA 界面打开

### 6.2 增量更新测试
1. 只更新 zip 包（保留 U 盘其他文件）
2. 运行 setup，确认跳过已存在文件
3. 清理本地临时目录后重跑

### 6.3 冷启动测试
1. 关机
2. U 盘插到另一台 Windows 电脑
3. 运行 `Windows-Start.bat`
4. 确认 Gateway 正常启动

---

## 七、GitHub 提交流骤

> ⚠️ **测试通过后再提交。未通过测试不要 push。**

```bash
cd /Users/chaoge/clawosx

# 1. 检查状态
git status

# 2. 添加文件
git add .

# 3. 提交
git commit -m "v1.0 - initial release"

# 4. 推送
git push origin main
```

---

## 八、文件清单

| 文件 | 是否提交 | 说明 |
|------|:--:|------|
| `Windows-Setup.bat` | ✅ | 安装脚本 |
| `Windows-Start.bat` | ✅ | 启动脚本 |
| `ClawOSX-Config.bat` | ✅ | 配置工具启动脚本 |
| `clawosx_config.hta` | ✅ | HTA 配置工具 |
| `OPENCLAW_VERSION` | ✅ | 版本号记录 |
| `README.md` | ✅ | 说明文档 |
| `AGENTS.md` | ✅ | 开发指南 |
| `DEVELOPMENT.md` | ✅ | 开发流程文档 |
| `node-*.zip` | ❌ | 第三方文件，不提交 |
| `openclaw-*.zip` | ❌ | npm 安装产物，不提交 |

---

## 九、关键原则

1. **零宿主机依赖**：配置工具不能依赖任何未预装的软件
2. **ASCII 输出**：批处理文件 echo 不能用中文字符（GBK 编码问题）
3. **本地优先**：zip 提取在本地磁盘 C:\Temp，复制到 U 盘再删临时文件
4. **每步验证**：move/copy 后立即检测目标，不轻信 [OK] 输出
5. **不隐藏错误**：只在确认成功的步骤使用 `>nul`，失败必须显示
6. **测试后才能 push**：未通过测试的代码不允许提交到 GitHub

---

_最后更新：2026-05-29_