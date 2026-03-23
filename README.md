# OpenClaw Prompt Switcher

快速切换 OpenClaw 提示词配置 + 智能体管理工具。

---

## 功能

- 📋 **提示词管理** - 快速切换不同场景的提示词
- 🤖 **智能体创建** - 预设多个专业智能体，一键部署到 OpenClaw
- 🔄 **多端同步** - 通过 GitHub 在任意电脑同步配置

---

## 快速开始

```bash
# 克隆项目
git clone https://github.com/Yhazrin/openclaw-prompt-switcher.git
cd openclaw-prompt-switcher

# 切换提示词
python3 switch.py --switch coding

# 创建预设智能体
python3 agent_manager.py --create coding-assistant
```

---

## 提示词切换 (switch.py)

```bash
# 查看所有提示词
python3 switch.py --list

# 切换提示词
python3 switch.py --switch coding

# 添加新提示词
python3 switch.py --add my-prompt

# 编辑提示词
python3 switch.py --edit my-prompt
```

---

## 智能体管理 (agent_manager.py)

```bash
# 列出所有预设智能体
python3 agent_manager.py --list

# 查看智能体详情
python3 agent_manager.py --show coding-assistant

# 创建智能体到 OpenClaw
python3 agent_manager.py --create coding-assistant

# 创建新的预设智能体
python3 agent_manager.py --new my-agent --description "我的助手"

# 编辑智能体配置
python3 agent_manager.py --edit my-agent

# 编辑智能体提示词
python3 agent_manager.py --edit-prompt my-agent

# 删除 OpenClaw 中的智能体
python3 agent_manager.py --delete my-agent

# 绑定到频道
python3 agent_manager.py --bind my-agent telegram:mychat
```

---

## 预设智能体

| 智能体 | 描述 |
|--------|------|
| `coding-assistant` | 专业编程助手 |
| `security-expert` | 网络安全专家 |
| `data-analyst` | 数据分析专家 |

---

## 目录结构

```
openclaw-prompt-switcher/
├── switch.py                 # 提示词切换工具
├── agent_manager.py          # 智能体管理工具
├── prompts/                   # 提示词配置
│   ├── default.txt
│   ├── coding.txt
│   └── security.txt
├── agents/                    # 预设智能体
│   ├── coding-assistant/
│   │   ├── config.json
│   │   └── system_prompt.txt
│   ├── security-expert/
│   │   ├── config.json
│   │   └── system_prompt.txt
│   └── data-analyst/
│       ├── config.json
│       └── system_prompt.txt
└── README.md
```

---

## 多电脑同步

```bash
# 拉取最新配置
git pull

# 推送修改
git add .
git commit -m "更新配置"
git push
```

---

## 命令速查

### 提示词切换
| 操作 | 命令 |
|------|------|
| 列出 | `python3 switch.py --list` |
| 切换 | `python3 switch.py --switch <名称>` |
| 添加 | `python3 switch.py --add <名称>` |
| 编辑 | `python3 switch.py --edit <名称>` |
| 查看 | `python3 switch.py --show <名称>` |

### 智能体管理
| 操作 | 命令 |
|------|------|
| 列出预设 | `python3 agent_manager.py --list` |
| 查看详情 | `python3 agent_manager.py --show <名称>` |
| 创建 | `python3 agent_manager.py --create <名称>` |
| 新建预设 | `python3 agent_manager.py --new <名称>` |
| 编辑配置 | `python3 agent_manager.py --edit <名称>` |
| 编辑提示词 | `python3 agent_manager.py --edit-prompt <名称>` |
| 删除 | `python3 agent_manager.py --delete <名称>` |
