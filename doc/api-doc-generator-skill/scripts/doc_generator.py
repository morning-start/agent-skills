#!/usr/bin/env python3
"""
文档生成脚本

用于根据模块划分结果生成完整的 API 文档。
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any


class DocGenerator:
    """文档生成器"""

    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(__file__).parent.parent / 'assets' / 'templates'

    def load_modules(self) -> Dict[str, Any]:
        """加载模块分类结果"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate(self):
        """生成文档"""
        modules_data = self.load_modules()
        modules = modules_data.get('modules', {})
        hierarchy = modules_data.get('hierarchy', {})

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 生成概述文档
        self._generate_overview(modules, hierarchy)

        # 生成模块文档
        for module_name, items in modules.items():
            self._generate_module(module_name, items)

        print(f"文档生成完成，输出目录: {self.output_dir}")

    def _generate_overview(self, modules: Dict[str, List[Dict[str, Any]]], hierarchy: Dict[str, Any]):
        """生成概述文档"""
        overview_template = self.templates_dir / 'overview-template.md'

        if not overview_template.exists():
            print(f"警告: 概述模板不存在: {overview_template}")
            return

        with open(overview_template, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 替换模板变量
        content = template_content.replace('{{MODULE_COUNT}}', str(len(modules)))
        content = content.replace('{{ENDPOINT_COUNT}}', str(sum(len(items) for items in modules.values())))

        # 写入文件
        output_file = self.output_dir / 'overview.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"生成概述文档: {output_file}")

    def _generate_module(self, module_name: str, items: List[Dict[str, Any]]):
        """生成模块文档"""
        module_template = self.templates_dir / 'module-template.md'

        if not module_template.exists():
            print(f"警告: 模块模板不存在: {module_template}")
            return

        with open(module_template, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 替换模板变量
        content = template_content.replace('{{MODULE_NAME}}', module_name)
        content = content.replace('{{ITEM_COUNT}}', str(len(items)))

        # 生成端点列表
        endpoint_list = []
        for item in items:
            if item.get('type') == 'component':
                endpoint_list.append(f"- **{item.get('name')}** ({item.get('file')})")
            else:
                endpoint_list.append(f"- **{item.get('method')}** {item.get('path')} ({item.get('file')})")

        content = content.replace('{{ENDPOINT_LIST}}', '\n'.join(endpoint_list))

        # 写入文件
        output_file = self.output_dir / f'{module_name}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"生成模块文档: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='文档生成脚本')
    parser.add_argument('--input', required=True, help='输入JSON文件路径')
    parser.add_argument('--output-dir', default='api', help='输出目录')

    args = parser.parse_args()

    generator = DocGenerator(args.input, args.output_dir)
    generator.generate()


if __name__ == '__main__':
    main()
