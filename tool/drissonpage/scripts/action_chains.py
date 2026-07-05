#!/usr/bin/env python3
"""
高级动作链脚本
演示复杂的鼠标和键盘操作
"""

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Actions, Keys
import time


def drag_and_drop_demo():
    """
    演示拖拽操作
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 访问拖拽测试页面
        tab.get('https://jqueryui.com/resources/demos/draggable/default.html')
        
        # 获取拖拽元素
        draggable = tab.ele('#draggable')
        
        # 拖拽到新位置
        draggable.drag(200, 100)
        print("✓ 拖拽完成")
        
        # 使用动作链拖拽
        tab.actions.hold('#draggable')
        tab.actions.move(100, 50)
        tab.actions.release()
        print("✓ 动作链拖拽完成")
        
    finally:
        browser.quit()


def simulate_human_typing(url: str, input_selector: str, text: str):
    """
    模拟人类输入（逐字符输入）
    
    Args:
        url: 页面URL
        input_selector: 输入框选择器
        text: 要输入的文本
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        
        # 点击使输入框获取焦点
        tab.ele(input_selector).click()
        
        # 逐字符输入（模拟人类）
        for char in text:
            tab.actions.type(char)
            time.sleep(0.1)  # 随机延迟
        
        print(f"✓ 输入完成: {text}")
        
    finally:
        browser.quit()


def keyboard_shortcut_demo():
    """
    演示键盘快捷键操作
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get('https://www.baidu.com')
        
        # 获取搜索框
        search_box = tab.ele('#kw')
        search_box.click()
        
        # 输入文本
        search_box.input('test')
        
        # 全选
        tab.actions.key_down(Keys.CTRL)
        tab.actions.type('a')
        tab.actions.key_up(Keys.CTRL)
        
        # 删除
        tab.actions.key_down(Keys.DELETE)
        
        # 输入新内容
        tab.actions.type('DrissionPage')
        
        print("✓ 快捷键操作完成")
        
    finally:
        browser.quit()


def mouse_gesture_demo():
    """
    演示鼠标手势操作
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get('https://example.com')
        
        # 移动到元素
        tab.actions.move_to('tag:h1')
        
        # 移动到坐标
        tab.actions.move(100, 50)
        
        # 绘制简单的手势（Z字形）
        tab.actions.move_to((100, 100))
        tab.actions.down(50)
        tab.actions.right(100)
        tab.actions.up(50)
        tab.actions.right(100)
        
        print("✓ 鼠标手势完成")
        
    finally:
        browser.quit()


def scroll_page_demo():
    """
    演示页面滚动操作
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get('https://example.com')
        
        # 滚动到页面底部
        tab.actions.scroll(0, 1000)
        
        # 滚动到页面顶部
        tab.actions.scroll(0, -1000)
        
        # 平滑滚动
        for _ in range(10):
            tab.actions.scroll(0, 100)
            time.sleep(0.1)
        
        print("✓ 滚动操作完成")
        
    finally:
        browser.quit()


def hover_menu_demo(url: str, menu_selector: str, item_selector: str):
    """
    演示悬停菜单操作
    
    Args:
        url: 页面URL
        menu_selector: 菜单选择器
        item_selector: 菜单项选择器
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        
        # 悬停到菜单
        menu = tab.ele(menu_selector)
        menu.hover()
        
        # 等待子菜单出现
        tab.wait.ele_displayed(item_selector)
        
        # 点击菜单项
        tab.ele(item_selector).click()
        
        print("✓ 菜单操作完成")
        
    finally:
        browser.quit()


def complex_action_chain():
    """
    复杂动作链演示：模拟完整的数据录入流程
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 假设这是一个表单页面
        tab.get('https://example.com/form')
        
        # 完整动作链：填写表单
        (
            tab.actions
            # 移动到第一个输入框
            .move_to('#name')
            .click()
            # 输入姓名
            .type('张三')
            # 移动到下一个输入框
            .move_to('#email')
            .click()
            # 输入邮箱
            .type('zhangsan@example.com')
            # 移动到提交按钮
            .move_to('#submit')
            .click()
        )
        
        print("✓ 表单填写完成")
        
    finally:
        browser.quit()


def double_click_demo():
    """
    演示双击操作
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get('https://example.com')
        
        # 双击
        ele = tab.ele('#element')
        ele.click.multi(2)
        
        # 或使用动作链
        tab.actions.click('#element').click()
        
        print("✓ 双击操作完成")
        
    finally:
        browser.quit()


def right_click_context_menu():
    """
    演示右键点击（打开上下文菜单）
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get('https://example.com')
        
        # 右键点击
        tab.actions.r_click('#element')
        
        # 等待菜单出现
        tab.wait.ele_displayed('.context-menu')
        
        # 点击菜单项
        tab.ele('text=复制').click()
        
        print("✓ 右键菜单操作完成")
        
    finally:
        browser.quit()


def drag_file_to_browser():
    """
    演示拖拽文件到浏览器
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get('https://example.com/upload')
        
        # 拖入文件
        tab.actions.drag_in(
            '#dropzone',
            files=['D:/test.txt', 'D:/test.jpg']
        )
        
        print("✓ 文件拖入完成")
        
    finally:
        browser.quit()


if __name__ == '__main__':
    # 示例调用
    # drag_and_drop_demo()
    # simulate_human_typing('https://example.com', '#input', 'Hello World')
    # keyboard_shortcut_demo()
    # mouse_gesture_demo()
    # scroll_page_demo()
    
    print("请根据实际需求选择合适的函数调用")
