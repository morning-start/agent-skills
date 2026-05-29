#!/usr/bin/env python3
"""
批量爬取脚本
支持多URL批量爬取、数据提取和导出
"""

import json
from pathlib import Path
from DrissionPage import Chromium, ChromiumOptions
from tqdm import tqdm


class BatchCrawler:
    """批量爬取器"""
    
    def __init__(self, headless: bool = True):
        """
        初始化批量爬取器
        
        Args:
            headless: 是否使用无头模式
        """
        self.co = ChromiumOptions()
        self.co.headless(headless)
        self.co.mute(True)
        self.co.set_timeouts(base=30)
        self.browser = None
        self.tab = None
    
    def start(self):
        """启动浏览器"""
        self.browser = Chromium(addr_or_opts=self.co)
        self.tab = self.browser.latest_tab
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.quit()
    
    def visit_url(self, url: str, wait: float = 1.0):
        """
        访问URL
        
        Args:
            url: 目标URL
            wait: 等待秒数
        """
        import time
        self.tab.get(url)
        time.sleep(wait)
    
    def extract_data(self, selectors: dict) -> dict:
        """
        使用选择器提取数据
        
        Args:
            selectors: 选择器字典，格式: {'字段名': '选择器'}
        
        Returns:
            提取的数据字典
        """
        data = {}
        for field, selector in selectors.items():
            try:
                ele = self.tab.ele(selector)
                if ele:
                    data[field] = ele.text
                else:
                    data[field] = None
            except:
                data[field] = None
        return data
    
    def extract_list(self, item_selector: str, field_selectors: dict) -> list:
        """
        提取列表数据
        
        Args:
            item_selector: 列表项选择器
            field_selectors: 字段选择器字典
        
        Returns:
            数据列表
        """
        items = self.tab.eles(item_selector)
        results = []
        
        for item in items:
            data = {}
            for field, selector in field_selectors.items():
                try:
                    sub_ele = item.ele(selector)
                    data[field] = sub_ele.text if sub_ele else None
                except:
                    data[field] = None
            results.append(data)
        
        return results
    
    def scroll_and_load(self, times: int = 3, distance: int = 500):
        """
        滚动加载更多内容
        
        Args:
            times: 滚动次数
            distance: 每次滚动距离
        """
        for _ in range(times):
            self.tab.scroll.down(distance)
    
    def batch_crawl(self, urls: list, selectors: dict = None, 
                    output_file: str = None) -> list:
        """
        批量爬取
        
        Args:
            urls: URL列表
            selectors: 提取选择器
            output_file: 输出文件路径
        
        Returns:
            爬取结果列表
        """
        results = []
        
        try:
            self.start()
            
            with tqdm(total=len(urls), desc="爬取进度", unit="page") as pbar:
                for url in urls:
                    try:
                        self.visit_url(url)
                        
                        if selectors:
                            data = self.extract_data(selectors)
                            data['url'] = url
                            results.append(data)
                        else:
                            results.append({'url': url, 'html': self.tab.html})
                        
                        pbar.update(1)
                        
                    except Exception as e:
                        print(f"\n爬取失败 {url}: {e}")
                        results.append({'url': url, 'error': str(e)})
        
        finally:
            self.close()
        
        # 保存结果
        if output_file and results:
            self.save_results(results, output_file)
        
        return results
    
    def save_results(self, results: list, output_file: str):
        """
        保存结果到文件
        
        Args:
            results: 结果列表
            output_file: 输出文件路径
        """
        output_path = Path(output_file)
        suffix = output_path.suffix.lower()
        
        if suffix == '.json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        elif suffix == '.csv':
            import csv
            if results:
                keys = results[0].keys()
                with open(output_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(results)
        else:
            # 默认为 txt
            with open(output_file, 'w', encoding='utf-8') as f:
                for r in results:
                    f.write(json.dumps(r, ensure_ascii=False) + '\n')
        
        print(f"✓ 结果已保存到: {output_file}")


def crawl_with_config(config_file: str):
    """
    使用配置文件批量爬取
    
    Args:
        config_file: 配置文件路径 (JSON格式)
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    urls = config.get('urls', [])
    selectors = config.get('selectors', None)
    output_file = config.get('output', 'results.json')
    headless = config.get('headless', True)
    
    crawler = BatchCrawler(headless=headless)
    results = crawler.batch_crawl(urls, selectors, output_file)
    
    return results


if __name__ == '__main__':
    # 示例配置
    config = {
        'urls': [
            'https://example.com/page1',
            'https://example.com/page2',
        ],
        'selectors': {
            'title': 'tag:h1',
            'content': '.content',
            'author': '.author'
        },
        'output': 'results.json',
        'headless': True
    }
    
    # 保存配置
    with open('crawl_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 使用配置文件运行
    # crawl_with_config('crawl_config.json')
    
    # 或直接运行
    crawler = BatchCrawler(headless=True)
    
    # 添加URL列表
    urls = [
        'https://www.baidu.com',
        'https://www.google.com',
    ]
    
    # 定义提取选择器
    selectors = {
        'title': 'title',
        'description': 'meta[name=description]'
    }
    
    # 运行爬取
    # results = crawler.batch_crawl(urls, selectors, 'output.json')
