#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Sten
# 仓库地址:https://github.com/aefa6/QinglongScript.git
# 请点击star支持作者
# 该脚本默认使用分片推送防止内容过长被截断
# 如需合并推送请修改第28-30行的注释

import requests
import notify

def fetch_60s_news():
    """获取60秒读懂世界内容"""
    url = 'https://60s.viki.moe/v2/60s?encoding=text'
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"获取新闻失败: {e}")
        return None

def split_content(content):
    """分割内容为两段"""
    pieces = content.split('\n', 10)
    return (
        '\n'.join(pieces[:10]) if pieces else "",
        '\n'.join(pieces[10:]) if len(pieces) > 10 else ""
    )

def send_notification(title, content):
    """发送通知（带错误处理）"""
    try:
        notify.send(title, content)
    except Exception as e:
        print(f"发送通知失败: {e}")

def main():
    # 获取新闻内容
    news_content = fetch_60s_news()
    if not news_content:
        print("未获取到新闻内容")
        return
    
    # 分片推送模式（默认）
    content1, content2 = split_content(news_content)
    
    #if content1 or content2:
        # 分片推送
        #send_notification("🌍 每天60s读懂世界 [1/2]", content1 + "\n\n")
        #if content2:
         #   send_notification("🌍 每天60s读懂世界 [2/2]", content2)
    
    # 整段推送模式（需要时取消下方注释）
     send_notification("🌍 每天60s读懂世界", news_content)

if __name__ == "__main__":
    main()
