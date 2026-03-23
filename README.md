# OpenClaw Prompt Switcher

快速切换 OpenClaw 提示词配置的工具。

## 功能

- 📋 列出所有提示词配置
- 🔄 快速切换提示词
- ➕ 添加新提示词
- ✏️ 编辑提示词
- 🗑️ 删除提示词

## 使用方法

### 列出所有提示词
```bash
python switch.py --list
```

### 切换提示词
```bash
python switch.py --switch coding
```

### 添加新提示词
```bash
python switch.py --add my-prompt
```

### 查看提示词内容
```bash
python switch.py --show coding
```

### 编辑提示词
```bash
python switch.py --edit coding
```

### 删除提示词
```bash
python switch.py --remove old-prompt
```

## 目录结构

```
openclaw-prompt-switcher/
├── switch.py           # 主脚本
├── prompts/            # 提示词配置目录
│   ├── default.txt     # 默认提示词
│   ├── coding.txt      # 编程助手
│   └── security.txt    # 安全分析
├── current_prompt.txt  # 当前使用的提示词
└── README.md
```

## 配置

提示词文件存放在 `prompts/` 目录，每个提示词是一个独立的 `.txt` 文件。

修改提示词内容后，使用 `--switch` 命令应用更改。
