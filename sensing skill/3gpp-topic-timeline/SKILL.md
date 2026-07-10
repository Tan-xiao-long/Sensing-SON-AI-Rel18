---
name: 3gpp-topic-timeline
description: 从 3GPP 工作组会议主席笔记（Chairs Notes）中提取 agreed 与非 agreed 议题及对应文稿，按需从 3GPP FTP 下载文稿原文并解压转文本，最终生成"以议题为主线"的讨论时间线调研报告（每个议题：提案人、逐次会议共识演进、最终结果、依据文稿及章节引用）。当用户提到 3GPP 会议调研、Chair notes / 主席笔记分析、RAN3/RAN2 等工作组议题梳理、TDoc 下载与总结、标准演进时间线、"按议题梳理"、agreed 文稿统计等需求时使用本 skill，即使用户没有明确说"时间线"或"报告"。纯 Python 实现，不依赖任何平台专有工具，可迁移。
compatibility: Python 3.8+；依赖 requests（下载）、python-docx（可选，docx 解析增强）；.doc 转文本优先用系统的 libreoffice/antiword（存在则自动调用），否则退化为内置纯 Python 提取
---

# 3GPP 议题时间线调研

把"按会议流水记录"的主席笔记，重组为"按议题演进"的调研报告。适用于 3GPP 各工作组（脚本默认适配 RAN3 风格的 Chairs Notes，其他工作组见 references/chair_notes_format.md 的调参说明）。

## 总体流程

```
0. 准备输入        会议主席笔记文件（.doc/.docx/.txt 或其 zip）放入一个目录，
                  编写 meetings.json（会议元数据：名称/日期/FTP目录/议程章节）
1. 解析主席笔记    python scripts/parse_chair_notes.py  → work/records.json
2. 组装议题时间线  python scripts/build_topic_timeline.py → work/topic_timeline.json
3. 下载文稿(可选)  python scripts/download_tdocs.py      → work/tdocs/<mtg>/R3-xxxxxx.zip
4. 解压与转文本    python scripts/extract_tdocs.py       → work/tdocs_txt/… + sections.json
5. 撰写报告        由模型按 references/report_template.md 逐议题撰写（见下"撰写报告"）
```

每一步的脚本都可独立运行，`--help` 有完整参数。步骤 3/4 可选：没有网络或不需要文稿级引用时，仅凭 records.json + topic_timeline.json 也能写出报告（引用粒度到"会议+议程节"）。

## 步骤 0：输入准备

创建一个工作目录，例如 `work/`。准备两样东西：

1. **主席笔记**：每次会议取"日期最新"的一份（RAN3 惯例为 `..._EOM`、`_EOM1`、`_EOM2` 等，取最大序号）。可以是 zip（内含 .doc）或已解压的 .doc/.docx/.txt。
2. **meetings.json**：会议清单，按时间先后排列。示例见 `references/meetings.example.json`。核心字段：

```json
[{
  "meeting": "RAN3#119",
  "date": "2023-02-27",
  "chair_notes": "input/RAN3_119_agenda_20230303_EOM2.zip",
  "ftp_dir": "https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_119/",
  "sections": [
    {"label": "SON", "start": "^10\\. Enhancement of Data Collection", "end": "^11\\. "},
    {"label": "AI",  "start": "^12\\. AI/ML for NG-RAN", "end": "^13\\. "}
  ],
  "filter_keywords": null
}]
```

`sections` 用正则圈定要分析的议程章节。注意：同一工作项在不同阶段会换议程位置（特性开发期在独立议程，如 RAN3 的 10/12 章；版本冻结后转入 "Corrections to Rel-XX" 章节，如 9.1.x），逐会议核对章节号——先 grep 章节标题再写 meetings.json，不要臆测。当一个章节混杂多主题（如纠错章节），用 `filter_keywords` 给出保留条目的正则（大小写敏感，避免 `SON` 误匹配 `Ericsson` 中的 `sson`，用 `\\bSON\\b`）。

## 步骤 1-2：解析与时间线组装

```bash
python scripts/parse_chair_notes.py --meetings meetings.json --out work/records.json
python scripts/build_topic_timeline.py --records work/records.json \
    --topics references/topics.example.json --out work/topic_timeline.json
```

`records.json`：每次会议 → 议程小节 → {当次新增共识文本行, 文稿条目[编号/标题/来源公司/结论/修订链]}。**agreed 与非 agreed（noted/withdrawn/discussion 等）都会保留**，供报告呈现"哪些方案被否/被搁置"。

`topics.json` 定义议题归组规则：议程小节名 → 议题 key，以及关键词兜底（用于纠错章节的散落条目）。示例 `references/topics.example.json` 是 RAN3 Rel-18 SON/MDT 与 AI/ML 的现成配置，可直接改造。

解析质量自检（重要）：
- 对照主席笔记原文抽查 2-3 个小节，确认结论（agreed/noted）与修订链（`Rev in R3-xxxxxx`）没有张冠李戴；
- 修订链交叠（同一 CB 块多条 Rev 行）是常见坑，`records.json` 中此类条目带有 `"ambiguous": true` 标记，报告中要么下载原文确认，要么明确标注"存疑"；
- Come-Back（CB）线下讨论直接产出的文稿没有原始提交条目，`origin` 字段为 `"(CB)"`。

## 步骤 3-4：下载与解压（可选）

```bash
python scripts/download_tdocs.py --records work/records.json --meetings meetings.json \
    --out work/tdocs --delay 2.0 --only-decisions agreed,endorsed
python scripts/extract_tdocs.py --in work/tdocs --out work/tdocs_txt
```

- 下载器对每篇文稿先试 `Docs/`、再试 `Inbox/`（会中修订稿多在 Inbox），带限速（默认 2 秒 + 随机抖动）与断点续传（已存在即跳过）。**3GPP FTP 对高频访问敏感，不要把 --delay 调到 1 秒以下**；大批量（>100 篇）建议分多次跑。
- `--only-decisions` 可过滤只下 agreed/endorsed；写报告若需引用被否方案的原文，再补下 noted 的关键篇目即可，不必全量。
- `extract_tdocs.py` 解压 zip、把 .doc/.docx 转成 .txt，并对 .docx 额外产出 `sections.json`（标题层级 → 行号映射），供报告引用"第几章第几节"。

## 步骤 5：撰写报告

读取 `references/report_template.md`，按其中的结构逐议题撰写。要点：

- **一个议题一章**，内部按时间线（会议先后）推进；不要按会议分章。
- **提案人**从文稿标题尾部括号中的来源公司统计（records.json 的 `source` 字段已提好）；区分"主要推动者"（多次提案/被 agree 的来源）与一般参与者。
- **每次会议写增量**：该议题这次会议新达成了什么、否掉了什么、遗留什么。records.json 的 `agreements` 行是当次新增共识（脚本已尽力与小节开头的历史累积共识分离，但仍需人工判断——若一条"共识"在更早会议的记录中出现过，它就不是本次的增量）。
- **最终结果**：议题收敛到的方案 + 最终落入的规范/CR。
- **依据引用**：每个论断给出处。三级粒度，能细则细：
  1. `〔RAN3#121 Chairs Notes §10.2.2〕` —— 主席笔记会议+议程节（步骤 1 即可支持）；
  2. `〔R3-234665〕` —— 文稿编号（步骤 1 即可支持）；
  3. `〔R3-234665 §2.1〕` —— 文稿内部章节（需要步骤 3-4，从 sections.json 或转出的 txt 中定位）。
- 写完后做一致性核查：每个议题的"最终结果"必须能被最后一次相关会议的记录支撑；引用的文稿编号在 records.json 中存在且结论无误。

## 常见问题

- **.doc 转文本乱码/空**：优先安装 libreoffice 或 antiword；两者都没有时脚本用内置提取（WordDocument 流 + cp1252/utf-16 启发式），对表格复杂的文件效果有限。
- **章节定位失败**：主席笔记转 txt 后标题格式可能变化，用 `grep -n "^10\." file.txt` 之类先确认再改 meetings.json 的正则。
- **换工作组**：RAN1/RAN2/SA2 的 chair notes / 会议报告格式不同，阅读 references/chair_notes_format.md 的"迁移到其他工作组"一节。
