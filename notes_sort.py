#!/usr/bin/env python
# coding: utf-8

import os
import re
from collections import defaultdict
from datetime import datetime

# Define a dictionary to store notes for each book, where the key is the book title
notes_by_book = defaultdict(list)

# Regular expression to match book title, location info, time, and note content
note_pattern = re.compile(r"(.*) \((.*)\)\n- 您在位置 #(\d+)-?(\d+)?的标注 \| 添加于 (.*)")

# Read the My Clippings.txt file, handle BOM character
with open('My Clippings.txt', 'r', encoding='utf-8-sig') as file:
    content = file.read()

# Split different note entries
entries = content.split("==========\n")

# Process each note
for entry in entries:
    lines = entry.strip().split('\n')
    
    # Ensure the entry has at least 3 lines: book title, location info, and note content
    if len(lines) < 3:
        continue
    
    # Try to match the book title, location info, and timestamp
    match = note_pattern.match('\n'.join(lines[:2]))  # The first two lines should contain the book title and location info
    if match:
        book_title = match.group(1).strip() + " (" + match.group(2).strip() + ")"
        start_position = int(match.group(3))
        end_position = match.group(4)
        if end_position:
            end_position = int(end_position)
        else:
            end_position = start_position
        timestamp = match.group(5)
        
        # Replace Chinese "AM" and "PM" with their English equivalents
        if "上午" in timestamp:
            timestamp = timestamp.replace("上午", "AM")
        elif "下午" in timestamp:
            timestamp = timestamp.replace("下午", "PM")
        
       # Remove the Chinese day-of-week part
        timestamp = re.sub(r'星期.', '', timestamp)

        # Convert the time to a datetime object for sorting
        timestamp_dt = datetime.strptime(timestamp, '%Y年%m月%d日 %p%I:%M:%S')
        
        # Get the actual note content (starting from the third line)
        note_content = '\n'.join(lines[2:]).strip()  # Treat the rest as the note content
        
        # If the content is not empty, store the note
        if note_content:
            notes_by_book[book_title].append({
                'start_position': start_position,
                'end_position': end_position,
                'timestamp': timestamp,
                'timestamp_dt': timestamp_dt,  # Store the datetime object for sorting
                'content': note_content
            })

# Create a folder to store the sorted notes
output_dir = "kindle_notes_sorted"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Sort the notes for each book by position, and when positions are the same, by timestamp
for book, notes in notes_by_book.items():
for book, notes in notes_by_book.items():
    # Sort first by start_position, then by timestamp_dt
    notes.sort(key=lambda x: (x['start_position'], x['timestamp_dt']))
    
   # Export to a new file, with the path in the newly created folder
    output_file_path = os.path.join(output_dir, f"{book}_notes_sorted.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for index, note in enumerate(notes, start=1):
            output_file.write(f"标注 {index}:\n")
            output_file.write(f"位置 {note['start_position']}-{note['end_position']} | {note['timestamp']}\n")
            output_file.write(note['content'] + "\n\n")

print(f"所有笔记已导出到文件夹: {output_dir}")





