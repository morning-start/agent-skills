#!/usr/bin/env python3
"""
批量创建 DrissionPage 相关技能
基于文档自动生成技能结构
"""

import json
import os
from pathlib import Path


SKILL_TEMPLATE = """# {skill_name}

## 技能概述

{description}

## 核心功能

{full_name} 是 DrissionPage 框架的重要组成部分，主要用于 {purpose}。

## 使用方法

### 基础用法

```python
{basic_code}
```

### 常用 API

| API | 说明 |
|-----|------|
{api_table}

## 示例代码

```python
{examples}
```

## 注意事项

{notes}
"""


SUB_SKILLS = [
    {
        "name": "browser-control",
        "full_name": "浏览器控制",
        "description": "浏览器连接、启动、配置和管理技能",
        "purpose": "连接和管理浏览器实例",
        "basic_code": '''from DrissionPage import Chromium, ChromiumOptions

# 创建浏览器
browser = Chromium()

# 使用配置
co = ChromiumOptions()
co.headless(True).mute(True)
browser = Chromium(co)

# 获取标签页
tab = browser.latest_tab
tab.get('https://example.com')

# 关闭浏览器
browser.quit()''',
        "api_table": """| latest_tab | 获取当前标签页 |
| new_tab(url) | 新建标签页 |
| quit() | 关闭浏览器 |
| tabs() | 获取所有标签页 |""",
        "examples": """# 无头模式
co = ChromiumOptions()
co.headless(True)
browser = Chromium(co)

# 多标签页管理
tab1 = browser.new_tab('https://a.com')
tab2 = browser.new_tab('https://b.com')
tab1.get('https://c.com')""",
        "notes": "1. 程序结束时浏览器不会自动关闭\n2. 同一浏览器只能有一个 Chromium 对象\n3. 多个浏览器需要不同端口"
    },
    {
        "name": "element-locator",
        "full_name": "元素定位",
        "description": "网页元素定位和查找技能",
        "purpose": "快速准确地定位网页元素",
        "basic_code": '''from DrissionPage import Chromium

tab = Chromium().latest_tab
tab.get('https://example.com')

# 各种定位方式
ele = tab.ele('#id')           # ID定位
ele = tab.ele('@name=value')   # 属性定位
ele = tab.ele('text=文本')     # 文本定位
ele = tab.ele('tag:div')       # 标签定位
eles = tab.eles('tag:a')       # 获取多个''',
        "api_table": """| ele(locator) | 查找单个元素 |
| eles(locator) | 查找多个元素 |
| wait.ele_visible() | 等待元素可见 |
| wait.ele_enabled() | 等待元素可用 |""",
        "examples": """# 相对定位
container = tab.ele('.container')
item = container.ele('tag:li')

# 链式查找
tab.ele('#form')('tag:input').click()

# 筛选
eles = tab.eles('tag:a')
visible_links = [e for e in eles if e.displayed]""",
        "notes": "1. 优先使用稳定属性定位\n2. 避免使用绝对路径\n3. 结合相对定位提高鲁棒性"
    },
    {
        "name": "element-operation",
        "full_name": "元素交互",
        "description": "元素点击、输入、拖拽等交互操作",
        "purpose": "模拟用户与网页元素的交互",
        "basic_code": '''from DrissionPage import Chromium

tab = Chromium().latest_tab
tab.get('https://example.com')

# 点击
tab.ele('#btn').click()

# 输入
tab.ele('#input').input('text')

# 拖拽
ele = tab.ele('#drag')
ele.drag(100, 100)''',
        "api_table": """| click() | 点击 |
| input(text) | 输入文本 |
| clear() | 清空 |
| drag(offset_x, offset_y) | 拖拽 |
| hover() | 悬停 |
| select.by_text() | 下拉选择 |""",
        "examples": """# 模拟点击(被遮挡时用JS)
ele.click(by_js=True)

# 带偏移点击
ele.click.at(10, 10)

# 右键菜单
ele.click.right()

# 拖拽到目标
target = tab.ele('#target')
ele.drag_to(target)""",
        "notes": "1. 注意元素是否在视口内\n2. 复杂操作考虑使用动作链\n3. 登录场景注意验证码处理"
    },
    {
        "name": "session-page",
        "full_name": "SessionPage",
        "description": "无需浏览器的网页访问方式",
        "purpose": "使用数据包方式高效访问网页",
        "basic_code": '''from DrissionPage import SessionPage

page = SessionPage()
page.get('https://example.com')

# 查找元素
title = page.ele('tag:h1')
items = page.eles('tag:li')

# 获取信息
print(page.title)
print(page.url)''',
        "api_table": """| get(url) | 访问URL |
| ele(locator) | 查找元素 |
| eles(locator) | 查找多个 |
| title | 页面标题 |
| url | 当前URL |
| html | 页面HTML |""",
        "examples": """# POST请求
page.post('https://api.example.com', data={'key': 'value'})

# 带参数
page.get('https://api.com', params={'page': 1})

# 设置请求头
page.headers.update({'Authorization': 'Bearer xxx'})""",
        "notes": "1. 无需启动浏览器，性能更好\n2. 适合静态页面\n3. 无法处理JavaScript渲染的内容"
    },
    {
        "name": "network-listener",
        "full_name": "网络监听",
        "description": "监听和拦截网络请求",
        "purpose": "分析网络流量和API调用",
        "basic_code": '''from DrissionPage import Chromium

tab = Chromium().latest_tab
tab.get('https://example.com')

# 开始监听
tab.listen.start('api.example.com')

# 等待请求
packet = tab.listen.wait()
print(packet.request.url)
print(packet.response.body)

# 停止监听
tab.listen.stop()''',
        "api_table": """| listen.start(domain) | 开始监听 |
| listen.wait() | 等待数据包 |
| listen.steps() | 获取已捕获数据包 |
| listen.stop() | 停止监听 |""",
        "examples": """# 监听多种类型
tab.listen.start('example.com', type='xhr')

# 获取所有捕获的包
tab.listen.start()
# ... 执行操作 ...
packets = tab.listen.steps()
for p in packets:
    print(p.request.url)""",
        "notes": "1. 可用于分析API接口\n2. 方便获取Ajax数据\n3. 支持请求和响应内容获取"
    },
    {
        "name": "download-manager",
        "full_name": "下载管理",
        "description": "文件下载功能",
        "purpose": "处理网页文件下载",
        "basic_code": '''from DrissionPage import Chromium, ChromiumOptions

# 配置下载路径
co = ChromiumOptions()
co.set_download_path('./downloads')

browser = Chromium(co)
tab = browser.latest_tab
tab.get('https://example.com')

# 点击下载
mission = tab.ele('#download').click.to_download()
print(mission.state)''',
        "api_table": """| click.to_download() | 点击下载 |
| set_download_path() | 设置路径 |
| DownloadMission | 下载任务对象 |""",
        "examples": """# 带重命名
mission = ele.click.to_download(
    save_path='./downloads',
    rename='file.pdf'
)

# 等待下载完成
mission.wait()
print(mission.state)""",
        "notes": "1. 无头模式需要额外配置\n2. 注意下载路径权限\n3. 大文件考虑分块下载"
    }
]


def create_sub_skill(skill_info: dict, base_path: Path):
    """创建子技能"""
    skill_path = base_path / skill_info["name"]
    skill_path.mkdir(parents=True, exist_ok=True)
    
    content = SKILL_TEMPLATE.format(
        skill_name=skill_info["full_name"],
        description=skill_info["description"],
        full_name=skill_info["full_name"],
        purpose=skill_info["purpose"],
        basic_code=skill_info["basic_code"],
        api_table=skill_info["api_table"],
        examples=skill_info["examples"],
        notes=skill_info["notes"]
    )
    
    (skill_path / "SKILL.md").write_text(content, encoding='utf-8')
    print(f"✓ 创建技能: {skill_info['full_name']}")


def create_all_skills(base_path: str = None):
    """创建所有子技能"""
    if base_path is None:
        base_path = Path(__file__).parent
    
    base_path = Path(base_path)
    
    # 创建主技能目录
    main_skill_path = base_path / "drissionpage-modules"
    main_skill_path.mkdir(parents=True, exist_ok=True)
    
    print("批量创建 DrissionPage 子技能...")
    print("-" * 40)
    
    for skill in SUB_SKILLS:
        create_sub_skill(skill, main_skill_path)
    
    print("-" * 40)
    print(f"✓ 已创建 {len(SUB_SKILLS)} 个子技能")
    print(f"  位置: {main_skill_path}")


if __name__ == '__main__':
    create_all_skills()
