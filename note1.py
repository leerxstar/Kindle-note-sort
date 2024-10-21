#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import re
from collections import defaultdict

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
        
        # 获取笔记的实际内容（从第三行开始）
        note_content = '\n'.join(lines[2:]).strip()  # 将剩下的部分视为笔记内容
        
        # 如果内容不为空，存储笔记
        if note_content:
            notes_by_book[book_title].append({
                'start_position': start_position,
                'end_position': end_position,
                'timestamp': timestamp,
                'content': note_content
            })

# 创建存储笔记的文件夹
output_dir = "kindle_notes_sorted"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 对每本书的笔记按位置排序并导出到新的文件夹
for book, notes in notes_by_book.items():
    notes.sort(key=lambda x: x['start_position'])  # 按起始位置排序
    
    # 导出为新文件，路径在新建的文件夹中
    output_file_path = os.path.join(output_dir, f"{book}_notes_sorted.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for index, note in enumerate(notes, start=1):
            output_file.write(f"标注 {index}:\n")
            output_file.write(f"位置 {note['start_position']}-{note['end_position']} | {note['timestamp']}\n")
            output_file.write(note['content'] + "\n\n")

print(f"所有笔记已导出到文件夹: {output_dir}")



# In[ ]:




