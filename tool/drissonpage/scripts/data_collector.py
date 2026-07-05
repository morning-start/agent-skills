#!/usr/bin/env python3
"""
数据采集脚本
演示如何使用 DrissionPage 采集网页数据
"""

from DrissionPage import Chromium, ChromiumOptions


def collect_table_data(url: str, table_selector: str = 'table'):
    """
    采集表格数据
    
    Args:
        url: 目标网页URL
        table_selector: 表格选择器
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        
        # 等待表格加载
        tab.wait.ele_visible(table_selector)
        
        # 获取表格
        table = tab.ele(table_selector)
        
        # 获取所有行
        rows = table.eles('tag:tr')
        
        data = []
        for row in rows:
            cells = row.eles('tag:td')
            if cells:
                row_data = [cell.text for cell in cells]
                data.append(row_data)
                print(' | '.join(row_data[:5]))  # 只显示前5列
        
        return data
        
    finally:
        browser.quit()


def collect_list_data(url: str, item_selector: str = 'div.item'):
    """
    采集列表数据
    
    Args:
        url: 目标网页URL
        item_selector: 列表项选择器
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        
        # 滚动加载更多内容
        for _ in range(3):
            tab.scroll.down(500)
            
        # 获取所有列表项
        items = tab.eles(item_selector)
        
        results = []
        for item in items:
            # 根据实际页面结构调整提取逻辑
            result = {
                'text': item.text[:100],  # 标题或文本
                'html': item.html[:200],   # HTML内容
            }
            results.append(result)
        
        print(f"共采集 {len(results)} 条数据")
        return results
        
    finally:
        browser.quit()


def collect_dynamic_page(url: str, scroll_count: int = 5):
    """
    采集动态加载页面（如无限滚动）
    
    Args:
        url: 目标网页URL
        scroll_count: 滚动次数
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        
        # 模拟滚动加载
        for i in range(scroll_count):
            tab.scroll.to_bottom()
            print(f"滚动第 {i+1} 次...")
            
        # 提取数据 - 根据实际页面调整选择器
        # 示例：提取所有文章标题
        articles = tab.eles('tag:article')
        
        results = []
        for article in articles:
            title = article.ele('tag:h2')
            if title:
                results.append({
                    'title': title.text,
                    'link': title.ele('tag:a').link if title.ele('tag:a') else None
                })
        
        print(f"共采集 {len(results)} 篇文章")
        for i, article in enumerate(results[:10], 1):
            print(f"{i}. {article['title']}")
        
        return results
        
    finally:
        browser.quit()


def collect_with_pagination(base_url: str, page_param: str = 'page', max_pages: int = 3):
    """
    带分页的数据采集
    
    Args:
        base_url: 基础URL
        page_param: 页码参数名
        max_pages: 最大页数
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    all_data = []
    
    try:
        for page in range(1, max_pages + 1):
            url = f"{base_url}?{page_param}={page}"
            print(f"\n采集第 {page} 页: {url}")
            
            tab.get(url)
            
            # 等待内容加载
            tab.wait(1)
            
            # 提取数据 - 根据实际页面调整
            items = tab.eles('.item')
            
            for item in items:
                data = {
                    'page': page,
                    'text': item.text[:100]
                }
                all_data.append(data)
            
            print(f"  本页 {len(items)} 条，总计 {len(all_data)} 条")
    
    finally:
        browser.quit()
    
    return all_data


if __name__ == '__main__':
    # 示例：采集测试页面
    # collect_table_data('https://example.com/table')
    # collect_list_data('https://example.com/list')
    # collect_dynamic_page('https://example.com/feed')
    
    print("请根据实际需求修改选择器和提取逻辑")
