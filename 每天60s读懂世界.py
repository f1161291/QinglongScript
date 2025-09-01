#!/usr/bin/env python3
# @author Sten
# 仓库地址:https://github.com/aefa6/QinglongScript.git
import os
import requests
from requests.exceptions import RequestException
import notify

# 配置区域 ==============================================
NOTIFY_TITLE = "每天60s读懂世界"  # 推送标题
API_URL = "https://60s.viki.moe/v2/60s?encoding=text"
TIMEOUT = 15  # 请求超时时间(秒)
MAX_RETRY = 2  # 最大重试次数
SPLIT_LENGTH = 500  # 分片长度(字符)
# ======================================================

def get_60s_news(retry_count=0):
    """获取60秒新闻内容"""
    try:
        resp = requests.get(API_URL, timeout=TIMEOUT)
        resp.raise_for_status()
        content = resp.text.strip()
        if not content:
            raise ValueError("响应内容为空")
        return content
    except RequestException as e:
        if retry_count < MAX_RETRY:
            print(f"请求失败，正在重试({retry_count+1}/{MAX_RETRY})...")
            return get_60s_news(retry_count + 1)
        raise RuntimeError(f"接口请求失败: {str(e)}") from e

def split_content(content, max_length=SPLIT_LENGTH):
    """智能分片内容"""
    if len(content) <= max_length:
        return [content]
    
    # 尝试按换行符分片
    pieces = []
    current = []
    current_length = 0
    
    for line in content.split('\n'):
        line_length = len(line) + 1  # 包含换行符
        if current_length + line_length > max_length:
            pieces.append('\n'.join(current))
            current = [line]
            current_length = line_length
        else:
            current.append(line)
            current_length += line_length
    
    if current:
        pieces.append('\n'.join(current))
    
    # 如果仍然过长则强制分片
    final_pieces = []
    for piece in pieces:
        if len(piece) > max_length:
            final_pieces.extend([piece[i:i+max_length] for i in range(0, len(piece), max_length)])
        else:
            final_pieces.append(piece)
    
    return final_pieces

def main():
    print("开始获取每日新闻...")
    try:
        content = get_60s_news()
        print("内容获取成功，准备推送")
        
        # 分片处理
        pieces = split_content(content)
        print(f"内容分片完成，共 {len(pieces)} 个片段")
        
        # 发送通知
        for i, piece in enumerate(pieces, 1):
            msg = f"{piece}\n\n[{i}/{len(pieces)}]" if len(pieces) > 1 else piece
            notify.send(NOTIFY_TITLE, msg)
            print(f"第 {i} 段推送已发送")
            
        print("所有通知发送完成")
    except Exception as e:
        error_msg = f"❌ 任务执行失败: {str(e)}"
        print(error_msg)
        notify.send("新闻推送异常", error_msg)

if __name__ == "__main__":
    main()
