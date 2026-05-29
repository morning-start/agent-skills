#!/usr/bin/env python3
"""
doc-orchestrator transform script
双轨格式转换：Agent 结构化 ↔ 人类可读 Markdown
"""

import re
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, Optional


def parse_frontmatter(content: str) -> tuple:
    """解析 YAML front matter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None, content
    frontmatter_str = match.group(1)
    body = match.group(2)
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError:
        return None, content
    return frontmatter, body


def to_agent_json(content: str) -> str:
    """将文档转换为 Agent 可读的 JSON 格式"""
    frontmatter, body = parse_frontmatter(content)
    
    result = {
        "metadata": frontmatter.get("doc", {}) if frontmatter else {},
        "content": body.strip()
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)


def to_agent_yaml(content: str) -> str:
    """将文档转换为 Agent 可读的 YAML 格式"""
    frontmatter, body = parse_frontmatter(content)
    
    result = {
        "metadata": frontmatter.get("doc", {}) if frontmatter else {},
        "content": body.strip()
    }
    
    return yaml.dump(result, allow_unicode=True, default_flow_style=False)


def add_frontmatter(content: str, metadata: Dict) -> str:
    """为纯 Markdown 添加 YAML front matter"""
    frontmatter = {"doc": metadata}
    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False)
    
    return f"---\n{fm_str}---\n\n{content}"


def extract_metadata(content: str) -> Optional[Dict]:
    """从文档中提取元数据"""
    frontmatter, _ = parse_frontmatter(content)
    if frontmatter and "doc" in frontmatter:
        return frontmatter["doc"]
    return None


def update_metadata(content: str, updates: Dict) -> str:
    """更新文档的元数据"""
    frontmatter, body = parse_frontmatter(content)
    
    if not frontmatter:
        return add_frontmatter(content, updates)
    
    if "doc" not in frontmatter:
        frontmatter["doc"] = {}
    
    frontmatter["doc"].update(updates)
    
    fm_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False)
    return f"---\n{fm_str}---\n\n{body}"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="文档双轨格式转换工具")
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-f", "--format", choices=["json", "yaml", "add-fm"],
                       default="json", help="输出格式")
    parser.add_argument("--metadata", help="JSON 格式的元数据（用于添加 front matter）")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 文件 {args.input} 不存在")
        sys.exit(1)
    
    content = input_path.read_text(encoding='utf-8')
    
    if args.format == "json":
        result = to_agent_json(content)
    elif args.format == "yaml":
        result = to_agent_yaml(content)
    elif args.format == "add-fm":
        if not args.metadata:
            print("错误: 添加 front matter 需要提供 --metadata 参数")
            sys.exit(1)
        metadata = json.loads(args.metadata)
        result = add_frontmatter(content, metadata)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(result, encoding='utf-8')
        print(f"输出到: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
