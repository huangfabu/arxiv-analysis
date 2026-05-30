# arXiv AI Paper Keyword Trend Analysis (2012-2026)

Cloud Computing Big Assignment — Jiangnan University, AI 2401

## Overview
Distributed keyword frequency analysis on arXiv AI papers using Hadoop MapReduce on Alibaba Cloud ECS.

## Tech Stack
- Hadoop 3.4.0 (HDFS + YARN + MapReduce)
- Python Streaming (mapper.py / reducer.py)
- Matplotlib + WordCloud (visualization)
- Docker + Nginx (deployment)

## Files
- `fetch_arxiv.py` — fetch papers from arXiv API (2012-2026, stratified by year)
- `mapper.py` — extract keywords per paper, emit YEAR_WORD\t1
- `reducer.py` — sum keyword counts by year
- `visualize.py` — generate 4 charts from results
- `Dockerfile` — containerize the web visualization
- `web/index.html` — results showcase page

## Student
单义凯 | 1190224121 | AI 2401 | May 2026