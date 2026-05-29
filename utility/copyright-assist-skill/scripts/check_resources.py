#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源完整性检查工具
用于软件著作权申请前的资源准备检查
改进：添加详细日志和错误处理，提供解决方案链接
"""

import os
import argparse
import sys
import logging
from pathlib import Path
from typing import List, Dict, Set
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 软著申请所需的最小资源要求
MIN_REQUIREMENTS = {
    'code': {
        'description': '源代码文件',
        'min_count': 1,
        'extensions': {'.py', '.java', '.c', '.cpp', '.js', '.ts', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.cs', '.m'}
    },
    'screenshot': {
        'description': '软件运行截图',
        'min_count': 5,
        'extensions': {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    },
    'document': {
        'description': '项目文档（README、设计文档、需求文档等）',
        'min_count': 0,  # 可选
        'extensions': {'.md', '.txt', '.doc', '.docx', '.pdf', '.rst'}
    }
}

# 忽略的目录
IGNORE_DIRS = {
    '__pycache__', 'node_modules', '.git', '.venv', 'venv', 'env',
    'dist', 'build', 'target', '.idea', '.vscode', 'vendor',
    'logs', 'tmp', 'temp', 'cache', '.cache'
}


def find_files_by_type(directory: Path, extensions: Set[str]) -> List[Path]:
    """查找指定类型的文件"""
    files = []
    
    if not directory.exists():
        logger.warning(f"目录不存在: {directory}")
        return files
    
    for root, dirs, file_names in os.walk(directory):
        # 过滤常见忽略目录
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file_name in file_names:
            file_path = Path(root) / file_name
            if file_path.suffix.lower() in extensions:
                files.append(file_path)
    
    return files


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


def analyze_screenshots(files: List[Path]) -> Dict:
    """分析截图文件"""
    if not files:
        logger.warning("未找到任何截图文件")
        return {
            'count': 0,
            'size_range': '0 KB',
            'formats': set(),
            'issues': []
        }
    
    total_size = 0
    formats = set()
    issues = []
    low_resolution_files = []
    
    for file_path in files:
        if file_path.exists():
            try:
                size = file_path.stat().st_size
                total_size += size
                formats.add(file_path.suffix.lower())
                
                # 检查文件大小（简单判断分辨率）
                size_kb = size / 1024
                if size_kb < 50:  # 小于50KB可能分辨率过低
                    low_resolution_files.append((file_path.name, size_kb))
                    issues.append({
                        'file': file_path.name,
                        'issue': '文件过小，可能分辨率不足',
                        'size_kb': size_kb,
                        'recommendation': '建议截图分辨率至少1280x720，文件大小建议大于100KB'
                    })
            except Exception as e:
                logger.warning(f"分析截图失败 {file_path}: {e}")
                continue
    
    avg_size = total_size / len(files) if files else 0
    
    if low_resolution_files:
        logger.warning(f"发现 {len(low_resolution_files)} 个可能的低分辨率截图:")
        for file_name, size_kb in low_resolution_files:
            logger.warning(f"  - {file_name}: {size_kb:.1f} KB")
    
    return {
        'count': len(files),
        'total_size_kb': total_size / 1024,
        'avg_size_kb': avg_size / 1024,
        'formats': list(formats),
        'issues': issues
    }


def check_code_sufficiency(files: List[Path]) -> Dict:
    """检查代码是否满足软著要求"""
    total_lines = count_lines_in_code(files)
    min_required_lines = 3000  # 60页 × 50行
    
    issues = []
    
    if total_lines < min_required_lines:
        issues.append({
            'type': 'code_insufficient',
            'current_lines': total_lines,
            'required_lines': min_required_lines,
            'recommendation': f'代码行数 ({total_lines}) 不足，建议补充至少 {min_required_lines - total_lines} 行',
            'solution': '参考文档：references/source-code-format.md 了解如何补充代码'
        })
    
    return {
        'total_files': len(files),
        'total_lines': total_lines,
        'required_lines': min_required_lines,
        'sufficient': total_lines >= min_required_lines,
        'recommendation': (
            f"代码行数 ({total_lines}) 符合软著要求 (≥{min_required_lines}行)"
            if total_lines >= min_required_lines
            else f"代码行数 ({total_lines}) 不足，建议补充至少 {min_required_lines - total_lines} 行"
        ),
        'issues': issues
    }


def generate_check_report(code_dir: Path, doc_dir: Path, screenshot_dir: Path) -> Dict:
    """生成资源检查报告"""
    logger.info("开始生成资源检查报告...")
    
    report = {
        'timestamp': str(Path.cwd()),
        'status': 'unknown',
        'categories': {},
        'warnings': [],
        'recommendations': [],
        'issues': []
    }
    
    # 检查源代码
    logger.info("检查源代码...")
    code_files = find_files_by_type(code_dir, MIN_REQUIREMENTS['code']['extensions'])
    code_check = check_code_sufficiency(code_files)
    
    report['categories']['code'] = {
        'description': '源代码文件',
        'found': len(code_files),
        'required': MIN_REQUIREMENTS['code']['min_count'],
        'sufficient': len(code_files) >= MIN_REQUIREMENTS['code']['min_count'],
        'details': code_check
    }
    
    if len(code_files) < MIN_REQUIREMENTS['code']['min_count']:
        report['warnings'].append("源代码文件数量不足")
        report['issues'].append({
            'category': 'code',
            'issue': 'code_count_insufficient',
            'message': '源代码文件数量不足',
            'found': len(code_files),
            'required': MIN_REQUIREMENTS['code']['min_count'],
            'solution': '确保代码目录包含主要业务逻辑代码文件'
        })
    
    if not code_check['sufficient']:
        report['warnings'].append("代码行数不满足软著要求（需要至少3000行）")
        report['recommendations'].append(
            f"建议补充代码，或参考 references/source-code-format.md 了解代码格式要求"
        )
    
    # 收集代码问题
    if code_check.get('issues'):
        report['issues'].extend(code_check['issues'])
    
    # 检查截图
    logger.info("检查截图文件...")
    screenshot_files = find_files_by_type(screenshot_dir, MIN_REQUIREMENTS['screenshot']['extensions'])
    screenshot_info = analyze_screenshots(screenshot_files)
    
    report['categories']['screenshot'] = {
        'description': '软件运行截图',
        'found': screenshot_info['count'],
        'required': MIN_REQUIREMENTS['screenshot']['min_count'],
        'sufficient': screenshot_info['count'] >= MIN_REQUIREMENTS['screenshot']['min_count'],
        'details': screenshot_info
    }
    
    if screenshot_info['count'] < MIN_REQUIREMENTS['screenshot']['min_count']:
        report['warnings'].append(f"截图数量不足（需要至少{MIN_REQUIREMENTS['screenshot']['min_count']}张）")
        report['recommendations'].append(
            f"建议准备软件运行截图，包括：登录界面、主要功能模块、数据操作、报表导出等场景，每个场景至少2-3张截图。"
            f"参考文档：references/user-manual-guide.md 了解截图规范。"
        )
        report['issues'].append({
            'category': 'screenshot',
            'issue': 'screenshot_count_insufficient',
            'message': '截图数量不足',
            'found': screenshot_info['count'],
            'required': MIN_REQUIREMENTS['screenshot']['min_count'],
            'solution': '准备更多软件运行截图，覆盖主要功能模块'
        })
    
    # 收集截图问题
    if screenshot_info.get('issues'):
        report['issues'].extend(screenshot_info['issues'])
        report['warnings'].append("部分截图可能存在问题（分辨率过低）")
        report['recommendations'].append(
            "建议检查截图分辨率，确保至少1280x720，文件大小建议大于100KB。"
        )
    
    # 检查文档
    logger.info("检查项目文档...")
    doc_files = find_files_by_type(doc_dir, MIN_REQUIREMENTS['document']['extensions'])
    
    report['categories']['document'] = {
        'description': '项目文档',
        'found': len(doc_files),
        'required': MIN_REQUIREMENTS['document']['min_count'],
        'sufficient': True,  # 文档是可选的
        'details': {
            'files': [str(f.relative_to(doc_dir)) for f in doc_files[:10]] if doc_files else []
        }
    }
    
    if not doc_files:
        report['recommendations'].append(
            "建议准备项目文档（如README、需求文档、设计文档等），有助于说明书撰写。"
        )
        report['issues'].append({
            'category': 'document',
            'issue': 'document_missing',
            'message': '未找到项目文档',
            'solution': '准备项目文档（README、需求文档、设计文档等）'
        })
    else:
        logger.info(f"找到 {len(doc_files)} 个文档文件")
    
    # 总体状态
    code_ok = report['categories']['code']['sufficient'] and code_check['sufficient']
    screenshot_ok = report['categories']['screenshot']['sufficient']
    no_critical_issues = len([i for i in report['issues'] if i.get('type') == 'code_insufficient']) == 0
    
    report['status'] = 'ready' if (code_ok and screenshot_ok) else 'needs_action'
    
    logger.info(f"资源检查完成，状态: {report['status']}")
    
    return report


def print_report(report: Dict):
    """打印检查报告"""
    print("\n" + "=" * 80)
    print("资源完整性检查报告")
    print("=" * 80)
    
    # 打印各项检查结果
    for category, info in report['categories'].items():
        print(f"\n【{info['description']}】")
        print(f"  找到: {info['found']} 个文件/项")
        print(f"  要求: {'至少 ' + str(info['required']) + ' 个' if info['required'] > 0 else '无'}")
        
        if category == 'code':
            details = info['details']
            print(f"  代码总行数: {details['total_lines']} 行")
            print(f"  要求行数: {details['required_lines']} 行")
            print(f"  状态: {'✓ 符合' if details['sufficient'] else '✗ 不符合'}")
            
            if details.get('issues'):
                print(f"\n  ⚠  问题:")
                for issue in details['issues']:
                    print(f"    - {issue['recommendation']}")
                    
        elif category == 'screenshot':
            details = info['details']
            print(f"  截图总数: {details['count']} 张")
            print(f"  平均大小: {details['avg_size_kb']:.1f} KB")
            print(f"  格式: {', '.join(details['formats']) if details['formats'] else '无'}")
            print(f"  状态: {'✓ 充足' if info['sufficient'] else '✗ 不足'}")
            
            if details.get('issues'):
                print(f"\n  ⚠  问题:")
                for issue in details['issues']:
                    print(f"    - {issue['file']}: {issue['issue']}")
                    print(f"      建议: {issue['recommendation']}")
                    
        elif category == 'document':
            if info['details'].get('files'):
                print(f"  文档列表:")
                for file in info['details']['files'][:5]:
                    print(f"    - {file}")
                if len(info['details']['files']) > 5:
                    print(f"    ... 还有 {len(info['details']['files']) - 5} 个文件")
            else:
                print(f"  文档: 未找到（可选）")
    
    # 打印问题列表
    if report['issues']:
        print("\n" + "⚠ " * 40)
        print("详细问题列表:")
        for i, issue in enumerate(report['issues'], 1):
            print(f"\n  {i}. [{issue.get('category', 'unknown').upper()}] {issue.get('message', '未知问题')}")
            print(f"     解决方案: {issue.get('solution', '请联系技术支持')}")
            
            if issue.get('file'):
                print(f"     相关文件: {issue['file']}")
            if issue.get('size_kb'):
                print(f"     文件大小: {issue['size_kb']:.1f} KB")
    
    # 打印警告
    if report['warnings']:
        print("\n" + "⚠ " * 20)
        print("警告:")
        for warning in report['warnings']:
            print(f"  • {warning}")
    
    # 打印建议
    if report['recommendations']:
        print("\n" + "💡 " * 20)
        print("建议:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    # 打印总体状态
    print("\n" + "=" * 80)
    if report['status'] == 'ready':
        print("✓ 资源检查通过，可以开始准备软著申请材料")
    else:
        print("✗ 资源不完整，请根据上述建议补充缺失资源")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='资源完整性检查工具（软件著作权申请）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检查默认目录
  python check_resources.py --code-dir ./src
  
  # 检查指定目录并输出JSON报告
  python check_resources.py --code-dir ./src --doc-dir ./docs --screenshot-dir ./screenshots --output report.json
        """
    )
    parser.add_argument('--code-dir', type=str, required=True, help='代码目录路径')
    parser.add_argument('--doc-dir', type=str, default='./docs', help='文档目录路径（默认./docs）')
    parser.add_argument('--screenshot-dir', type=str, default='./screenshots', help='截图目录路径（默认./screenshots）')
    parser.add_argument('--output', type=str, help='输出JSON报告文件路径（可选）')
    
    args = parser.parse_args()
    
    # 构建路径
    code_dir = Path(args.code_dir)
    doc_dir = Path(args.doc_dir)
    screenshot_dir = Path(args.screenshot_dir)
    
    logger.info(f"代码目录: {code_dir}")
    logger.info(f"文档目录: {doc_dir}")
    logger.info(f"截图目录: {screenshot_dir}")
    
    # 生成检查报告
    report = generate_check_report(code_dir, doc_dir, screenshot_dir)
    
    # 打印报告
    print_report(report)
    
    # 保存JSON报告
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON报告已保存到: {output_path}")
    
    # 返回状态码
    sys.exit(0 if report['status'] == 'ready' else 1)


if __name__ == '__main__':
    main()
