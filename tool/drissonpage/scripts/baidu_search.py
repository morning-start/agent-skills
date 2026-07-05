#!/usr/bin/env python3
"""
百度搜索自动化脚本
演示 DrissionPage 的基本搜索功能
"""

import sys
from DrissionPage import Chromium, ChromiumOptions


def search_baidu(keyword: str, headless: bool = True):
    """
    在百度搜索指定关键词
    
    Args:
        keyword: 搜索关键词
        headless: 是否使用无头模式
    """
    # 创建配置
    co = ChromiumOptions()
    co.headless(headless)
    co.mute(True)
    co.set_timeouts(base=10)
    
    try:
        # 启动浏览器
        browser = Chromium(addr_or_opts=co)
        tab = browser.latest_tab
        
        # 访问百度
        tab.get('https://www.baidu.com')
        
        # 查找搜索框并输入
        search_box = tab.ele('#kw')
        search_box.input(keyword)
        
        # 点击搜索按钮
        tab.ele('#su').click()
        
        # 等待结果加载
        import time
        time.sleep(2)
        
        # 获取搜索结果
        results = tab.eles('tag:h3')
        
        print(f"\n搜索 '{keyword}' 的结果 (前10条):")
        print("-" * 50)
        for i, result in enumerate(results[:10], 1):
            try:
                # 尝试获取链接
                link = result.ele('tag:a')
                if link:
                    print(f"{i}. {result.text[:60]}")
                    print(f"   URL: {link.link}")
            except:
                print(f"{i}. {result.text[:60]}")
        
        return True
        
    except Exception as e:
        print(f"搜索失败: {e}")
        return False
        
    finally:
        browser.quit()


def batch_search(keywords: list, headless: bool = True):
    """
    批量搜索多个关键词
    
    Args:
        keywords: 关键词列表
        headless: 是否使用无头模式
    """
    co = ChromiumOptions()
    co.headless(headless)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        for keyword in keywords:
            print(f"\n搜索: {keyword}")
            
            # 访问百度
            tab.get('https://www.baidu.com')
            
            # 输入并搜索
            tab.ele('#kw').input(keyword)
            tab.ele('#su').click()
            
            # 等待结果
            import time
            time.sleep(1)
            
            # 获取结果数量
            results = tab.eles('tag:h3')
            print(f"  找到 {len(results)} 个结果")
    
    finally:
        browser.quit()


if __name__ == '__main__':
    # 单次搜索
    search_baidu('DrissionPage')
    
    # 批量搜索示例
    # batch_search(['Python', '自动化测试', '网页抓取'])
