#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wordcloud import WordCloud
from collections import defaultdict
import os

results_file = os.path.expanduser('~/arxiv-analysis/results.txt')
output_dir   = os.path.expanduser('~/arxiv-analysis/charts')
os.makedirs(output_dir, exist_ok=True)

# ── 读取 MapReduce 输出 ───────────────────────────────────────────
data = []
with open(results_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
        key, cnt = parts
        idx = key.index('_')
        year_str, word = key[:idx], key[idx+1:]
        try:
            data.append({'year': int(year_str), 'word': word, 'count': int(cnt)})
        except:
            continue

df = pd.DataFrame(data)
years = sorted(df['year'].unique())
print(f"Records: {len(df)}  Year range: {df['year'].min()}-{df['year'].max()}")

# ── 图1: 总体 Top30 高频词 (横向条形图) ─────────────────────────
top30 = df.groupby('word')['count'].sum().sort_values(ascending=False).head(30)

fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top30.index[::-1], top30.values[::-1], color='steelblue', edgecolor='white')
ax.set_xlabel('Paper Count (deduplicated)', fontsize=12)
ax.set_title('Top 30 Keywords in arXiv AI Papers (2012-2026)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
fig.savefig(f'{output_dir}/fig1_top30_overall.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Fig1: top30_overall.png")

# ── 图2: 关键术语年度趋势 (折线图 -- 报告核心亮点) ──────────────
# 选择能体现AI发展历程的代表性词汇
trend_terms = [
    'convolutional', 'recurrent', 'generative',
    'attention', 'transformer', 'reinforcement',
    'diffusion', 'multimodal', 'self-supervised'
]
existing = [t for t in trend_terms if t in df['word'].values]

pivot = df[df['word'].isin(existing)].pivot_table(
    index='year', columns='word', values='count', aggfunc='sum', fill_value=0
)

fig, ax = plt.subplots(figsize=(14, 7))
colors = ['#E24B4A','#185FA5','#1D9E75','#EF9F27','#534AB7',
          '#D85A30','#3B6D11','#993556','#0F6E56']
for i, term in enumerate(existing):
    if term in pivot.columns:
        vals = pivot[term].reindex(years, fill_value=0)
        ax.plot(years, vals, marker='o', linewidth=2.2,
                label=term, color=colors[i % len(colors)])

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Papers', fontsize=12)
ax.set_title('Evolution of Key AI Research Topics (2012-2026)', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', ncol=2, fontsize=10)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
plt.xticks(rotation=45)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
fig.savefig(f'{output_dir}/fig2_trend_keywords.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Fig2: trend_keywords.png")

# ── 图3: 近三年热词 Top20 ────────────────────────────────────────
recent = df[df['year'] >= 2023].groupby('word')['count'].sum() \
           .sort_values(ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(recent.index[::-1], recent.values[::-1], color='coral', edgecolor='white')
ax.set_xlabel('Paper Count', fontsize=12)
ax.set_title('Top 20 Hot Keywords (2023-2026)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
fig.savefig(f'{output_dir}/fig3_recent_top20.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Fig3: recent_top20.png")

# ── 图4: 词云 (2020-2026 论文词频) ──────────────────────────────
recent_freq = df[df['year'] >= 2020].groupby('word')['count'].sum()
wc = WordCloud(
    width=1200, height=600,
    background_color='white',
    max_words=150,
    colormap='viridis',
    prefer_horizontal=0.7
).generate_from_frequencies(recent_freq.to_dict())

fig, ax = plt.subplots(figsize=(14, 7))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
ax.set_title('Word Cloud of AI Research Keywords (2020-2026)', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(f'{output_dir}/fig4_wordcloud.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Fig4: wordcloud.png")

print(f"\nAll charts saved to: {output_dir}/")

# ── 打印关键统计 ──────────────────────────────────────────────────
total_freq = df.groupby('word')['count'].sum().sort_values(ascending=False)
print("\n>>> Overall Top15 Keywords:")
for w, c in total_freq.head(15).items():
    print(f"  {w:<20} {c:>5}")