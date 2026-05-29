#!/usr/bin/env python3
"""
OpenAPI 3.0 格式验证工具
用于验证 OpenAPI 3.0/YAML 文档的格式正确性和完整性
"""

import sys
import yaml
import json
from typing import Dict, Any, List

def validate_openapi_spec(file_path: str) -> Dict[str, Any]:
    """
    验证 OpenAPI 3.0 规范的 YAML 或 JSON 文件

    Args:
        file_path: 文档文件路径

    Returns:
        包含验证结果的字典
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }

    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.json'):
                spec = json.load(f)
            else:
                spec = yaml.safe_load(f)

        # 验证 OpenAPI 版本
        if 'openapi' not in spec:
            result['errors'].append("缺少 openapi 字段")
            result['valid'] = False
        elif not spec['openapi'].startswith('3.0'):
            result['errors'].append(f"OpenAPI 版本 {spec['openapi']} 不支持，仅支持 3.0.x")
            result['valid'] = False

        # 验证必需字段
        required_fields = ['info', 'paths']
        for field in required_fields:
            if field not in spec:
                result['errors'].append(f"缺少必需字段: {field}")
                result['valid'] = False

        # 验证 info 字段
        if 'info' in spec:
            info = spec['info']
            if 'title' not in info:
                result['warnings'].append("info 缺少 title 字段")
            if 'version' not in info:
                result['warnings'].append("info 缺少 version 字段")

        # 验证 paths 字段
        if 'paths' in spec:
            paths = spec['paths']
            if not isinstance(paths, dict) or len(paths) == 0:
                result['errors'].append("paths 字段必须是非空对象")
                result['valid'] = False
            else:
                for path, methods in paths.items():
                    if not path.startswith('/'):
                        result['errors'].append(f"路径 {path} 必须以 / 开头")
                        result['valid'] = False

                    if not isinstance(methods, dict):
                        result['errors'].append(f"路径 {path} 的值必须是对象")
                        result['valid'] = False
                        continue

                    for method, operation in methods.items():
                        if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace']:
                            result['warnings'].append(f"未知 HTTP 方法: {method}")

                        if 'summary' not in operation:
                            result['warnings'].append(f"{method.upper()} {path} 缺少 summary")

                        if 'responses' not in operation:
                            result['warnings'].append(f"{method.upper()} {path} 缺少 responses")
                        else:
                            responses = operation['responses']
                            if '200' not in responses:
                                result['warnings'].append(f"{method.upper()} {path} 缺少 200 响应定义")

        return result

    except FileNotFoundError:
        result['valid'] = False
        result['errors'].append(f"文件不存在: {file_path}")
        return result
    except yaml.YAMLError as e:
        result['valid'] = False
        result['errors'].append(f"YAML 解析错误: {str(e)}")
        return result
    except json.JSONDecodeError as e:
        result['valid'] = False
        result['errors'].append(f"JSON 解析错误: {str(e)}")
        return result
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"未知错误: {str(e)}")
        return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python validate_openapi.py <openapi.yaml/json>")
        sys.exit(1)

    file_path = sys.argv[1]

    result = validate_openapi_spec(file_path)

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
