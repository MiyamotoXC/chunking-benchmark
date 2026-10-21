# 切片策略基准评测（chunking-benchmark）

> 一套**文本切片（Chunking）策略基准对比工具**：在同一份语料上跑 6 种切片策略，量化对比切片数、平均/最短/最长长度、长度方差与推荐度，
> 帮你在 RAG 落地前用数据选出最适合当前语料的切分方式，而不是拍脑袋定 chunk_size。

> 作者：[@MiyamotoXC](https://github.com/MiyamotoXC) ｜ 许可证：MIT ｜ 欢迎 Star / Fork 二次开发。

## 一、内置 6 种策略

| # | 策略 | 切分逻辑 |
|---|---|---|
| 1 | 固定长度切片 | 按 `TARGET_SIZE` 切，回退到最近句末，带 `OVERLAP` 重叠 |
| 2 | 句子边界切片 | 按句累积到 `max_chunk_size` 再断块 |
| 3 | LLM 语义切片 | `qwen-plus` 按语义完整性切分；无 Key 时自动降级为策略 2 |
| 4 | 滑动窗口切片 | 固定 `window_size` + `step_size` 连续滑窗 |
| 5 | 自适应切片 | 按段落聚合，超 `target_size` 断块 |
| 6 | 智能自适应切片 | 按句聚合，带 `min_size`/`max_size` 上下限 |

## 二、目录结构

```
chunking-benchmark/
├── config.py          # 语料路径、目标长度、LLM 模型（密钥走环境变量）
├── benchmark.py       # 6 策略实现 + 对比评测主程序
├── example_docs/      # 脱敏示例语料
├── requirements.txt
└── LICENSE
```

## 三、快速开始

```bash
pip install -r requirements.txt

# 可选：启用 LLM 语义切片
export DASHSCOPE_API_KEY="你的密钥"      # Windows: set DASHSCOPE_API_KEY=...

python benchmark.py
```

输出 6 种策略的统计表：切片数、平均长度、长度方差、推荐度（1-5）。

## 四、配置（config.py）

| 项 | 默认 | 说明 |
|---|---|---|
| `DASHSCOPE_API_KEY` | 环境变量（可选） | 仅 LLM 语义切片需要 |
| `CORPUS_PATH` | `example_docs/sample.txt` | 评测语料 |
| `TARGET_SIZE` | 300 | 目标块长度 |
| `OVERLAP` | 50 | 固定长度切片重叠 |
| `LLM_MODEL` | `qwen-plus` | 语义切片模型 |

## 五、能力边界（诚实说明）

- 推荐度是基于「切片数 / 长度方差 / 平均长度」的启发式评分，仅作横向参考，非检索召回率
- 真实选型应结合下游检索召回率（建议接一个 reranker 或人工标注集再定）
- LLM 语义切片有调用成本与延迟，批量大时建议仅在冷启动阶段做一次

## 六、License

代码以 MIT 发布。
