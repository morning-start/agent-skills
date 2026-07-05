#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
源代码提取与格式化工具
用于软件著作权申请材料的准备

功能：
1. 自动判断总行数，决定提取策略（全量 or 前后各30页）
2. 强制每页补足50行（如用注释填充空白页）
3. 输出页码标记（如 /* === 第1页 === */）
"""

import os
import argparse
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 支持的代码文件扩展名
CODE_EXTENSIONS = {
    '.py', '.java', '.c', '.cpp', '.h', '.js', '.ts', '.jsx', '.tsx',
    '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.cs',
    '.m', '.mm', '.dart', '.lua', '.sql', '.sh', '.bat', '.ps1'
}

# 忽略的目录
IGNORE_DIRS = {
    '__pycache__', 'node_modules', '.git', '.venv', 'venv', 'env',
    'dist', 'build', 'target', '.idea', '.vscode', 'vendor', 'third_party',
    'logs', 'tmp', 'temp', 'cache', '.cache'
}

# 忽略的文件
IGNORE_FILES = {
    '.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes',
    'package-lock.json', 'yarn.lock', 'poetry.lock', 'requirements.lock'
}

# 软著申请官方要求
MIN_TOTAL_LINES = 3000  # 总行数≥3000行才需提交60页
PAGES_PER_SECTION = 30  # 每个部分的页数
LINES_PER_PAGE = 50  # 每页行数（含空行和注释）


def find_code_files(code_dir: Path) -> List[Path]:
    """查找所有代码文件"""
    code_files = []
    
    logger.info(f"正在扫描代码目录: {code_dir}")
    
    for root, dirs, files in os.walk(code_dir):
        # 过滤忽略的目录
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            # 检查扩展名
            if file_path.suffix.lower() in CODE_EXTENSIONS:
                # 检查是否在忽略列表中
                if file not in IGNORE_FILES:
                    code_files.append(file_path)
    
    logger.info(f"找到 {len(code_files)} 个代码文件")
    return code_files


def count_lines_in_code(files: List[Path]) -> int:
    """统计代码总行数"""
    total_lines = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                total_lines += sum(1 for _ in f)
        except Exception as e:
            logger.warning(f"读取文件失败 {file_path}: {e}")
            continue
    
    return total_lines


def extract_main_code(files: List[Path]) -> Optional[Path]:
    """查找主入口文件（main函数）"""
    main_files = []
    
    logger.info("正在查找主入口文件...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 查找主函数定义
                if any(keyword in content for keyword in [
                    'def main(', 'public static void main',
                    'int main(', 'func main(', 'package main',
                    '@SpringBootApplication'
                ]):
                    main_files.append((file_path, count_lines_in_code([file_path])))
        except Exception as e:
            logger.warning(f"分析文件失败 {file_path}: {e}")
            continue
    
    if main_files:
        # 选择最大的主函数文件
        main_file = max(main_files, key=lambda x: x[1])[0]
        logger.info(f"找到主入口文件: {main_file}")
        return main_file
    
    logger.warning("未找到明确的主入口文件，将按文件行数排序")
    return None


def determine_extraction_strategy(total_lines: int) -> Tuple[str, int]:
    """
    根据总行数决定提取策略
    
    Args:
        total_lines: 代码总行数
    
    Returns:
        (策略类型, 需要提取的行数)
        策略类型: 'full' (全量) 或 'sections' (前后各30页)
    """
    if total_lines < MIN_TOTAL_LINES:
        logger.info(f"代码总行数 ({total_lines}) < {MIN_TOTAL_LINES}，采用全量提交策略")
        return 'full', total_lines
    
    required_lines = PAGES_PER_SECTION * LINES_PER_PAGE * 2  # 前30页 + 后30页
    logger.info(f"代码总行数 ({total_lines}) >= {MIN_TOTAL_LINES}，采用前后各30页策略")
    return 'sections', required_lines


def pad_page_to_lines(lines: List[str], target_lines: int, file_path: Path) -> List[str]:
    """
    补足页面到目标行数（用注释填充）
    
    Args:
        lines: 当前页的行列表
        target_lines: 目标行数
        file_path: 当前文件路径
    
    Returns:
        补足后的行列表
    """
    if len(lines) >= target_lines:
        return lines[:target_lines]
    
    # 用注释补足
    padding_lines = target_lines - len(lines)
    
    # 根据文件扩展名选择注释风格
    suffix = file_path.suffix.lower()
    comment_prefix = "//"
    
    if suffix in {'.py', '.sh', '.pl', '.rb', '.lua'}:
        comment_prefix = "#"
    elif suffix in {'.sql', '.pl'}:
        comment_prefix = "--"
    elif suffix in {'.html', '.xml', '.htm'}:
        comment_prefix = "<!--"
        comment_suffix = "-->"
    elif suffix in {'.bat', '.cmd'}:
        comment_prefix = "REM"
    
    # 构造填充注释
    padding = []
    if comment_prefix == "<!--":
        for i in range(padding_lines):
            padding.append(f"{comment_prefix} 此处为填充行，以满足每页不少于50行的要求 {comment_suffix}")
    else:
        for i in range(padding_lines):
            padding.append(f"{comment_prefix} 此处为填充行，以满足每页不少于50行的要求")
    
    lines.extend(padding)
    logger.info(f"已补足 {padding_lines} 行填充注释")
    return lines


def format_page(lines: List[str], page_num: int, section: str, file_path: Optional[Path] = None) -> str:
    """
    格式化单页代码
    
    Args:
        lines: 代码行列表
        page_num: 页码
        section: 章节（'前部' 或 '后部'）
        file_path: 当前文件路径（可选）
    
    Returns:
        格式化后的页面字符串
    """
    formatted = []
    
    # 添加页眉
    if file_path:
        formatted.append(f"/* === 第{page_num}页 ({section}) === */")
        formatted.append(f"/* 文件: {file_path} */")
    else:
        formatted.append(f"/* === 第{page_num}页 ({section}) === */")
    formatted.append("/*")
    
    # 添加代码行
    for idx, line in enumerate(lines, 1):
        formatted.append(line)
    
    return '\n'.join(formatted)


def extract_code_pages(files: List[Path], total_lines: int, strategy: str) -> str:
    """
    提取代码页
    
    Args:
        files: 代码文件列表
        total_lines: 代码总行数
        strategy: 提取策略（'full' 或 'sections'）
    
    Returns:
        格式化后的代码文本
    """
    result = []
    
    # 收集所有代码行
    all_code_lines = []
    current_file = None
    file_start_line = 1
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                # 去除行尾换行符
                lines = [line.rstrip('\n\r') for line in lines]
                
                # 记录文件信息
                for i, line in enumerate(lines, 1):
                    all_code_lines.append({
                        'file_path': file_path,
                        'line_num': i,
                        'content': line
                    })
        except Exception as e:
            logger.warning(f"读取文件失败 {file_path}: {e}")
            continue
    
    if not all_code_lines:
        logger.error("未找到任何有效的代码文件")
        raise ValueError("未找到任何有效的代码文件")
    
    # 添加头部信息
    result.append("=" * 80)
    result.append("软件著作权申请 - 源代码文档")
    if strategy == 'full':
        result.append(f"提取策略: 全量提交 (代码总行数 {total_lines} < {MIN_TOTAL_LINES})")
        result.append(f"总页数: {(total_lines + LINES_PER_PAGE - 1) // LINES_PER_PAGE} 页")
    else:
        result.append(f"提取策略: 前{PAGES_PER_SECTION}页 + 后{PAGES_PER_SECTION}页")
        result.append(f"总页数: {PAGES_PER_SECTION * 2} 页")
    result.append(f"每页行数: {LINES_PER_PAGE} 行 (含空行和注释)")
    result.append("=" * 80)
    result.append("")
    
    # 根据策略提取代码
    if strategy == 'full':
        # 全量提交
        extract_full_code(result, all_code_lines, total_lines)
    else:
        # 前后各30页
        extract_sections_code(result, all_code_lines)
    
    # 添加页脚信息
    result.append("")
    result.append("=" * 80)
    if strategy == 'full':
        total_pages = (total_lines + LINES_PER_PAGE - 1) // LINES_PER_PAGE
        result.append(f"源代码文档结束 - 共 {total_pages} 页 (全量提交)")
    else:
        result.append(f"源代码文档结束 - 共 {PAGES_PER_SECTION * 2} 页 (前后各{PAGES_PER_SECTION}页)")
    result.append("=" * 80)
    
    return '\n'.join(result)


def extract_full_code(result: List[str], all_code_lines: List[Dict], total_lines: int) -> None:
    """全量提取代码"""
    logger.info(f"正在提取全量代码 (共{total_lines}行)")
    
    current_page = 1
    page_lines = []
    current_file_path = None
    
    for idx, line_info in enumerate(all_code_lines, 1):
        # 文件切换时处理
        if current_file_path != line_info['file_path']:
            if page_lines:
                # 补足当前页并输出
                page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
                page_content = format_page(page_lines, current_page, "全量", current_file_path)
                result.append(page_content)
                result.append("")
                current_page += 1
                page_lines = []
            current_file_path = line_info['file_path']
            page_lines.append(f"/* 文件: {line_info['file_path']} */")
            page_lines.append(f"/* 从第 {line_info['line_num']} 行开始 */")
            page_lines.append("/*")
        
        page_lines.append(f"{line_info['line_num']:4d}: {line_info['content']}")
        
        # 达到每页行数，分页
        if len(page_lines) >= LINES_PER_PAGE:
            page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
            page_content = format_page(page_lines, current_page, "全量", current_file_path)
            result.append(page_content)
            result.append("")
            current_page += 1
            page_lines = []
    
    # 输出最后一页
    if page_lines:
        page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
        page_content = format_page(page_lines, current_page, "全量", current_file_path)
        result.append(page_content)
        result.append("")
    
    total_pages = (total_lines + LINES_PER_PAGE - 1) // LINES_PER_PAGE
    logger.info(f"全量提取完成，共 {current_page} 页")


def extract_sections_code(result: List[str], all_code_lines: List[Dict]) -> None:
    """提取前后各30页"""
    logger.info(f"正在提取前后各{PAGES_PER_SECTION}页")
    
    # 计算需要提取的行数
    front_lines_count = PAGES_PER_SECTION * LINES_PER_PAGE
    back_lines_count = PAGES_PER_SECTION * LINES_PER_PAGE
    
    # 提取前N页
    logger.info(f"正在提取前{PAGES_PER_SECTION}页...")
    current_page = 1
    page_lines = []
    current_file_path = None
    
    for idx, line_info in enumerate(all_code_lines[:front_lines_count], 1):
        # 文件切换时处理
        if current_file_path != line_info['file_path']:
            if page_lines:
                page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
                page_content = format_page(page_lines, current_page, "前部", current_file_path)
                result.append(page_content)
                result.append("")
                current_page += 1
                page_lines = []
            current_file_path = line_info['file_path']
            page_lines.append(f"/* 文件: {line_info['file_path']} */")
            page_lines.append(f"/* 从第 {line_info['line_num']} 行开始 */")
            page_lines.append("/*")
        
        page_lines.append(f"{line_info['line_num']:4d}: {line_info['content']}")
        
        # 达到每页行数，分页
        if len(page_lines) >= LINES_PER_PAGE:
            page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
            page_content = format_page(page_lines, current_page, "前部", current_file_path)
            result.append(page_content)
            result.append("")
            current_page += 1
            page_lines = []
    
    # 输出前部最后一页
    if page_lines:
        page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
        page_content = format_page(page_lines, current_page, "前部", current_file_path)
        result.append(page_content)
        result.append("")
    
    # 添加分隔符
    result.append("")
    result.append("=" * 80)
    result.append(f"以上为源代码前部（前{PAGES_PER_SECTION}页），以下为源代码后部（后{PAGES_PER_SECTION}页）")
    result.append("=" * 80)
    result.append("")
    
    # 提取后N页
    logger.info(f"正在提取后{PAGES_PER_SECTION}页...")
    current_file_path = None
    page_lines = []
    
    for idx, line_info in enumerate(all_code_lines[-back_lines_count:], 1):
        # 文件切换时处理
        if current_file_path != line_info['file_path']:
            if page_lines:
                page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
                page_content = format_page(page_lines, current_page, "后部", current_file_path)
                result.append(page_content)
                result.append("")
                current_page += 1
                page_lines = []
            current_file_path = line_info['file_path']
            page_lines.append(f"/* 文件: {line_info['file_path']} */")
            page_lines.append(f"/* 从第 {line_info['line_num']} 行开始 */")
            page_lines.append("/*")
        
        page_lines.append(f"{line_info['line_num']:4d}: {line_info['content']}")
        
        # 达到每页行数，分页
        if len(page_lines) >= LINES_PER_PAGE:
            page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
            page_content = format_page(page_lines, current_page, "后部", current_file_path)
            result.append(page_content)
            result.append("")
            current_page += 1
            page_lines = []
    
    # 输出后部最后一页
    if page_lines:
        page_lines = pad_page_to_lines(page_lines, LINES_PER_PAGE, current_file_path)
        page_content = format_page(page_lines, current_page, "后部", current_file_path)
        result.append(page_content)
        result.append("")
    
    logger.info(f"前后各{PAGES_PER_SECTION}页提取完成")


def main():
    parser = argparse.ArgumentParser(
        description='源代码提取与格式化工具（符合国家版权局要求）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 提取前30页+后30页（代码总行数>=3000）
  python extract_source_code.py --code-dir ./src --output ./code.txt
  
  # 全量提取（代码总行数<3000）
  python extract_source_code.py --code-dir ./src --output ./code.txt
  
  # 指定版本号
  python extract_source_code.py --code-dir ./src --output ./code.txt --version 1.0.0
        """
    )
    parser.add_argument('--code-dir', type=str, required=True, help='代码目录路径')
    parser.add_argument('--output', type=str, required=True, help='输出文件路径')
    parser.add_argument('--version', type=str, default='1.0.0', help='软件版本号（默认1.0.0）')
    parser.add_argument('--lines-per-page', type=int, default=LINES_PER_PAGE, 
                       help=f'每页行数（默认{LINES_PER_PAGE}）')
    parser.add_argument('--min-lines', type=int, default=MIN_TOTAL_LINES,
                       help=f'全量提交的最低行数阈值（默认{MIN_TOTAL_LINES}）')
    
    args = parser.parse_args()
    
    # 检查代码目录
    code_dir = Path(args.code_dir)
    if not code_dir.exists():
        logger.error(f"错误: 代码目录不存在: {code_dir}")
        sys.exit(1)
    
    logger.info(f"软件版本: {args.version}")
    
    # 查找代码文件
    code_files = find_code_files(code_dir)
    
    if not code_files:
        logger.error("错误: 未找到任何代码文件")
        sys.exit(1)
    
    # 查找主入口文件
    main_file = extract_main_code(code_files)
    
    # 统计总行数
    total_lines = count_lines_in_code(code_files)
    logger.info(f"代码总行数: {total_lines}")
    
    # 判断提取策略
    strategy, required_lines = determine_extraction_strategy(total_lines)
    
    # 提取代码
    logger.info("正在提取和格式化代码...")
    try:
        formatted_code = extract_code_pages(code_files, total_lines, strategy)
    except Exception as e:
        logger.error(f"代码提取失败: {e}")
        sys.exit(1)
    
    # 写入输出文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted_code)
    
    logger.info(f"代码提取完成！")
    logger.info(f"输出文件: {output_path}")
    
    if strategy == 'full':
        total_pages = (total_lines + args.lines_per_page - 1) // args.lines_per_page
        logger.info(f"提取策略: 全量提交")
        logger.info(f"总页数: {total_pages} 页")
        logger.info(f"总行数: {total_lines} 行")
    else:
        logger.info(f"提取策略: 前{PAGES_PER_SECTION}页 + 后{PAGES_PER_SECTION}页")
        logger.info(f"总页数: {PAGES_PER_SECTION * 2} 页")
    
    logger.info(f"每页行数: {args.lines_per_page} 行")
    logger.info("请检查输出文件是否符合软著申请要求")


if __name__ == '__main__':
    main()
