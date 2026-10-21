# -*- coding: utf-8 -*-
"""切片策略基准评测：统一配置。"""
import os

# 可选：仅 LLM 语义切片需要；未设置时自动降级为基础语义切片
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
CORPUS_PATH = "example_docs/sample.txt"
TARGET_SIZE = 300
OVERLAP = 50
LLM_MODEL = "qwen-plus"
