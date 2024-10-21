#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import re
from collections import defaultdict
from datetime import datetime

# 定义一个字典来存储每本书的笔记，键为书名
notes_by_book = defaultdict(list)

# 正则表达式匹配书名、位置信息、时间和标注内容
note_pattern = re.compile(r"(.*) \((.*)\)\n- 您在位置 #(\d+)-?(\d+)?的标注 \| 添加于 (.*)")

# 读取 My Clippings.txt 文件，处理 BOM 字符
with open('My Clippings.txt', 'r', encoding='utf-8-sig') as file:
    content = file.read()

# 分割不同的笔记条目
entries = content.split("==========\n")

# 处理每条笔记
for entry in entries:
    lines = entry.strip().split('\n')
    
    # 确保条目有至少 3 行：书名、位置信息、笔记内容
    if len(lines) < 3:
        continue
    
    # 尝试匹配书名、位置信息和时间
    match = note_pattern.match('\n'.join(lines[:2]))  # 前两行应该包含书名和位置信息
    if match:
        book_title = match.group(1).strip() + " (" + match.group(2).strip() + ")"
        start_position = int(match.group(3))
        end_position = match.group(4)
        if end_position:
            end_position = int(end_position)
        else:
            end_position = start_position
        timestamp = match.group(5)
        
        # 将时间中的 "上午" 和 "下午" 替换为 AM 和 PM
        if "上午" in timestamp:
            timestamp = timestamp.replace("上午", "AM")
        elif "下午" in timestamp:
            timestamp = timestamp.replace("下午", "PM")
        
        # 去掉中文的星期部分
        timestamp = re.sub(r'星期.', '', timestamp)

        # 将时间转换为 datetime 对象以便排序
        timestamp_dt = datetime.strptime(timestamp, '%Y年%m月%d日 %p%I:%M:%S')
        
        # 获取笔记的实际内容（从第三行开始）
        note_content = '\n'.join(lines[2:]).strip()  # 将剩下的部分视为笔记内容
        
        # 如果内容不为空，存储笔记
        if note_content:
            notes_by_book[book_title].append({
                'start_position': start_position,
                'end_position': end_position,
                'timestamp': timestamp,
                'timestamp_dt': timestamp_dt,  # 存储 datetime 对象用于排序
                'content': note_content
            })

# 创建存储笔记的文件夹
output_dir = "kindle_notes_sorted"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 对每本书的笔记按位置排序，并在位置相同时按时间排序
for book, notes in notes_by_book.items():
    # 先按 start_position 排序，再按 timestamp_dt 排序
    notes.sort(key=lambda x: (x['start_position'], x['timestamp_dt']))
    
    # 导出为新文件，路径在新建的文件夹中
    output_file_path = os.path.join(output_dir, f"{book}_notes_sorted.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for index, note in enumerate(notes, start=1):
            output_file.write(f"标注 {index}:\n")
            output_file.write(f"位置 {note['start_position']}-{note['end_position']} | {note['timestamp']}\n")
            output_file.write(note['content'] + "\n\n")

print(f"所有笔记已导出到文件夹: {output_dir}")


# In[ ]:




