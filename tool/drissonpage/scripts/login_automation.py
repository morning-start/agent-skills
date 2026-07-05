#!/usr/bin/env python3
"""
登录自动化脚本
演示如何使用 DrissionPage 处理各种登录场景
"""

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Keys
import time


def login_with_username_password(url: str, username: str, password: str, 
                                  username_selector: str = None, 
                                  password_selector: str = None,
                                  submit_selector: str = None):
    """
    使用用户名密码登录
    
    Args:
        url: 登录页面URL
        username: 用户名
        password: 密码
        username_selector: 用户名输入框选择器
        password_selector: 密码输入框选择器
        submit_selector: 提交按钮选择器
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 访问登录页
        tab.get(url)
        
        # 等待页面加载
        tab.wait(1)
        
        # 查找登录表单元素 - 自动检测或使用指定选择器
        if username_selector:
            user_input = tab.ele(username_selector)
        else:
            # 尝试自动查找
            user_input = tab.ele('@type=text') or tab.ele('@name*=user') or tab.ele('#username') or tab.ele('tag:input')
        
        if password_selector:
            pwd_input = tab.ele(password_selector)
        else:
            pwd_input = tab.ele('@type=password') or tab.ele('@name*=pass') or tab.ele('#password') or tab.ele('tag:input')
        
        if submit_selector:
            submit_btn = tab.ele(submit_selector)
        else:
            submit_btn = tab.ele('text=登录') or tab.ele('text=Sign in') or tab.ele('@type=submit') or tab.ele('tag:button')
        
        if not all([user_input, pwd_input, submit_btn]):
            print("未找到登录表单元素，请检查选择器")
            return False
        
        # 输入用户名
        user_input.input(username)
        print(f"✓ 输入用户名: {username}")
        
        # 输入密码
        pwd_input.input(password)
        print("✓ 输入密码")
        
        # 点击登录按钮
        submit_btn.click()
        print("✓ 点击登录按钮")
        
        # 等待登录结果
        time.sleep(2)
        
        # 检查是否登录成功（根据实际页面调整）
        current_url = tab.url
        if 'login' not in current_url.lower():
            print(f"✓ 登录成功，当前URL: {current_url}")
            return True
        else:
            print("✗ 登录可能失败，仍在登录页面")
            return False
            
    except Exception as e:
        print(f"登录过程出错: {e}")
        return False
        
    finally:
        browser.quit()


def login_with_verification(url: str, username: str, password: str):
    """
    处理需要验证码的登录
    
    Args:
        url: 登录页面URL
        username: 用户名
        password: 密码
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        tab.wait(1)
        
        # 输入账号密码
        tab.ele('@name=username').input(username)
        tab.ele('@name=password').input(password)
        
        # 点击登录
        tab.ele('tag:button').click()
        
        # 等待验证码输入
        print("请在浏览器中手动输入验证码...")
        print("输入完成后按回车继续...")
        input()
        
        # 等待登录结果
        time.sleep(2)
        
        return True
        
    finally:
        browser.quit()


def login_with_slider(url: str, username: str, password: str):
    """
    处理滑块验证的登录
    
    Args:
        url: 登录页面URL
        username: 用户名
        password: 密码
    """
    from DrissionPage import ChromiumPage
    
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        tab.get(url)
        tab.wait(1)
        
        # 输入账号密码
        tab.ele('@name=username').input(username)
        tab.ele('@name=password').input(password)
        
        # 查找滑块按钮
        slider = tab.ele('.slider-button') or tab.ele('text=向右滑动')
        
        if slider:
            # 拖动滑块
            slider.drag_to((300, 0), duration=1)
            print("✓ 拖动滑块完成")
        
        # 点击登录
        tab.ele('tag:button').click()
        
        time.sleep(2)
        
        return True
        
    finally:
        browser.quit()


def handle_cookie_login(url: str, cookies: dict):
    """
    使用 Cookie 登录
    
    Args:
        url: 目标网站URL
        cookies: Cookie 字典
    """
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 先访问网站
        tab.get(url)
        
        # 设置 Cookie
        for name, value in cookies.items():
            tab.set.cookies({name: value})
        
        print(f"✓ 已设置 {len(cookies)} 个 Cookie")
        
        # 刷新页面使 Cookie 生效
        tab.get(url)
        
        return True
        
    finally:
        browser.quit()


def save_session(url: str, save_path: str):
    """
    保存登录后的会话
    
    Args:
        url: 登录页面URL
        save_path: 保存路径
    """
    import json
    
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 访问网站（此时应该已登录）
        tab.get(url)
        
        # 获取 cookies
        cookies = tab.cookies()
        
        # 保存到文件
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"✓ 会话已保存到: {save_path}")
        return True
        
    finally:
        browser.quit()


def load_session(url: str, save_path: str):
    """
    加载保存的会话
    
    Args:
        url: 目标网站URL
        save_path: 保存路径
    """
    import json
    
    co = ChromiumOptions()
    co.headless(True)
    co.mute(True)
    
    browser = Chromium(addr_or_opts=co)
    tab = browser.latest_tab
    
    try:
        # 读取保存的 cookies
        with open(save_path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        # 访问网站
        tab.get(url)
        
        # 设置 cookies
        for cookie in cookies:
            tab.set.cookies(cookie)
        
        print(f"✓ 已加载 {len(cookies)} 个 Cookie")
        
        # 刷新页面
        tab.get(url)
        
        return True
        
    finally:
        browser.quit()


if __name__ == '__main__':
    # 示例用法
    # login_with_username_password(
    #     url='https://example.com/login',
    #     username='testuser',
    #     password='testpass',
    #     username_selector='#username',
    #     password_selector='#password',
    #     submit_selector='button[type=submit]'
    # )
    
    print("请根据实际需求修改登录逻辑")
