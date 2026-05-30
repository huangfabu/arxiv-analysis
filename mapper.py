#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mapper.py: 从每篇论文的标题+摘要中提取关键词
输入: title\tabstract\tcategory\tyear (每行一篇)
输出: YEAR_WORD\t1
"""
import sys
import re

STOPWORDS = {
    'the','a','an','and','or','but','in','on','at','to','for','of','with',
    'by','from','is','was','are','were','be','been','have','has','had',
    'do','does','did','will','would','could','should','may','might','can',
    'this','that','these','those','we','our','they','their','it','its',
    'not','no','as','if','while','when','where','which','who','what','how',
    'than','then','so','also','each','more','most','other','such','into',
    'there','here','paper','papers','work','show','shows','shown',
    'proposed','propose','presents','present','based','using','used','use',
    'provide','provides','given','however','although','since','between',
    'within','about','against','through','during','over','after','above',
    'further','across','both','without','where','whether','thus','hence',
    'two','three','four','five','one','several','many','few','new','high',
    'large','small','first','second','different','various','recent',
    'existing','state','art','experimental','experiments','significantly'
}

MIN_LEN = 3
MAX_LEN = 25

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split('\t')
    if len(parts) < 4:
        continue
    
    title, abstract, category, year_str = parts[0], parts[1], parts[2], parts[3]
    
    try:
        year = int(year_str)
        if year < 2010 or year > 2030:
            continue
    except:
        continue
    
    text = f"{title} {abstract}".lower()
    # 提取纯字母单词和连字符词(如 self-attention, few-shot)
    words = re.findall(r'[a-z][a-z-]{2,}[a-z]', text)
    
    seen = set()  # 每篇论文内去重:统计"包含该词的论文数"
    for word in words:
        word = word.strip('-')
        if (word not in STOPWORDS
                and MIN_LEN <= len(word) <= MAX_LEN):
            if word not in seen:
                seen.add(word)
                print(f"{year}_{word}\t1")