#!/usr/bin/env python3
"""
OpenClaw Prompt Switcher
快速切换 OpenClaw 提示词配置的工具
"""

import os
import json
import shutil
import argparse
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"
CONFIG_FILE = Path(__file__).parent / "current_prompt.txt"


def list_prompts():
    """列出所有可用的提示词配置"""
    prompts = [f.stem for f in PROMPTS_DIR.glob("*.txt")]
    print("\n📋 可用的提示词配置：")
    print("-" * 30)
    for i, p in enumerate(prompts, 1):
        current = " [当前]" if is_current(p) else ""
        print(f"  {i}. {p}{current}")
    print()

    current = get_current_prompt()
    if current:
        print(f"✅ 当前使用: {current}")

    return prompts


def is_current(prompt_name: str) -> bool:
    """检查是否为当前使用的提示词"""
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip() == prompt_name
    return False


def get_current_prompt() -> str | None:
    """获取当前提示词名称"""
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()
    return None


def switch_to(prompt_name: str):
    """切换到指定的提示词"""
    prompt_file = PROMPTS_DIR / f"{prompt_name}.txt"

    if not prompt_file.exists():
        print(f"❌ 错误: 找不到提示词配置 '{prompt_name}'")
        print("   使用 --list 查看可用配置")
        return False

    # 读取提示词内容
    content = prompt_file.read_text()

    # 保存当前使用的提示词名称
    CONFIG_FILE.write_text(prompt_name)

    # 如果有 OpenClaw 的配置路径，复制过去
    openclaw_config = Path.home() / ".openclaw" / "system_prompt.txt"
    if openclaw_config.parent.exists():
        openclaw_config.write_text(content)
        print(f"✅ 已切换到: {prompt_name}")
        print(f"   配置已更新: {openclaw_config}")
    else:
        print(f"✅ 已切换到: {prompt_name}")
        print(f"   内容已保存到: {CONFIG_FILE}")
        print(f"   请手动复制到 OpenClaw 配置目录")

    return True


def add_prompt(name: str, content: str = ""):
    """添加新的提示词配置"""
    prompt_file = PROMPTS_DIR / f"{name}.txt"

    if prompt_file.exists():
        print(f"❌ 错误: 提示词 '{name}' 已存在")
        return False

    if content:
        prompt_file.write_text(content)
    else:
        prompt_file.write_text("# 在这里编写你的提示词...\n")

    print(f"✅ 已创建: {name}")
    print(f"   路径: {prompt_file}")
    return True


def remove_prompt(name: str):
    """删除提示词配置"""
    prompt_file = PROMPTS_DIR / f"{name}.txt"

    if not prompt_file.exists():
        print(f"❌ 错误: 找不到提示词 '{name}'")
        return False

    if is_current(name):
        CONFIG_FILE.unlink(missing_ok=True)

    prompt_file.unlink()
    print(f"✅ 已删除: {name}")
    return True


def edit_prompt(name: str):
    """编辑提示词配置"""
    prompt_file = PROMPTS_DIR / f"{name}.txt"

    if not prompt_file.exists():
        print(f"❌ 错误: 找不到提示词 '{name}'")
        return False

    # 尝试使用默认编辑器
    editor = os.environ.get("EDITOR", "vi")
    os.system(f'{editor} "{prompt_file}"')
    return True


def show_prompt(name: str):
    """显示提示词内容"""
    prompt_file = PROMPTS_DIR / f"{name}.txt"

    if not prompt_file.exists():
        print(f"❌ 错误: 找不到提示词 '{name}'")
        return False

    print(f"\n📝 {name}:")
    print("-" * 40)
    print(prompt_file.read_text())
    print("-" * 40)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 提示词快速切换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list              查看所有提示词
  %(prog)s --switch coding     切换到 coding 提示词
  %(prog)s --add my-prompt      添加新提示词
  %(prog)s --show coding       查看提示词内容
  %(prog)s --edit coding       编辑提示词
  %(prog)s --remove old-prompt 删除提示词
        """
    )

    parser.add_argument("--list", "-l", action="store_true",
                        help="列出所有提示词配置")
    parser.add_argument("--switch", "-s", metavar="NAME",
                        help="切换到指定提示词")
    parser.add_argument("--add", "-a", metavar="NAME",
                        help="添加新的提示词配置")
    parser.add_argument("--remove", "-r", metavar="NAME",
                        help="删除提示词配置")
    parser.add_argument("--show", metavar="NAME",
                        help="查看提示词内容")
    parser.add_argument("--edit", "-e", metavar="NAME",
                        help="编辑提示词配置")

    args = parser.parse_args()

    # 确保 promts 目录存在
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.list:
        list_prompts()
    elif args.switch:
        switch_to(args.switch)
    elif args.add:
        add_prompt(args.add)
    elif args.remove:
        remove_prompt(args.remove)
    elif args.show:
        show_prompt(args.show)
    elif args.edit:
        edit_prompt(args.edit)
    else:
        # 默认显示列表
        list_prompts()


if __name__ == "__main__":
    main()
