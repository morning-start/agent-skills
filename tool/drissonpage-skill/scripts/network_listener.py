#!/usr/bin/env python3
"""
网络监听脚本
演示如何使用 DrissionPage 监听和分析网络请求
"""

from DrissionPage import Chromium, ChromiumOptions
import json


def listen_and_capture(url: str, target_pattern: str = None):
    """
    监听网络请求并捕获数据
    
    Args:
        url: 目标URL
        target_pattern: 监听目标模式
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 设置监听目标
        target = target_pattern or 'api'
        tab.listen.start(target)
        
        # 访问页面
        tab.get(url)
        
        # 等待并捕获数据包
        packets = []
        for i in range(10):
            packet = tab.listen.wait(timeout=5)
            if packet:
                packets.append({
                    'url': packet.request.url,
                    'method': packet.request.method,
                    'status': packet.response.status,
                    'type': packet.resourceType
                })
                print(f"[{i+1}] {packet.request.method} {packet.request.url}")
            else:
                break
        
        return packets
        
    finally:
        tab.listen.stop()
        browser.quit()


def capture_api_data(url: str, action_selector: str, api_pattern: str):
    """
    捕获点击触发的 API 数据
    
    Args:
        url: 页面URL
        action_selector: 触发请求的元素选择器
        api_pattern: API 匹配模式
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 开始监听
        tab.listen.start(api_pattern)
        
        # 访问页面
        tab.get(url)
        
        # 触发动作
        action_ele = tab.ele(action_selector)
        if action_ele:
            action_ele.click()
        
        # 等待数据包
        packet = tab.listen.wait()
        
        if packet:
            # 解析响应
            response_body = packet.response.body
            
            print("请求信息:")
            print(f"  URL: {packet.request.url}")
            print(f"  方法: {packet.request.method}")
            
            if packet.request.postData:
                print(f"  POST数据: {packet.request.postData}")
            
            print("\n响应信息:")
            print(f"  状态码: {packet.response.status}")
            
            # 如果是 JSON
            if isinstance(response_body, dict):
                print(f"  数据: {json.dumps(response_body, indent=2, ensure_ascii=False)[:500]}")
            else:
                print(f"  数据: {str(response_body)[:500]}")
            
            return response_body
        
        return None
        
    finally:
        tab.listen.stop()
        browser.quit()


def capture_pagination_data(url: str, item_selector: str, next_selector: str, max_pages: int = 5):
    """
    捕获分页数据（结合网络监听和 DOM 提取）
    
    Args:
        url: 列表页URL
        item_selector: 列表项选择器
        next_selector: 下一页按钮选择器
        max_pages: 最大页数
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    all_data = []
    all_packets = []
    
    try:
        for page in range(1, max_pages + 1):
            print(f"\n=== 第 {page} 页 ===")
            
            # 访问页面
            tab.get(f"{url}?page={page}")
            
            # 监听 API 请求
            tab.listen.start('api', res_type='xhr')
            
            # 提取页面数据
            items = tab.eles(item_selector)
            page_data = []
            for item in items:
                try:
                    data = {
                        'text': item.text[:100] if item.text else '',
                        'html': item.html[:200] if item.html else ''
                    }
                    page_data.append(data)
                except:
                    pass
            
            print(f"  DOM提取: {len(page_data)} 条")
            all_data.extend(page_data)
            
            # 获取监听到的数据包
            packets = []
            for _ in range(5):
                packet = tab.listen.wait(timeout=2)
                if packet:
                    packets.append({
                        'url': packet.request.url,
                        'body': packet.response.body
                    })
            
            if packets:
                print(f"  API捕获: {len(packets)} 个请求")
                all_packets.extend(packets)
            
            # 检查是否有下一页
            next_btn = tab.ele(next_selector)
            if not next_btn or 'disabled' in next_btn.attrs.get('class', ''):
                print("  已到最后一页")
                break
        
        print(f"\n总计: DOM数据 {len(all_data)} 条, API请求 {len(all_packets)} 个")
        return {'items': all_data, 'packets': all_packets}
        
    finally:
        tab.listen.stop()
        browser.quit()


def analyze_api_requests(url: str, target_pattern: str):
    """
    分析 API 请求并提取关键信息
    
    Args:
        url: 目标URL
        target_pattern: 目标 API 模式
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.listen.start(target_pattern)
        tab.get(url)
        
        api_analysis = {
            'endpoints': set(),
            'methods': set(),
            'total_requests': 0
        }
        
        # 捕获所有匹配的请求
        while True:
            packet = tab.listen.wait(timeout=3)
            if not packet:
                break
            
            api_analysis['total_requests'] += 1
            api_analysis['endpoints'].add(packet.request.url)
            api_analysis['methods'].add(packet.request.method)
        
        print(f"API 分析结果:")
        print(f"  总请求数: {api_analysis['total_requests']}")
        print(f"  端点数: {len(api_analysis['endpoints'])}")
        print(f"  请求方法: {api_analysis['methods']}")
        
        print("\n端点列表:")
        for endpoint in sorted(api_analysis['endpoints']):
            print(f"  - {endpoint}")
        
        return api_analysis
        
    finally:
        tab.listen.stop()
        browser.quit()


def get_json_api_data(url: str):
    """
    直接获取 JSON API 数据
    
    Args:
        url: API URL
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.listen.start(url)
        tab.get(url)
        
        packet = tab.listen.wait()
        
        if packet and packet.response.body:
            return packet.response.body
        
        return None
        
    finally:
        tab.listen.stop()
        browser.quit()


if __name__ == '__main__':
    # 示例用法
    # 监听请求
    # listen_and_capture('https://example.com')
    
    # 捕获 API 数据
    # capture_api_data('https://example.com', '#load-btn', 'api/data')
    
    # 分页数据采集
    # result = capture_pagination_data('https://example.com/list', '.item', '.next')
    
    # 分析 API
    # analyze_api_requests('https://example.com', 'api.')
    
    print("请根据实际需求修改参数")
