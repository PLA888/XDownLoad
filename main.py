import os
import requests
import bs4
from tqdm import tqdm
from pathlib import Path
import time

# 定义一个函数，用于下载视频
def download_video(video_url, output_file_name) -> None:
    """
    从指定的URL下载视频到本地。

    参数:
        video_url (str): 要下载的视频的URL。
        output_file_name (str): 保存视频的文件名或路径。
    """

    # 发起请求，获取响应
    response = requests.get(video_url, stream=True)
    # 获取内容的总大小
    total_size = int(response.headers.get("content-length", 0))
    # 设置块大小
    block_size = 1024
    # 初始化进度条
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    # 使用当前运行路径为下载路径
    download_path = os.path.join(os.getcwd(), output_file_name)

    # 以二进制写模式打开文件
    with open(download_path, "wb") as video_file:
        for data_chunk in response.iter_content(block_size):
            progress_bar.update(len(data_chunk))
            video_file.write(data_chunk)

    # 关闭进度条
    progress_bar.close()
    print("视频成功下载！")
    print("视频保存路径：" + download_path)

# 定义一个函数，用于下载Twitter视频
def download_twitter_video(twitter_post_url):
    """
    提取并下载Twitter帖子中的最高质量视频。

    参数:
        twitter_post_url (str): Twitter帖子URL。
    """

    # 构建API URL
    api_request_url = f"https://twitsave.com/info?url={twitter_post_url}"

    # 发起请求，获取响应
    response = requests.get(api_request_url)
    page_content = bs4.BeautifulSoup(response.text, "html.parser")
    # 查找下载按钮
    download_section = page_content.find_all("div", class_="origin-top-right")[0]
    # 查找质量选择按钮
    quality_links = download_section.find_all("a")
    # 获取最高质量视频的URL
    highest_quality_video_url = quality_links[0].get("href")
    
    # 使用时间戳生成视频文件名
    timestamp = int(time.time())
    video_file_name = f"{timestamp}.mp4"
    
    # 调用下载视频函数
    download_video(highest_quality_video_url, video_file_name)

def main():
    download_twitter_video("https://x.com/Morris_LT/status/1864475885023400122")

if __name__ == "__main__":
    main()
