#!/usr/bin/env python3
"""
API 扫描脚本

用于扫描项目代码，提取 API 路由和参数信息。

支持框架：
- 后端：Flask, FastAPI, Django, Express, NestJS, Spring Boot, Gin, Echo
- 前端：React, Vue, Angular, Svelte, Next.js, Nuxt.js
"""

import argparse
import ast
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class APIScanner:
    """API 扫描器"""

    def __init__(self, project_dir: str, framework: str = 'auto'):
        self.project_dir = Path(project_dir)
        self.framework = framework
        self.endpoints = []
        self.framework_detected = None

    def detect_framework(self) -> str:
        """检测项目使用的框架"""
        if self.framework != 'auto':
            return self.framework

        # 后端框架检测
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                file_path = Path(root) / file
                if not file_path.suffix in ['.py', '.js', '.ts', '.java', '.go']:
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                # FastAPI
                if 'from fastapi import' in content or 'FastAPI(' in content:
                    return 'fastapi'
                # Flask
                if 'from flask import' in content or 'Flask(' in content:
                    return 'flask'
                # Django
                if 'from django.urls import' in content or 'from rest_framework import' in content:
                    return 'django'
                # Express
                if "require('express')" in content or 'express()' in content:
                    return 'express'
                # NestJS
                if '@nestjs/common' in content:
                    return 'nestjs'
                # Spring Boot
                if '@Controller' in content or '@RestController' in content:
                    return 'spring'
                # Gin
                if 'github.com/gin-gonic/gin' in content:
                    return 'gin'
                # Echo
                if 'github.com/labstack/echo/v4' in content:
                    return 'echo'
                # React
                if 'import React' in content or "from 'react'" in content:
                    return 'react'
                # Vue
                if '<template>' in content or 'defineProps' in content:
                    return 'vue'
                # Angular
                if '@Component' in content or '@angular/core' in content:
                    return 'angular'
                # Svelte
                if '<script>' in content and 'lang="ts"' not in content:
                    return 'svelte'
                # Next.js
                if 'next/server' in content or 'pages/api/' in content:
                    return 'nextjs'
                # Nuxt.js
                if 'defineEventHandler' in content or 'server/api/' in content:
                    return 'nuxtjs'

        return 'unknown'

    def scan(self) -> List[Dict[str, Any]]:
        """扫描项目代码，提取 API 信息"""
        self.framework_detected = self.detect_framework()
        print(f"检测到框架: {self.framework_detected}")

        if self.framework_detected in ['flask', 'fastapi', 'django']:
            self._scan_python()
        elif self.framework_detected in ['express', 'nestjs']:
            self._scan_javascript()
        elif self.framework_detected == 'spring':
            self._scan_java()
        elif self.framework_detected in ['gin', 'echo']:
            self._scan_go()
        elif self.framework_detected in ['react', 'vue', 'angular', 'svelte']:
            self._scan_frontend()
        elif self.framework_detected in ['nextjs', 'nuxtjs']:
            self._scan_api_routes()

        return self.endpoints

    def _scan_python(self):
        """扫描 Python 项目"""
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if not file.endswith('.py'):
                    continue

                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                if self.framework_detected == 'flask':
                    self._scan_flask(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'fastapi':
                    self._scan_fastapi(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'django':
                    self._scan_django(content, str(file_path.relative_to(self.project_dir)))

    def _scan_flask(self, content: str, file_path: str):
        """扫描 Flask 路由"""
        pattern = r'@app\.route\([\'"]([^\'"]+)[\'"]\s*,\s*methods=\[([^\]]+)\]\)'
        matches = re.findall(pattern, content)

        for match in matches:
            path, methods = match
            methods = [m.strip().strip("'\"") for m in methods.split(',')]
            for method in methods:
                self.endpoints.append({
                    'path': path,
                    'method': method,
                    'file': file_path,
                    'framework': 'flask'
                })

    def _scan_fastapi(self, content: str, file_path: str):
        """扫描 FastAPI 路由"""
        pattern = r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]\)'
        matches = re.findall(pattern, content)

        for match in matches:
            method, path = match
            self.endpoints.append({
                'path': path,
                'method': method.upper(),
                'file': file_path,
                'framework': 'fastapi'
            })

    def _scan_django(self, content: str, file_path: str):
        """扫描 Django 路由"""
        pattern = r'path\([\'"]([^\'"]+)[\'"]'
        matches = re.findall(pattern, content)

        for match in matches:
            path = match
            self.endpoints.append({
                'path': path,
                'method': 'GET',  # Django 默认使用 GET
                'file': file_path,
                'framework': 'django'
            })

    def _scan_javascript(self):
        """扫描 JavaScript/TypeScript 项目"""
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if not file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                    continue

                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                if self.framework_detected == 'express':
                    self._scan_express(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'nestjs':
                    self._scan_nestjs(content, str(file_path.relative_to(self.project_dir)))

    def _scan_express(self, content: str, file_path: str):
        """扫描 Express 路由"""
        pattern = r'app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'
        matches = re.findall(pattern, content)

        for match in matches:
            method, path = match
            self.endpoints.append({
                'path': path,
                'method': method.upper(),
                'file': file_path,
                'framework': 'express'
            })

    def _scan_nestjs(self, content: str, file_path: str):
        """扫描 NestJS 路由"""
        pattern = r'@(Get|Post|Put|Delete|Patch)\([\'"]([^\'"]*)[\'"]\)'
        matches = re.findall(pattern, content)

        for match in matches:
            method, path = match
            self.endpoints.append({
                'path': path,
                'method': method.upper(),
                'file': file_path,
                'framework': 'nestjs'
            })

    def _scan_java(self):
        """扫描 Java 项目"""
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if not file.endswith('.java'):
                    continue

                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                self._scan_spring(content, str(file_path.relative_to(self.project_dir)))

    def _scan_spring(self, content: str, file_path: str):
        """扫描 Spring Boot 路由"""
        pattern = r'@(Get|Post|Put|Delete|Patch)Mapping\([\'"]([^\'"]*)[\'"]\)'
        matches = re.findall(pattern, content)

        for match in matches:
            method, path = match
            self.endpoints.append({
                'path': path,
                'method': method.upper(),
                'file': file_path,
                'framework': 'spring'
            })

    def _scan_go(self):
        """扫描 Go 项目"""
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if not file.endswith('.go'):
                    continue

                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                if self.framework_detected == 'gin':
                    self._scan_gin(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'echo':
                    self._scan_echo(content, str(file_path.relative_to(self.project_dir)))

    def _scan_gin(self, content: str, file_path: str):
        """扫描 Gin 路由"""
        pattern = r'r\.(GET|POST|PUT|DELETE|PATCH)\([\'"]([^\'"]+)[\'"]'
        matches = re.findall(pattern, content)

        for match in matches:
            method, path = match
            self.endpoints.append({
                'path': path,
                'method': method.upper(),
                'file': file_path,
                'framework': 'gin'
            })

    def _scan_echo(self, content: str, file_path: str):
        """扫描 Echo 路由"""
        pattern = r'e\.(GET|POST|PUT|DELETE|PATCH)\([\'"]([^\'"]+)[\'"]'
        matches = re.findall(pattern, content)

        for match in matches:
            method, path = match
            self.endpoints.append({
                'path': path,
                'method': method.upper(),
                'file': file_path,
                'framework': 'echo'
            })

    def _scan_frontend(self):
        """扫描前端组件"""
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if not file.endswith(('.jsx', '.tsx', '.vue', '.svelte')):
                    continue

                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                if self.framework_detected == 'react':
                    self._scan_react_component(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'vue':
                    self._scan_vue_component(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'angular':
                    self._scan_angular_component(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'svelte':
                    self._scan_svelte_component(content, str(file_path.relative_to(self.project_dir)))

    def _scan_react_component(self, content: str, file_path: str):
        """扫描 React 组件"""
        pattern = r'(?:function|const)\s+(\w+)\s*(?:\([^)]*\))\s*(?:=>|\{)'
        matches = re.findall(pattern, content)

        for match in matches:
            component_name = match
            if component_name[0].isupper():
                self.endpoints.append({
                    'name': component_name,
                    'type': 'component',
                    'file': file_path,
                    'framework': 'react'
                })

    def _scan_vue_component(self, content: str, file_path: str):
        """扫描 Vue 组件"""
        pattern = r'name:\s*[\'"](\w+)[\'"]'
        matches = re.findall(pattern, content)

        for match in matches:
            component_name = match
            self.endpoints.append({
                'name': component_name,
                'type': 'component',
                'file': file_path,
                'framework': 'vue'
            })

    def _scan_angular_component(self, content: str, file_path: str):
        """扫描 Angular 组件"""
        pattern = r'@Component\(\{[^}]*selector:\s*[\'"]([^\'"]+)[\'"]'
        matches = re.findall(pattern, content)

        for match in matches:
            selector = match
            component_name = selector.replace('-', ' ').title().replace(' ', '')
            self.endpoints.append({
                'name': component_name,
                'type': 'component',
                'file': file_path,
                'framework': 'angular'
            })

    def _scan_svelte_component(self, content: str, file_path: str):
        """扫描 Svelte 组件"""
        component_name = file_path.split('/')[-1].replace('.svelte', '')
        self.endpoints.append({
            'name': component_name,
            'type': 'component',
            'file': file_path,
            'framework': 'svelte'
        })

    def _scan_api_routes(self):
        """扫描 API 路由（Next.js/Nuxt.js）"""
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if not file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                    continue

                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                except:
                    continue

                if self.framework_detected == 'nextjs':
                    self._scan_nextjs_route(content, str(file_path.relative_to(self.project_dir)))
                elif self.framework_detected == 'nuxtjs':
                    self._scan_nuxtjs_route(content, str(file_path.relative_to(self.project_dir)))

    def _scan_nextjs_route(self, content: str, file_path: str):
        """扫描 Next.js API 路由"""
        if 'export default function handler' in content or 'export async function' in content:
            path = file_path.replace('pages/api/', '').replace('\\', '/')
            self.endpoints.append({
                'path': '/' + path,
                'method': 'GET',
                'file': file_path,
                'framework': 'nextjs'
            })

    def _scan_nuxtjs_route(self, content: str, file_path: str):
        """扫描 Nuxt.js API 路由"""
        if 'export default defineEventHandler' in content:
            path = file_path.replace('server/api/', '').replace('\\', '/')
            self.endpoints.append({
                'path': '/' + path,
                'method': 'GET',
                'file': file_path,
                'framework': 'nuxtjs'
            })


def main():
    parser = argparse.ArgumentParser(description='API 扫描脚本')
    parser.add_argument('--project-dir', required=True, help='项目根目录')
    parser.add_argument('--framework', default='auto', help='框架类型（auto/flask/fastapi/express/django/nestjs/spring/gin/echo/react/vue/angular/svelte/nextjs/nuxtjs）')
    parser.add_argument('--output', default='api_scan_result.json', help='输出JSON文件路径')

    args = parser.parse_args()

    scanner = APIScanner(args.project_dir, args.framework)
    endpoints = scanner.scan()

    result = {
        'framework': scanner.framework_detected,
        'endpoints': endpoints
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"扫描完成，共发现 {len(endpoints)} 个端点/组件")
    print(f"结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
