#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按年份分层采样 arXiv 论文（2012-2026），每年每类别独立查询
"""

import urllib.request
import xml.etree.ElementTree as ET
import time
import os
from urllib.parse import urlencode

categories = ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV', 'stat.ML']
years = list(range(2012, 2027))   # 2012 到 2026
papers_per_slot = 100             # 每 (年份, 类别) 最多取 100 篇
output_file = 'arxiv_papers.txt'

base_url = 'http://export.arxiv.org/api/query'
all_papers = []

total_slots = len(years) * len(categories)
print(f"分层采样: {len(years)} 年 × {len(categories)} 类别 = {total_slots} 个查询")
print(f"每个查询最多 {papers_per_slot} 篇，预计耗时 5-15 分钟\n")

slot = 0
for year in years:
    for cat in categories:
        slot += 1
        query_params = {
            'search_query': f'cat:{cat} AND submittedDate:[{year}01010000 TO {year}12312359]',
            'start': 0,
            'max_results': papers_per_slot,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        url = f"{base_url}?{urlencode(query_params)}"
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(url, timeout=40) as response:
                    xml_data = response.read()
                root = ET.fromstring(xml_data)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = root.findall('atom:entry', ns)
                
                count = 0
                for entry in entries:
                    title = entry.findtext('atom:title', '', ns).replace('\n', ' ').strip()
                    summary = entry.findtext('atom:summary', '', ns).replace('\n', ' ').strip()
                    if title and summary:
                        all_papers.append({
                            'title': title, 'abstract': summary,
                            'category': cat, 'year': year
                        })
                        count += 1
                
                if attempt > 0:
                    print(f"[{slot:>2}/{total_slots}] {year} {cat} (第 {attempt+1} 次尝试): ✓ 成功 {count} 篇")
                else:
                    print(f"[{slot:>2}/{total_slots}] {year} {cat}: {count} 篇")
                
                time.sleep(5)
                break  # 成功提取，跳出重试循环
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"[{slot:>2}/{total_slots}] {year} {cat} (第 {attempt+1} 次尝试): ✗ {e}，等待 10 秒后重试...")
                    time.sleep(10)
                else:
                    print(f"[{slot:>2}/{total_slots}] {year} {cat}: ✗ 最终获取失败 - {e}")

print(f"\n共获取 {len(all_papers)} 篇，保存到 {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    for paper in all_papers:
        f.write(f"{paper['title']}\t{paper['abstract']}\t{paper['category']}\t{paper['year']}\n")

file_size = os.path.getsize(output_file) / 1024 / 1024
print(f"✓ 完成! 文件大小: {file_size:.1f} MB, 论文数: {len(all_papers)}")