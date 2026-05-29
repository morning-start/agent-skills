#!/usr/bin/env python3
"""
DrissionPage 快速启动脚本
用于验证 DrissionPage 环境并展示基本用法
"""

import sys
from pathlib import Path

def check_drissionpage():
    """检查 DrissionPage 是否已安装"""
    try:
        import DrissionPage
        print(f"✓ DrissionPage 已安装，版本: {DrissionPage.__version__}")
        return True
    except ImportError:
        print("✗ DrissionPage 未安装")
        print("  安装命令: pip install DrissionPage")
        return False

def quick_demo():
    """快速演示 DrissionPage 基本用法"""
    from DrissionPage import Chromium, ChromiumOptions

    print("\n=== DrissionPage 快速演示 ===\n")

    # 1. 创建配置对象
    print("1. 创建浏览器配置...")
    co = ChromiumOptions()
    co.headless(True)  # 无头模式
    co.mute(True)     # 静音
    
    # 2. 创建浏览器对象
    print("2. 连接浏览器...")
    browser = Chromium(addr_or_opts=co)
    
    # 3. 获取标签页
    print("3. 获取标签页...")
    tab = browser.latest_tab
    
    # 4. 访问网页
    print("4. 访问百度...")
    tab.get('https://www.baidu.com')
    print(f"   页面标题: {tab.title}")
    
    # 5. 查找元素
    print("5. 查找搜索框...")
    search_box = tab.ele('#kw')
    if search_box:
        print(f"   找到搜索框: {search_box.tag}")
        
        # 6. 输入文本
        print("6. 输入搜索内容...")
        search_box.input('DrissionPage')
        
        # 7. 点击搜索
        print("7. 点击搜索按钮...")
        tab.ele('#su').click()
        
        # 8. 获取结果
        print("8. 获取搜索结果...")
        import time
        time.sleep(1)
        results = tab.eles('tag:h3')
        print(f"   找到 {len(results)} 个结果")
        for i, r in enumerate(results[:5]):
            print(f"   {i+1}. {r.text[:50]}...")
    
    # 关闭浏览器
    print("\n9. 关闭浏览器...")
    browser.quit()
    print("✓ 演示完成!")

def demo_element_operations():
    """元素操作演示"""
    from DrissionPage import Chromium

    print("\n=== 元素操作演示 ===\n")

    browser = Chromium()
    tab = browser.latest_tab
    tab.get('https://www.baidu.com')

    # 查找元素的方式
    print("1. 元素查找方式:")
    print(f"   - ID查找: tab.ele('#kw')")
    print(f"   - 属性查找: tab.ele('@name=kw')")
    print(f"   - 文本查找: tab.ele('text=hao123')")
    print(f"   - 标签查找: tab.eles('tag:div')")

    # 获取当前页面的元素示例
    ele = tab.ele('#kw')
    if ele:
        print(f"\n2. 元素信息:")
        print(f"   - 标签: {ele.tag}")
        print(f"   - 文本: {ele.text}")
        print(f"   - 属性: {ele.attrs}")

    # 元素操作
    print("\n3. 元素操作:")
    print(f"   - 点击: ele.click()")
    print(f"   - 输入: ele.input('text')")
    print(f"   - 清空: ele.clear()")
    print(f"   - 获取焦点: ele.focus()")

    browser.quit()

def demo_session_page():
    """SessionPage 演示 - 无浏览器方式访问网页"""
    from DrissionPage import SessionPage

    print("\n=== SessionPage 演示 (无需浏览器) ===\n")

    page = SessionPage()
    page.get('https://httpbin.org/html')
    
    print(f"页面标题: {page.title}")
    print(f"页面URL: {page.url}")
    
    # 查找元素
    body = page.ele('tag:body')
    if body:
        print(f"Body文本前100字符: {body.text[:100]}...")
    
    print("\n特点:")
    print("  - 无需启动浏览器，性能更好")
    print("  - 适合静态页面数据采集")
    print("  - 使用 requests 库底层")

if __name__ == '__main__':
    if not check_drissionpage():
        sys.exit(1)
    
    # 运行演示
    try:
        quick_demo()
    except Exception as e:
        print(f"演示出错: {e}")
        print("这可能是由于无头模式或网络问题导致的")
