#!/usr/bin/env python3
"""
文档生成器 - 基于模板快速生成标准文档

功能:
- 交互式选择模板
- 引导填写变量
- 自动生成文档
- 支持配置文件
- 批量生成模式
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class TemplateLoader:
    """模板加载器"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates = self._scan_templates()
    
    def _scan_templates(self) -> Dict[str, List[Path]]:
        """扫描所有模板"""
        templates = {}
        for subdir in self.templates_dir.iterdir():
            if subdir.is_dir() and subdir.name not in ['__pycache__']:
                category = subdir.name
                templates[category] = []
                for file in subdir.glob('*.md'):
                    if file.name != 'README.md':
                        templates[category].append(file)
        return templates
    
    def list_templates(self) -> None:
        """列出所有可用模板"""
        print("\n可用模板列表:\n")
        for category, files in sorted(self.templates.items()):
            print(f"\033[1;34m{category}/\033[0m")
            for file in files:
                print(f"  - {file.name}")
        print()
    
    def get_template(self, template_path: str) -> Optional[Path]:
        """获取模板文件路径"""
        # 支持完整路径或相对路径
        if '/' in template_path:
            parts = template_path.split('/')
            if len(parts) == 2:
                category, filename = parts
                template_file = self.templates_dir / category / filename
                if template_file.exists():
                    return template_file
        
        # 搜索匹配
        for category, files in self.templates.items():
            for file in files:
                if file.name == template_path or file.stem == template_path:
                    return file
        
        return None
    
    def load_content(self, template_path: Path) -> str:
        """加载模板内容"""
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()


class VariableExtractor:
    """变量提取器"""
    
    @staticmethod
    def extract_variables(content: str) -> List[str]:
        """提取模板中的所有变量"""
        pattern = r'\{\{([*?]?[a-zA-Z_][a-zA-Z0-9_*(?:_[a-zA-Z0-9_]+)*]?)\}\}'
        matches = re.findall(pattern, content)
        return list(set(matches))
    
    @staticmethod
    def parse_variable(var_name: str) -> Dict[str, Any]:
        """解析变量信息"""
        info = {
            'name': var_name,
            'required': True,
            'default': None
        }
        
        if var_name.startswith('*'):
            info['required'] = True
            info['name'] = var_name[1:]
        elif var_name.startswith('?'):
            info['required'] = False
            info['name'] = var_name[1:]
        
        return info


class ConfigLoader:
    """配置文件加载器"""
    
    @staticmethod
    def load(config_path: Path) -> Dict[str, Any]:
        """加载配置文件"""
        if not config_path.exists():
            return {}
        
        suffix = config_path.suffix.lower()
        with open(config_path, 'r', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml'] and HAS_YAML:
                return yaml.safe_load(f) or {}
            elif suffix == '.json':
                return json.load(f)
            else:
                # 尝试自动检测
                content = f.read()
                if content.strip().startswith('{'):
                    return json.loads(content)
                elif HAS_YAML:
                    return yaml.safe_load(content) or {}
        return {}


class DocumentGenerator:
    """文档生成器"""
    
    def __init__(self, template_loader: TemplateLoader):
        self.loader = template_loader
        self.variables: Dict[str, str] = {}
    
    def load_config(self, config_path: Optional[Path]) -> None:
        """加载配置文件"""
        if config_path and config_path.exists():
            config = ConfigLoader.load(config_path)
            self.variables.update(config)
            print(f"✓ 已加载配置文件：{config_path}")
    
    def interactive_input(self, variables: List[str]) -> None:
        """交互式输入变量"""
        print("\n请填写以下变量:\n")
        
        extractor = VariableExtractor()
        for var in sorted(variables):
            var_info = extractor.parse_variable(var)
            var_name = var_info['name']
            
            # 如果已有配置，跳过
            if var_name in self.variables:
                print(f"✓ {var_name}: {self.variables[var_name]} (使用配置值)")
                continue
            
            # 提示输入
            required = var_info['required']
            prompt = f"{var_name}"
            if required:
                prompt += " (必填)"
            else:
                prompt += " (可选)"
            
            value = input(f"{prompt}: ").strip()
            
            if value:
                self.variables[var_name] = value
            elif not required:
                self.variables[var_name] = ""
                print(f"  (留空)")
            else:
                # 必填项不能为空
                while not value:
                    print("  ❌ 必填项不能为空")
                    value = input(f"{var_name} (必填): ").strip()
                self.variables[var_name] = value
    
    def replace_variables(self, content: str) -> str:
        """替换模板变量"""
        result = content
        
        # 替换所有变量
        for var_name, value in self.variables.items():
            # 替换各种格式
            patterns = [
                f'{{{{{var_name}}}}}',  # {{var_name}}
                f'{{{{*{var_name}}}}}',  # {{*var_name}}
                f'{{{{?{var_name}}}}}',  # {{?var_name}}
            ]
            for pattern in patterns:
                result = result.replace(pattern, value)
        
        return result
    
    def generate(self, template_path: Path, output_path: Path, overwrite: bool = False) -> bool:
        """生成文档"""
        # 加载模板
        content = self.loader.load_content(template_path)
        
        # 提取变量
        extractor = VariableExtractor()
        variables = extractor.extract_variables(content)
        
        if not variables:
            print("ℹ 模板中没有变量")
        else:
            print(f"\n发现 {len(variables)} 个变量")
        
        # 交互式输入
        self.interactive_input(variables)
        
        # 替换变量
        result = self.replace_variables(content)
        
        # 检查是否还有未替换的必填变量
        remaining_required = []
        for var in variables:
            var_info = extractor.parse_variable(var)
            if var_info['required'] and var_info['name'] not in self.variables:
                remaining_required.append(var_info['name'])
        
        if remaining_required:
            print(f"\n⚠ 警告：以下必填变量未填写：{', '.join(remaining_required)}")
        
        # 保存文件
        if output_path.exists() and not overwrite:
            response = input(f"\n⚠ 文件已存在：{output_path}\n是否覆盖？(y/N): ")
            if response.lower() != 'y':
                print("已取消")
                return False
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"\n✓ 文档已生成：{output_path}")
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='文档生成器 - 基于模板快速生成标准文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出所有模板
  %(prog)s --list
  
  # 生成单个文档
  %(prog)s --template basic/README.md --output README.md
  
  # 使用配置文件
  %(prog)s --template basic/README.md --output README.md --config config.yaml
  
  # 批量生成项目文档集
  %(prog)s --project my-project --output-dir ./docs
        """
    )
    
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有可用模板')
    parser.add_argument('--template', '-t', type=str,
                        help='模板路径 (如：basic/README.md)')
    parser.add_argument('--output', '-o', type=str,
                        help='输出文件路径')
    parser.add_argument('--config', '-c', type=str,
                        help='配置文件路径 (YAML/JSON)')
    parser.add_argument('--project', '-p', type=str,
                        help='项目名称 (批量生成模式)')
    parser.add_argument('--output-dir', '-d', type=str, default='.',
                        help='输出目录 (默认当前目录)')
    parser.add_argument('--overwrite', action='store_true',
                        help='覆盖已存在的文件')
    parser.add_argument('--templates-dir', type=str, default='project-wiki/templates',
                        help='模板目录路径 (默认：project-wiki/templates)')
    
    args = parser.parse_args()
    
    # 检查模板目录
    templates_dir = Path(args.templates_dir)
    if not templates_dir.exists():
        print(f"❌ 模板目录不存在：{templates_dir}")
        return 1
    
    # 创建加载器
    loader = TemplateLoader(templates_dir)
    
    # 列出模板
    if args.list:
        loader.list_templates()
        return 0
    
    # 批量生成模式
    if args.project:
        print(f"\n📦 批量生成项目文档：{args.project}")
        # TODO: 实现批量生成
        print("⚠ 批量生成功能开发中，请使用单个文档生成模式")
        return 1
    
    # 单个文档生成
    if args.template:
        template_path = loader.get_template(args.template)
        if not template_path:
            print(f"❌ 模板不存在：{args.template}")
            print("\n使用 --list 查看所有可用模板")
            return 1
        
        output_path = Path(args.output or f"./{template_path.name}")
        
        # 创建生成器
        generator = DocumentGenerator(loader)
        
        # 加载配置
        if args.config:
            generator.load_config(Path(args.config))
        
        # 生成文档
        success = generator.generate(template_path, output_path, args.overwrite)
        return 0 if success else 1
    
    # 没有提供任何参数，显示帮助
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
