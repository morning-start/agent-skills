#!/usr/bin/env python3
"""
模块分类脚本

用于基于路由路径自动划分模块和层级结构。
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any


class ModuleClassifier:
    """模块分类器"""

    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        self.modules = {}

    def load_scan_result(self) -> Dict[str, Any]:
        """加载扫描结果"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def classify(self) -> Dict[str, List[Dict[str, Any]]]:
        """分类模块"""
        scan_result = self.load_scan_result()
        endpoints = scan_result.get('endpoints', [])
        framework = scan_result.get('framework', 'unknown')

        for endpoint in endpoints:
            if endpoint.get('type') == 'component':
                self._classify_component(endpoint)
            else:
                self._classify_endpoint(endpoint)

        return self.modules

    def _classify_endpoint(self, endpoint: Dict[str, Any]):
        """分类 API 端点"""
        path = endpoint.get('path', '')
        method = endpoint.get('method', 'GET')

        # 提取模块名（路径的第一段）
        segments = [s for s in path.split('/') if s]
        if not segments:
            module_name = 'root'
        else:
            module_name = segments[0]

        # 创建模块（如果不存在）
        if module_name not in self.modules:
            self.modules[module_name] = []

        # 添加端点到模块
        self.modules[module_name].append({
            'path': path,
            'method': method,
            'file': endpoint.get('file', ''),
            'framework': endpoint.get('framework', 'unknown')
        })

    def _classify_component(self, component: Dict[str, Any]):
        """分类前端组件"""
        name = component.get('name', '')
        file_path = component.get('file', '')

        # 提取模块名（文件路径的第一段）
        segments = [s for s in file_path.split('/') if s]
        if len(segments) > 1:
            module_name = segments[0]
        else:
            module_name = 'components'

        # 创建模块（如果不存在）
        if module_name not in self.modules:
            self.modules[module_name] = []

        # 添加组件到模块
        self.modules[module_name].append({
            'name': name,
            'type': 'component',
            'file': file_path,
            'framework': component.get('framework', 'unknown')
        })

    def analyze_hierarchy(self) -> Dict[str, Any]:
        """分析层级结构"""
        hierarchy = {}

        for module_name, items in self.modules.items():
            # 分析路径深度
            depths = []
            for item in items:
                if item.get('type') == 'component':
                    continue

                path = item.get('path', '')
                depth = len([s for s in path.split('/') if s])
                depths.append(depth)

            if depths:
                avg_depth = sum(depths) / len(depths)
                max_depth = max(depths)
            else:
                avg_depth = 0
                max_depth = 0

            hierarchy[module_name] = {
                'count': len(items),
                'avg_depth': avg_depth,
                'max_depth': max_depth
            }

        return hierarchy


def main():
    parser = argparse.ArgumentParser(description='模块分类脚本')
    parser.add_argument('--input', required=True, help='输入JSON文件路径')
    parser.add_argument('--output', default='api_modules.json', help='输出JSON文件路径')

    args = parser.parse_args()

    classifier = ModuleClassifier(args.input)
    modules = classifier.classify()
    hierarchy = classifier.analyze_hierarchy()

    result = {
        'modules': modules,
        'hierarchy': hierarchy
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"模块分类完成，共 {len(modules)} 个模块")
    for module_name, items in modules.items():
        print(f"  - {module_name}: {len(items)} 个端点/组件")
    print(f"结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
