#!/usr/bin/env python3
"""
doc-orchestrator export script
支持文档多格式导出（Markdown/PDF/HTML/ZIP）
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
from typing import List, Optional


def export_markdown(source_dir: str, output_dir: str) -> str:
    """导出为 Markdown（保持原始结构）"""
    src = Path(source_dir)
    dst = Path(output_dir)
    
    if dst.exists():
        shutil.rmtree(dst)
    
    shutil.copytree(src, dst)
    return output_dir


def export_zip(source_dir: str, output_file: str) -> str:
    """导出为 ZIP 压缩包"""
    src = Path(source_dir)
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in src.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(src)
                zf.write(file_path, arcname)
    
    return output_file


def export_html(source_dir: str, output_dir: str, title: str = "Documentation") -> str:
    """导出为 HTML（带侧边栏导航）"""
    src = Path(source_dir)
    dst = Path(output_dir)
    dst.mkdir(parents=True, exist_ok=True)
    
    # 收集所有 markdown 文件
    md_files = list(src.rglob('*.md'))
    
    # 生成侧边栏
    sidebar_items = []
    for f in sorted(md_files):
        rel_path = f.relative_to(src)
        sidebar_items.append(f'<li><a href="{rel_path}.html">{rel_path}</a></li>')
    
    sidebar = f'<ul>\n{"  ".join(sidebar_items)}\n</ul>'
    
    # 生成每个 HTML 文件
    for md_file in md_files:
        content = md_file.read_text(encoding='utf-8')
        
        # 简单的 Markdown 到 HTML 转换
        html_content = convert_markdown_to_html(content)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {md_file.name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; display: flex; }}
        .sidebar {{ width: 250px; height: 100vh; background: #f5f5f5; padding: 20px; position: fixed; overflow-y: auto; }}
        .content {{ margin-left: 250px; padding: 40px; max-width: 800px; }}
        h1 {{ margin-bottom: 20px; }}
        h2 {{ margin: 30px 0 15px; }}
        p {{ margin: 10px 0; line-height: 1.6; }}
        table {{ border-collapse: collapse; margin: 20px 0; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 16px; overflow-x: auto; border-radius: 5px; }}
    </style>
</head>
<body>
    <nav class="sidebar">{sidebar}</nav>
    <main class="content">{html_content}</main>
</body>
</html>"""
        
        output_file = dst / f"{md_file.stem}.html"
        output_file.write_text(html, encoding='utf-8')
    
    return output_dir


def convert_markdown_to_html(content: str) -> str:
    """简单的 Markdown 到 HTML 转换"""
    lines = content.split('\n')
    html_lines = []
    in_code_block = False
    
    for line in lines:
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</pre>')
                in_code_block = False
            else:
                html_lines.append('<pre><code>')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line)
            continue
        
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('- '):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('|'):
            # 简化处理表格
            html_lines.append(line)
        elif line.strip():
            html_lines.append(f'<p>{line}</p>')
    
    return '\n'.join(html_lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="文档导出工具")
    parser.add_argument("input", help="文档目录路径")
    parser.add_argument("-o", "--output", help="输出路径")
    parser.add_argument("-f", "--format", choices=["md", "html", "zip"],
                       default="zip", help="导出格式")
    parser.add_argument("-t", "--title", default="Documentation", help="文档标题")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 目录 {args.input} 不存在")
        sys.exit(1)
    
    if not args.output:
        args.output = str(input_path.parent / f"{input_path.name}-exported")
    
    if args.format == "md":
        result = export_markdown(args.input, args.output)
    elif args.format == "zip":
        if not args.output.endswith('.zip'):
            args.output += '.zip'
        result = export_zip(args.input, args.output)
    elif args.format == "html":
        result = export_html(args.input, args.output, args.title)
    
    print(f"导出完成: {result}")


if __name__ == "__main__":
    main()
