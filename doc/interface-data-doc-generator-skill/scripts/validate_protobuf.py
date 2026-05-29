#!/usr/bin/env python3
"""
Protobuf 格式验证工具
用于验证 .proto 文件的语法正确性
"""

import sys
import subprocess
from typing import Dict, Any

def validate_protobuf_file(file_path: str) -> Dict[str, Any]:
    """
    使用 protoc 编译器验证 .proto 文件的语法正确性

    Args:
        file_path: .proto 文件路径

    Returns:
        包含验证结果的字典
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }

    try:
        # 检查 protoc 是否可用
        try:
            subprocess.run(['protoc', '--version'],
                          capture_output=True,
                          check=True,
                          text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            result['valid'] = False
            result['errors'].append("protoc 编译器未安装或不在 PATH 中")
            result['warnings'].append("安装提示: https://grpc.io/docs/protoc-installation/")
            return result

        # 使用 protoc 进行语法检查（不生成代码）
        # 使用 --decode_raw 可以快速验证语法而无需指定输出目录
        cmd = ['protoc', '--proto_path=.']

        # 如果有 import，可能需要指定 include paths
        cmd.append(file_path)

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            result['valid'] = False
            result['errors'].append(f"protoc 验证失败: {process.stderr.strip()}")
        else:
            # 检查文件内容的基本规范
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # 检查版本号声明
                if 'syntax' not in content:
                    result['warnings'].append("建议在文件开头添加 syntax 声明 (如: syntax = \"proto3\";)")

                # 检查 package 声明
                if 'package' not in content:
                    result['warnings'].append("建议添加 package 声明以防止命名冲突")

        return result

    except FileNotFoundError:
        result['valid'] = False
        result['errors'].append(f"文件不存在: {file_path}")
        return result
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"未知错误: {str(e)}")
        return result


def basic_syntax_check(file_path: str) -> Dict[str, Any]:
    """
    基础语法检查（不依赖 protoc）

    Args:
        file_path: .proto 文件路径

    Returns:
        包含检查结果的字典
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # 检查消息定义
        message_count = 0
        for line in lines:
            line = line.strip()
            if line.startswith('message '):
                message_count += 1
                # 检查消息名称是否符合规范
                msg_name = line.split()[1].replace('{', '').strip()
                if not msg_name[0].isupper():
                    result['warnings'].append(f"消息名称 {msg_name} 建议使用大驼峰命名")

        if message_count == 0:
            result['warnings'].append("未找到任何消息定义")

        return result

    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"基础检查失败: {str(e)}")
        return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python validate_protobuf.py <file.proto>")
        sys.exit(1)

    file_path = sys.argv[1]

    # 先进行基础语法检查
    basic_result = basic_syntax_check(file_path)

    # 然后使用 protoc 进行完整验证
    protoc_result = validate_protobuf_file(file_path)

    # 合并结果
    result = {
        'valid': protoc_result['valid'] and basic_result['valid'],
        'errors': protoc_result['errors'] + basic_result['errors'],
        'warnings': protoc_result['warnings'] + basic_result['warnings']
    }

    if result['valid']:
        print(f"✓ {file_path} 验证通过")
    else:
        print(f"✗ {file_path} 验证失败")

    if result['errors']:
        print("\n错误:")
        for error in result['errors']:
            print(f"  - {error}")

    if result['warnings']:
        print("\n警告:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    sys.exit(0 if result['valid'] else 1)


if __name__ == '__main__':
    main()
