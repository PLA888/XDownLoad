import os
import requests
import bs4
from tqdm import tqdm
from pathlib import Path
import time
import tkinter as tk
from tkinter import messagebox
import re

def download_video(video_url, output_file_name) -> None:
    response = requests.get(video_url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    download_path = os.path.join(os.getcwd(), output_file_name)

    with open(download_path, "wb") as video_file:
        for data_chunk in response.iter_content(block_size):
            progress_bar.update(len(data_chunk))
            video_file.write(data_chunk)

    progress_bar.close()
    print("视频成功下载！")
    print("视频保存路径：" + download_path)
    return download_path

def extract_tweet_id(url):
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("无法从URL中提取Tweet ID")

def download_twitter_video(twitter_post_url):
    try:
        tweet_id = extract_tweet_id(twitter_post_url)
        api_request_url = f"https://twitsave.com/info?url={twitter_post_url}"
        response = requests.get(api_request_url)
        page_content = bs4.BeautifulSoup(response.text, "html.parser")
        download_section = page_content.find_all("div", class_="origin-top-right")[0]
        quality_links = download_section.find_all("a")
        highest_quality_video_url = quality_links[0].get("href")

        video_file_name = f"{tweet_id}.mp4"
        
        download_path = download_video(highest_quality_video_url, video_file_name)
        messagebox.showinfo("下载完成", f"视频已成功下载至: {download_path}")
    except Exception as e:
        messagebox.showerror("错误", f"下载失败: {e}")

def on_download_button_click():
    url = entry.get()
    if not url:
        messagebox.showwarning("输入错误", "请输入有效的Twitter帖子URL")
        return
    download_twitter_video(url)

# 创建主窗口
root = tk.Tk()
root.title("Twitter Video Downloader")
root.geometry("400x150")

# 创建并放置标签
label = tk.Label(root, text="请输入Twitter帖子URL:")
label.pack(pady=10)

# 创建并放置输入框
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# 创建并放置下载按钮
download_button = tk.Button(root, text="下载视频", command=on_download_button_click)
download_button.pack(pady=20)

# 运行主循环
root.mainloop()