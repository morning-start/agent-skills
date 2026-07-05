#!/usr/bin/env python3
"""
doc-orchestrator validate script
验证文档的 YAML front matter 格式和基本结构
"""

import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


REQUIRED_FIELDS = ["id", "type", "version", "status", "created"]
VALID_STATUSES = ["draft", "review", "approved", "deprecated", "template"]


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content
    frontmatter_str = match.group(1)
    body = match.group(2)
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError:
        return {}, content
    return frontmatter, body


def validate_frontmatter(frontmatter: Dict) -> List[str]:
    issues = []
    if "doc" not in frontmatter:
        issues.append("缺少 'doc' 键")
        return issues
    
    doc = frontmatter["doc"]
    
    for field in REQUIRED_FIELDS:
        if field not in doc:
            issues.append(f"缺少必填字段: {field}")
    
    if "status" in doc and doc["status"] not in VALID_STATUSES:
        issues.append(f"status 值无效: {doc['status']}，应为 {VALID_STATUSES}")
    
    if "version" in doc:
        version_pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(version_pattern, doc["version"]):
            issues.append(f"版本号格式无效: {doc['version']}，应为 MAJOR.MINOR.PATCH")
    
    if "id" in doc:
        id_pattern = r'^[A-Z]+-\d+$'
        if not re.match(id_pattern, doc["id"]):
            issues.append(f"文档 ID 格式无效: {doc['id']}，应为 PREFIX-NNN")
    
    return issues


def validate_body(body: str) -> List[str]:
    issues = []
    lines = body.split('\n')
    
    has_h1 = False
    for line in lines:
        if line.startswith('# '):
            if has_h1:
                issues.append("文档包含多个一级标题")
                break
            has_h1 = True
    
    if not has_h1:
        issues.append("文档缺少一级标题")
    
    return issues


def validate_file(filepath: str) -> Dict:
    path = Path(filepath)
    if not path.exists():
        return {"file": filepath, "valid": False, "issues": ["文件不存在"]}
    
    content = path.read_text(encoding='utf-8')
    frontmatter, body = parse_frontmatter(content)
    
    issues = []
    if not frontmatter:
        issues.append("未找到有效的 YAML front matter")
    else:
        issues.extend(validate_frontmatter(frontmatter))
    
    issues.extend(validate_body(body))
    
    return {
        "file": filepath,
        "valid": len(issues) == 0,
        "issues": issues
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python validate.py <file1> [file2] ...")
        sys.exit(1)
    
    results = []
    for filepath in sys.argv[1:]:
        result = validate_file(filepath)
        results.append(result)
        status = "✅ 通过" if result["valid"] else "❌ 失败"
        print(f"{status}: {result['file']}")
        for issue in result["issues"]:
            print(f"  - {issue}")
    
    failed = [r for r in results if not r["valid"]]
    if failed:
        print(f"\n共 {len(failed)}/{len(results)} 个文件验证失败")
        sys.exit(1)
    else:
        print(f"\n全部 {len(results)} 个文件验证通过")


if __name__ == "__main__":
    main()
