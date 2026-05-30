#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reducer.py: 统计每个 (年份, 词) 组合的论文数
输入: YEAR_WORD\t1  (已按key排序)
输出: YEAR_WORD\tcount
"""
import sys

current_key = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    
    key, value = parts[0], parts[1]
    
    try:
        count = int(value)
    except:
        continue
    
    if key == current_key:
        current_count += count
    else:
        if current_key is not None:
            print(f"{current_key}\t{current_count}")
        current_key = key
        current_count = count

if current_key is not None:
    print(f"{current_key}\t{current_count}")