#!/usr/bin/env python3
"""
OpenClaw Agent Manager
快速创建和管理 OpenClaw 智能体
"""

import os
import json
import shutil
import subprocess
import argparse
from pathlib import Path

AGENTS_DIR = Path(__file__).parent / "agents"
OPENCLAW_AGENTS_DIR = Path.home() / ".openclaw" / "agents"


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    """执行命令并返回 (returncode, stdout, stderr)"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def list_local_agents():
    """列出本地预设的智能体"""
    if not AGENTS_DIR.exists():
        return []

    agents = []
    for agent_dir in AGENTS_DIR.iterdir():
        if agent_dir.is_dir():
            config_file = agent_dir / "config.json"
            if config_file.exists():
                config = json.loads(config_file.read_text())
                config["_path"] = agent_dir.name
                agents.append(config)
            else:
                agents.append({
                    "name": agent_dir.name,
                    "description": "(无配置)",
                    "_path": agent_dir.name
                })
    return agents


def list_openclaw_agents():
    """列出 OpenClaw 中已创建的智能体"""
    code, stdout, stderr = run_command(["openclaw", "agents", "list", "--json"])
    if code == 0:
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            pass
    return []


def show_agent(agent_name: str):
    """显示智能体详细信息"""
    local_agents = list_local_agents()
    agent = next((a for a in local_agents if a["name"] == agent_name), None)

    if not agent:
        print(f"❌ 找不到本地智能体: {agent_name}")
        return False

    print(f"\n🤖 智能体: {agent['name']}")
    print("-" * 40)

    for key in ["description", "model", "temperature", "max_tokens"]:
        if key in agent:
            print(f"  {key}: {agent[key]}")

    system_prompt_file = AGENTS_DIR / agent_name / "system_prompt.txt"
    if system_prompt_file.exists():
        print(f"\n📝 System Prompt:")
        print("-" * 40)
        print(system_prompt_file.read_text())

    return True


def create_agent(agent_name: str, non_interactive: bool = False):
    """从预设创建 OpenClaw 智能体"""
    agent_path = AGENTS_DIR / agent_name
    config_file = agent_path / "config.json"

    if not agent_path.exists():
        print(f"❌ 找不到预设智能体: {agent_name}")
        print("\n📋 可用的预设智能体:")
        for a in list_local_agents():
            print(f"  - {a['name']}: {a.get('description', '')}")
        return False

    config = json.loads(config_file.read_text())

    # 构建 openclaw agents add 命令
    cmd = ["openclaw", "agents", "add", agent_name, "--non-interactive"]

    if "model" in config:
        cmd.extend(["--model", config["model"]])

    # 创建 workspace 目录
    workspace_dir = OPENCLAW_AGENTS_DIR / agent_name / "workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    cmd.extend(["--workspace", str(workspace_dir)])

    # 复制 system_prompt 到 workspace
    system_prompt_src = agent_path / "system_prompt.txt"
    system_prompt_dst = workspace_dir / "system_prompt.txt"
    if system_prompt_src.exists():
        shutil.copy(system_prompt_src, system_prompt_dst)

    # 执行创建命令
    print(f"🔄 正在创建智能体: {agent_name}")
    code, stdout, stderr = run_command(cmd)

    if code == 0:
        print(f"✅ 智能体创建成功: {agent_name}")
        if stdout:
            print(stdout)
        return True
    else:
        print(f"❌ 创建失败:")
        print(stderr)
        return False


def delete_agent(agent_name: str):
    """删除 OpenClaw 智能体"""
    cmd = ["openclaw", "agents", "delete", agent_name, "--non-interactive"]
    code, stdout, stderr = run_command(cmd)

    if code == 0:
        print(f"✅ 智能体已删除: {agent_name}")
        return True
    else:
        print(f"❌ 删除失败:")
        print(stderr)
        return False


def add_binding(agent_name: str, channel: str):
    """为智能体添加绑定"""
    cmd = ["openclaw", "agents", "bind", agent_name, "--bind", channel]
    code, stdout, stderr = run_command(cmd)

    if code == 0:
        print(f"✅ 绑定成功: {agent_name} -> {channel}")
        return True
    else:
        print(f"❌ 绑定失败:")
        print(stderr)
        return False


def new_agent(name: str, description: str = "", model: str = "claude-3-sonnet"):
    """创建新的预设智能体"""
    agent_path = AGENTS_DIR / name

    if agent_path.exists():
        print(f"❌ 智能体已存在: {name}")
        return False

    agent_path.mkdir(parents=True)
    config = {
        "name": name,
        "description": description or f"自定义智能体: {name}",
        "model": model,
        "temperature": 0.7,
        "max_tokens": 4096,
        "system_prompt_file": "system_prompt.txt"
    }

    with open(agent_path / "config.json", "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    with open(agent_path / "system_prompt.txt", "w") as f:
        f.write(f"# {name}\n\n{description or '自定义智能体'}\n\n## 角色\n\n\n\n## 能力\n\n\n\n## 约束\n\n\n")

    print(f"✅ 已创建预设智能体: {name}")
    print(f"   路径: {agent_path}")
    print(f"   使用 --edit {name} 编辑提示词")
    return True


def edit_agent(name: str):
    """编辑智能体配置"""
    agent_path = AGENTS_DIR / name
    config_file = agent_path / "config.json"

    if not config_file.exists():
        print(f"❌ 找不到智能体: {name}")
        return False

    editor = os.environ.get("EDITOR", "vi")
    os.system(f'{editor} "{config_file}"')
    return True


def edit_system_prompt(name: str):
    """编辑智能体的 system prompt"""
    agent_path = AGENTS_DIR / name
    prompt_file = agent_path / "system_prompt.txt"

    if not prompt_file.exists():
        print(f"❌ 找不到智能体: {name}")
        return False

    editor = os.environ.get("EDITOR", "vi")
    os.system(f'{editor} "{prompt_file}"')
    return True


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Agent Manager - 智能体快速创建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list              列出所有预设智能体
  %(prog)s --show coding-assistant   查看智能体详情
  %(prog)s --create coding-assistant 创建到 OpenClaw
  %(prog)s --delete coding-assistant 删除 OpenClaw 中的智能体
  %(prog)s --new my-agent       创建新的预设智能体
  %(prog)s --edit coding-assistant   编辑智能体配置
        """
    )

    parser.add_argument("--list", "-l", action="store_true",
                        help="列出所有预设智能体")
    parser.add_argument("--show", metavar="NAME",
                        help="查看智能体详情")
    parser.add_argument("--create", metavar="NAME",
                        help="从预设创建 OpenClaw 智能体")
    parser.add_argument("--delete", metavar="NAME",
                        help="删除 OpenClaw 中的智能体")
    parser.add_argument("--new", metavar="NAME",
                        help="创建新的预设智能体")
    parser.add_argument("--edit", metavar="NAME",
                        help="编辑智能体配置文件")
    parser.add_argument("--edit-prompt", metavar="NAME",
                        help="编辑智能体的 system prompt")
    parser.add_argument("--bind", nargs=2, metavar=("NAME", "CHANNEL"),
                        help="绑定智能体到频道")
    parser.add_argument("--description", metavar="DESC",
                        default="自定义智能体",
                        help="新建智能体的描述")
    parser.add_argument("--model", metavar="MODEL",
                        default="claude-3-sonnet",
                        help="新建智能体使用的模型")

    args = parser.parse_args()

    AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.list:
        print("\n📦 预设智能体:")
        print("-" * 50)
        for agent in list_local_agents():
            print(f"  🤖 {agent['name']}")
            print(f"     {agent.get('description', '无描述')}")
            if "model" in agent:
                print(f"     模型: {agent['model']}")
            print()

        print("\n🦞 OpenClaw 已创建的智能体:")
        print("-" * 50)
        for agent in list_openclaw_agents():
            print(f"  🤖 {agent.get('name', 'unknown')}")

    elif args.show:
        show_agent(args.show)
    elif args.create:
        create_agent(args.create)
    elif args.delete:
        delete_agent(args.delete)
    elif args.new:
        new_agent(args.new, args.description, args.model)
    elif args.edit:
        edit_agent(args.edit)
    elif args.edit_prompt:
        edit_system_prompt(args.edit_prompt)
    elif args.bind:
        add_binding(args.bind[0], args.bind[1])
    else:
        # 默认列出
        list_local_agents()


if __name__ == "__main__":
    main()
