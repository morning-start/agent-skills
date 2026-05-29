#!/usr/bin/env python3
"""
图片下载工具
用于从URL下载图片并保存到本地
"""

import os
import sys
import argparse
import requests
from urllib.parse import urlparse
from pathlib import Path


def download_image(image_url: str, output_dir: str = "./downloaded_images") -> str:
    """
    从URL下载图片并保存到本地

    Args:
        image_url: 图片URL
        output_dir: 输出目录，默认为当前目录下的downloaded_images

    Returns:
        下载成功的图片本地路径

    Raises:
        Exception: 下载失败时抛出异常
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 从URL中提取文件名
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path)

    # 如果URL中没有文件名，使用时间戳生成
    if not filename or '.' not in filename:
        import time
        filename = f"image_{int(time.time())}.jpg"

    # 完整的保存路径
    save_path = output_path / filename

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': parsed_url.scheme + '://' + parsed_url.netloc
    }

    try:
        # 下载图片，禁用SSL验证（用于某些有证书问题的网站）
        response = requests.get(
            image_url,
            headers=headers,
            timeout=30,
            verify=False,
            allow_redirects=True
        )
        response.raise_for_status()

        # 检查是否为图片内容
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            raise Exception(f"URL返回的不是图片内容，Content-Type: {content_type}")

        # 保存图片
        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"图片下载成功: {save_path}")
        return str(save_path)

    except requests.exceptions.SSLError as e:
        raise Exception(f"SSL错误，无法下载图片: {str(e)}")
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"网络连接失败，请检查URL是否正确: {str(e)}")
    except requests.exceptions.Timeout as e:
        raise Exception(f"下载超时: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"下载图片失败: {str(e)}")
    except Exception as e:
        raise Exception(f"保存图片失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='从URL下载图片')
    parser.add_argument('--image-url', required=True, help='图片URL')
    parser.add_argument('--output-dir', default='./downloaded_images', help='输出目录（默认：./downloaded_images）')

    args = parser.parse_args()

    try:
        local_path = download_image(args.image_url, args.output_dir)
        print(f"SUCCESS:{local_path}")
    except Exception as e:
        print(f"ERROR:{str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
