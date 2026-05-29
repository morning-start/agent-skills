#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
软著申请材料打包工具
自动将说明书和源代码打包为符合命名规范的ZIP包
"""

import os
import argparse
import sys
import logging
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def find_files_by_pattern(directory: Path, patterns: List[str]) -> List[Path]:
    """查找匹配模式的文件"""
    files = []
    
    if not directory.exists():
        logger.warning(f"目录不存在: {directory}")
        return files
    
    for root, dirs, file_names in os.walk(directory):
        for file_name in file_names:
            file_path = Path(root) / file_name
            # 检查文件名是否匹配任一模式
            if any(pattern in file_name.lower() for pattern in patterns):
                files.append(file_path)
    
    return files


def generate_zip_filename(software_name: str, version: str) -> str:
    """
    生成符合命名规范的ZIP文件名
    
    格式: 软件名称_版本号.zip
    示例: 用户管理系统_1.0.0.zip
    """
    # 清理软件名称中的特殊字符
    clean_name = software_name.replace(' ', '_').replace('-', '_')
    filename = f"{clean_name}_{version}.zip"
    return filename


def validate_package_structure(software_name: str, version: str, 
                            manual_file: Optional[Path], 
                            code_file: Optional[Path]) -> List[str]:
    """
    验证包结构是否完整
    
    Returns:
        验证错误列表（空列表表示验证通过）
    """
    errors = []
    
    if not manual_file or not manual_file.exists():
        errors.append(f"未找到说明书文件: {manual_file}")
        errors.append("  生成说明书可参考 SKILL.md 中的操作步骤")
    
    if not code_file or not code_file.exists():
        errors.append(f"未找到源代码文件: {code_file}")
        errors.append("  提取源代码可运行: scripts/extract_source_code.py")
    
    # 检查文件大小
    if manual_file and manual_file.exists():
        size_kb = manual_file.stat().st_size / 1024
        if size_kb < 10:  # 小于10KB可能内容不足
            errors.append(f"说明书文件过小 ({size_kb:.1f} KB)，可能内容不足")
            logger.warning(f"说明书文件大小: {size_kb:.1f} KB")
    
    if code_file and code_file.exists():
        size_kb = code_file.stat().st_size / 1024
        lines = 0
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            
            if lines < 3000:
                errors.append(f"源代码行数不足 ({lines} 行)，建议至少3000行")
                logger.warning(f"源代码行数: {lines} 行")
        except Exception as e:
            errors.append(f"无法读取源代码文件: {e}")
    
    return errors


def package_submission(software_name: str, 
                     version: str,
                     manual_file: Path,
                     code_file: Path,
                     output_dir: Path,
                     rename_files: bool = True) -> Path:
    """
    打包软著申请材料
    
    Args:
        software_name: 软件名称
        version: 版本号
        manual_file: 说明书文件路径
        code_file: 源代码文件路径
        output_dir: 输出目录
        rename_files: 是否重命名文件为标准格式
    
    Returns:
        生成的ZIP文件路径
    """
    # 验证包结构
    logger.info("验证包结构...")
    errors = validate_package_structure(software_name, version, manual_file, code_file)
    if errors:
        logger.error("包结构验证失败:")
        for error in errors:
            logger.error(f"  {error}")
        raise ValueError("包结构验证失败")
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成ZIP文件名
    zip_filename = generate_zip_filename(software_name, version)
    zip_path = output_dir / zip_filename
    
    logger.info(f"正在打包: {zip_path}")
    
    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 确定ZIP内的文件名
        if rename_files:
            manual_zip_name = f"{software_name}_{version}_说明书{manual_file.suffix}"
            code_zip_name = f"{software_name}_{version}_源代码{code_file.suffix}"
        else:
            manual_zip_name = manual_file.name
            code_zip_name = code_file.name
        
        # 添加说明书文件
        logger.info(f"  添加: {manual_file.name} -> {manual_zip_name}")
        zipf.write(manual_file, manual_zip_name)
        
        # 添加源代码文件
        logger.info(f"  添加: {code_file.name} -> {code_zip_name}")
        zipf.write(code_file, code_zip_name)
        
        # 可选：添加资源清单
        manifest = create_manifest(software_name, version, manual_file, code_file)
        zipf.writestr(f"{software_name}_{version}_资源清单.txt", manifest)
        logger.info(f"  添加: 资源清单.txt")
    
    # 显示ZIP文件信息
    zip_size_kb = zip_path.stat().st_size / 1024
    logger.info(f"打包完成!")
    logger.info(f"  文件: {zip_path}")
    logger.info(f"  大小: {zip_size_kb:.1f} KB")
    logger.info(f"  包含文件:")
    logger.info(f"    1. {software_name}_{version}_说明书{manual_file.suffix}")
    logger.info(f"    2. {software_name}_{version}_源代码{code_file.suffix}")
    logger.info(f"    3. {software_name}_{version}_资源清单.txt")
    
    return zip_path


def create_manifest(software_name: str, version: str,
                   manual_file: Path, code_file: Path) -> str:
    """创建资源清单"""
    manifest = []
    manifest.append("=" * 80)
    manifest.append("软件著作权申请材料清单")
    manifest.append("=" * 80)
    manifest.append("")
    manifest.append(f"软件名称: {software_name}")
    manifest.append(f"版本号: {version}")
    manifest.append(f"打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    manifest.append("")
    manifest.append("-" * 80)
    manifest.append("包含文件:")
    manifest.append("-" * 80)
    
    # 添加说明书信息
    manual_size_kb = manual_file.stat().st_size / 1024
    manifest.append(f"\n1. 说明书文件")
    manifest.append(f"   文件名: {software_name}_{version}_说明书{manual_file.suffix}")
    manifest.append(f"   原始路径: {manual_file}")
    manifest.append(f"   文件大小: {manual_size_kb:.1f} KB")
    
    # 添加源代码信息
    code_size_kb = code_file.stat().st_size / 1024
    code_lines = 0
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            code_lines = sum(1 for _ in f)
    except Exception:
        pass
    
    manifest.append(f"\n2. 源代码文件")
    manifest.append(f"   文件名: {software_name}_{version}_源代码{code_file.suffix}")
    manifest.append(f"   原始路径: {code_file}")
    manifest.append(f"   文件大小: {code_size_kb:.1f} KB")
    manifest.append(f"   代码行数: {code_lines} 行")
    
    manifest.append("")
    manifest.append("=" * 80)
    manifest.append("注意事项:")
    manifest.append("=" * 80)
    manifest.append("1. 请在提交前仔细检查文件内容是否正确")
    manifest.append("2. 确保说明书页数符合要求（通常60页以上）")
    manifest.append("3. 确保源代码格式符合软著申请要求")
    manifest.append("4. 如有任何问题，请参考相关文档或联系技术支持")
    manifest.append("")
    
    return '\n'.join(manifest)


def main():
    parser = argparse.ArgumentParser(
        description='软著申请材料打包工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python package_submission.py --software-name "用户管理系统" --version 1.0.0 \\
      --manual ./用户说明书.pdf --code ./formatted_code.txt
  
  # 指定输出目录
  python package_submission.py --software-name "用户管理系统" --version 1.0.0 \\
      --manual ./用户说明书.pdf --code ./formatted_code.txt \\
      --output ./output
  
  # 不重命名文件
  python package_submission.py --software-name "用户管理系统" --version 1.0.0 \\
      --manual ./用户说明书.pdf --code ./formatted_code.txt \\
      --no-rename
        """
    )
    parser.add_argument('--software-name', type=str, required=True, 
                       help='软件名称（如: 用户管理系统）')
    parser.add_argument('--version', type=str, required=True, 
                       help='软件版本号（如: 1.0.0）')
    parser.add_argument('--manual', type=str, required=True, 
                       help='说明书文件路径（支持PDF、Word、Markdown等格式）')
    parser.add_argument('--code', type=str, required=True, 
                       help='源代码文件路径（通常是extract_source_code.py生成的TXT文件）')
    parser.add_argument('--output', type=str, default='./output', 
                       help='输出目录（默认./output）')
    parser.add_argument('--no-rename', action='store_true',
                       help='不重命名文件，使用原始文件名')
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("软著申请材料打包工具")
    logger.info("=" * 80)
    logger.info(f"软件名称: {args.software_name}")
    logger.info(f"版本号: {args.version}")
    
    # 构建路径
    manual_file = Path(args.manual)
    code_file = Path(args.code)
    output_dir = Path(args.output)
    
    # 验证文件存在
    if not manual_file.exists():
        logger.error(f"说明书文件不存在: {manual_file}")
        sys.exit(1)
    
    if not code_file.exists():
        logger.error(f"源代码文件不存在: {code_file}")
        sys.exit(1)
    
    # 打包
    try:
        zip_path = package_submission(
            software_name=args.software_name,
            version=args.version,
            manual_file=manual_file,
            code_file=code_file,
            output_dir=output_dir,
            rename_files=not args.no_rename
        )
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("✓ 打包成功!")
        logger.info("=" * 80)
        logger.info(f"输出文件: {zip_path}")
        logger.info("可以直接用于软著申请上传")
        
    except Exception as e:
        logger.error(f"打包失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
