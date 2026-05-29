#!/usr/bin/env python3
"""
模板变量统一工具

功能：
1. 扫描所有模板文件
2. 识别现有变量格式（{var}, {{var}}, {{var_name}} 等）
3. 统一替换为 {{variable_name}} 格式
4. 生成变量映射报告
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def find_template_files(templates_dir: Path) -> List[Path]:
    """查找所有模板文件"""
    template_files = []
    for subdir in templates_dir.iterdir():
        if subdir.is_dir() and subdir.name not in ['__pycache__']:
            for file in subdir.glob('*.md'):
                if file.name != 'README.md':  # 跳过索引文件
                    template_files.append(file)
    return template_files


def identify_variable_patterns(content: str) -> Dict[str, List[str]]:
    """识别不同的变量格式"""
    patterns = {
        'single_brace': r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}',  # {var}
        'double_brace_simple': r'\{\{([a-zA-Z][a-zA-Z0-9]*)\}\}',  # {{var}}
        'double_brace_underscore': r'\{\{([a-zA-Z][a-zA-Z0-9_]*(?:_[a-zA-Z0-9_]+)*)\}\}',  # {{var_name}}
        'curly_with_underscore': r'\{([a-zA-Z][a-zA-Z0-9_]*(?:_[a-zA-Z0-9_]+)*)\}',  # {var_name}
    }
    
    found_vars = {}
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, content)
        if matches:
            found_vars[pattern_name] = list(set(matches))
    
    return found_vars


def normalize_variable_name(name: str) -> str:
    """标准化变量名为下划线格式"""
    # 如果已经包含下划线，直接返回
    if '_' in name:
        return name
    
    # 驼峰转下划线
    result = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    return result.lower()


def replace_variables(content: str) -> Tuple[str, Dict[str, str]]:
    """替换所有变量格式为统一格式"""
    replacements = {}
    
    # 替换单花括号 {var} -> {{var}}
    def replace_single(match):
        var_name = match.group(1)
        normalized = normalize_variable_name(var_name)
        replacements[f'{{{var_name}}}'] = f'{{{{{normalized}}}}}'
        return f'{{{{{normalized}}}}}'
    
    content = re.sub(r'\{([a-zA-Z_][a-zA-Z0-9_]*(?:_[a-zA-Z0-9_]+)*)\}', replace_single, content)
    
    # 替换双花括号但格式不统一的 {{var}} -> {{var_name}}
    def replace_double(match):
        var_name = match.group(1)
        normalized = normalize_variable_name(var_name)
        replacements[f'{{{{{var_name}}}}}'] = f'{{{{{normalized}}}}}'
        return f'{{{{{normalized}}}}}'
    
    content = re.sub(r'\{\{([a-zA-Z][a-zA-Z0-9]*(?:_[a-zA-Z0-9_]+)*)\}\}', replace_double, content)
    
    return content, replacements


def process_template_file(file_path: Path, dry_run: bool = True) -> Dict:
    """处理单个模板文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 识别现有变量格式
    found_vars = identify_variable_patterns(content)
    
    # 替换变量
    new_content, replacements = replace_variables(content)
    
    result = {
        'file': str(file_path),
        'found_variables': found_vars,
        'replacements': replacements,
        'changed': len(replacements) > 0,
    }
    
    if not dry_run and result['changed']:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return result


def generate_report(results: List[Dict], output_file: Path, base_dir: Path):
    """生成变量映射报告"""
    report = []
    report.append("# 模板变量统一报告\n")
    report.append(f"处理文件数：{len(results)}\n")
    report.append(f"发生变更：{sum(1 for r in results if r['changed'])}\n\n")
    
    for result in results:
        if result['changed']:
            try:
                rel_path = Path(result['file']).relative_to(base_dir)
                report.append(f"## {rel_path}\n")
            except ValueError:
                report.append(f"## {result['file']}\n")
            report.append("| 原格式 | 新格式 |\n")
            report.append("|--------|--------|\n")
            for old, new in result['replacements'].items():
                report.append(f"| `{old}` | `{new}` |\n")
            report.append("\n")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(report))


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='模板变量统一工具')
    parser.add_argument('--templates-dir', type=str, default='templates',
                        help='模板目录路径')
    parser.add_argument('--dry-run', action='store_true',
                        help='仅预览不实际修改')
    parser.add_argument('--output-report', type=str, default='variable_report.md',
                        help='输出报告文件路径')
    
    args = parser.parse_args()
    
    templates_dir = Path(args.templates_dir)
    if not templates_dir.exists():
        print(f"错误：模板目录不存在：{templates_dir}")
        return 1
    
    # 查找所有模板文件
    template_files = find_template_files(templates_dir)
    print(f"找到 {len(template_files)} 个模板文件")
    
    # 处理每个文件
    results = []
    for file_path in template_files:
        print(f"处理：{file_path}")
        result = process_template_file(file_path, dry_run=args.dry_run)
        results.append(result)
        
        if result['changed']:
            print(f"  ✓ 替换了 {len(result['replacements'])} 个变量")
        else:
            print(f"  - 无需变更")
    
    # 生成报告
    generate_report(results, Path(args.output_report), templates_dir)
    print(f"\n报告已生成：{args.output_report}")
    
    # 统计
    total_replacements = sum(len(r['replacements']) for r in results)
    print(f"\n总计：{total_replacements} 个变量被替换")
    
    return 0


if __name__ == '__main__':
    exit(main())
