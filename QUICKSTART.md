# OpenClaw 快速接入指南

在任意电脑上，只需 3 步即可完成配置。

---

## 第一步：克隆项目

```bash
git clone https://github.com/Yhazrin/openclaw-prompt-switcher.git
cd openclaw-prompt-switcher
```

---

## 第二步：确保 OpenClaw 已安装

```bash
# 检查是否安装
openclaw --version

# 如未安装，根据你的系统安装：
# macOS
brew install openclaw

# 或使用 pip
pip install openclaw
```

---

## 第三步：切换提示词

```bash
# 查看可用提示词
python3 switch.py --list

# 切换到需要的提示词
python3 switch.py --switch coding
```

OpenClaw 会自动读取 `~/.openclaw/system_prompt.txt` 并应用新配置。

---

## 后续同步（多电脑使用）

在另一台电脑上：

```bash
# 克隆项目
git clone https://github.com/Yhazrin/openclaw-prompt-switcher.git
cd openclaw-prompt-switcher

# 拉取你最新的提示词修改
git pull
```

修改提示词后，同步到 GitHub：

```bash
# 1. 编辑提示词
python3 switch.py --edit my-prompt

# 2. 提交更改
git add .
git commit -m "更新提示词配置"
git push
```

---

## 命令速查

| 操作 | 命令 |
|------|------|
| 查看所有提示词 | `python3 switch.py --list` |
| 切换提示词 | `python3 switch.py --switch <名称>` |
| 添加新提示词 | `python3 switch.py --add <名称>` |
| 编辑提示词 | `python3 switch.py --edit <名称>` |
| 查看提示词内容 | `python3 switch.py --show <名称>` |
| 删除提示词 | `python3 switch.py --remove <名称>` |

---

## 自定义 OpenClaw 配置路径

如果你的 OpenClaw 配置路径不同，编辑 `switch.py` 中的这行：

```python
openclaw_config = Path.home() / ".openclaw" / "system_prompt.txt"
```

改为你的实际路径即可。
