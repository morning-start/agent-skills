#!/usr/bin/env python3
"""
SQL DDL 格式验证工具
用于验证数据库表结构定义的 SQL 语法正确性
"""

import sys
import re
from typing import Dict, Any, List

def validate_sql_syntax(sql: str) -> Dict[str, Any]:
    """
    验证 SQL DDL 语法的基本正确性

    Args:
        sql: SQL DDL 语句字符串

    Returns:
        包含验证结果的字典
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }

    # 移除注释和多余空格
    lines = sql.strip().split('\n')
    cleaned_lines = []
    for line in lines:
        # 移除 -- 注释
        line = re.sub(r'--.*$', '', line)
        # 移除 /* */ 注释
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        cleaned_lines.append(line.strip())

    cleaned_sql = '\n'.join(cleaned_lines)

    # 基础语法检查
    if not cleaned_sql:
        result['errors'].append("SQL 内容为空")
        result['valid'] = False
        return result

    # 检查 CREATE TABLE 语句
    create_table_pattern = r'CREATE\s+TABLE\s+`?(\w+)`?\s*\((.*?)\)'
    matches = re.findall(create_table_pattern, cleaned_sql, re.IGNORECASE | re.DOTALL)

    if not matches:
        result['warnings'].append("未找到 CREATE TABLE 语句，请确认输入是否为 DDL 语句")
    else:
        for table_name, table_body in matches:
            # 检查主键
            if 'PRIMARY KEY' not in table_body.upper() and 'PRIMARY KEY' not in cleaned_sql.upper():
                result['warnings'].append(f"表 {table_name} 未定义主键")

            # 检查字段定义
            fields = re.findall(r'`?(\w+)`?\s+(\w+)(\(\d+\))?', table_body)
            if not fields:
                result['errors'].append(f"表 {table_name} 未定义任何字段")
                result['valid'] = False
            else:
                for field_name, field_type, field_length in fields:
                    # 检查字段类型
                    valid_types = ['INT', 'VARCHAR', 'CHAR', 'TEXT', 'BIGINT', 'SMALLINT', 'TINYINT',
                                   'DECIMAL', 'FLOAT', 'DOUBLE', 'DATETIME', 'DATE', 'TIMESTAMP',
                                   'BOOLEAN', 'JSON', 'BLOB', 'ENUM']
                    if field_type.upper() not in valid_types:
                        result['warnings'].append(f"表 {table_name} 字段 {field_name} 使用了不常见的类型: {field_type}")

                    # 检查 VARCHAR 长度
                    if field_type.upper() == 'VARCHAR' and not field_length:
                        result['errors'].append(f"表 {table_name} 字段 {field_name} (VARCHAR) 必须指定长度")
                        result['valid'] = False

    # 检查括号匹配
    open_brackets = cleaned_sql.count('(')
    close_brackets = cleaned_sql.count(')')
    if open_brackets != close_brackets:
        result['errors'].append(f"括号不匹配: 左括号 {open_brackets} 个，右括号 {close_brackets} 个")
        result['valid'] = False

    # 检查分号
    if not cleaned_sql.strip().endswith(';'):
        result['warnings'].append("SQL 语句建议以分号结尾")

    return result


def validate_sql_file(file_path: str) -> Dict[str, Any]:
    """
    验证 SQL 文件

    Args:
        file_path: SQL 文件路径

    Returns:
        包含验证结果的字典
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 如果文件包含多个语句，按分号分割
        statements = []
        current_statement = []
        for line in sql_content.split('\n'):
            line = line.strip()
            if line.startswith('--'):
                continue
            current_statement.append(line)
            if line.endswith(';'):
                statements.append('\n'.join(current_statement))
                current_statement = []

        if current_statement:
            statements.append('\n'.join(current_statement))

        # 验证每个语句
        for i, stmt in enumerate(statements):
            stmt_result = validate_sql_syntax(stmt)
            if not stmt_result['valid']:
                result['valid'] = False
                result['errors'].extend([f"语句 {i+1}: {err}" for err in stmt_result['errors']])
            result['warnings'].extend([f"语句 {i+1}: {warn}" for warn in stmt_result['warnings']])

        return result

    except FileNotFoundError:
        result['valid'] = False
        result['errors'].append(f"文件不存在: {file_path}")
        return result
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"未知错误: {str(e)}")
        return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python validate_sql.py <schema.sql>")
        sys.exit(1)

    file_path = sys.argv[1]

    result = validate_sql_file(file_path)

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
