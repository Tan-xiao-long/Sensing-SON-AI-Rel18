# RAN3 Chairs Notes 结构速查（解析依据）

理解主席笔记的记录惯例，是正确解析与撰写报告的前提。本文件描述 RAN3 风格；文末给出迁移到其他工作组的注意点。

## 文件获取

- 位置：`https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_<会议号>/Inbox/Chairs_Notes/`
- 命名：`RAN3_<号>_agenda_<日期>[_EOM|_EOM1|_EOM2].zip`。EOM = End of Meeting；数字后缀为会后修订版。**取序号最大 / 日期最新的一份**（历史版本是会中快照）。
- zip 内是单个 .doc（Word 二进制格式）。

## 议程结构

- 顶层章节 = 议程项（AI, Agenda Item）。特性开发期每个 WI 占一章（如 Rel-18 时 `10. Enhancement of Data Collection for SON_MDT…`、`12. AI/ML for NG-RAN`）；
- 版本功能冻结后，该版本条目转入"Corrections to Rel-XX"章节（如 `9.1.1. R18 SON/MDT`），原章节号让位给下一版本的 WI/SI——**同名议题在不同会议的章节号会漂移，必须逐会议确认**；
- 章下小节按特性方向划分（如 `10.2.1. SHR and SPR`、`12.2.2.3. ES and Xn procedures`）。

## 小节内的记录模式

一个小节从上到下通常是：

1. **累积共识区**：历次会议达成的 agreements 平铺罗列（无引号无标记），其中 `RAN3#120:` 这类行是"上次/更早会议"分隔标记——标记后的行属于更早会议的增量。判断"本次会议新增"需要与上一次会议的同小节文本对比才最可靠；
2. **文稿处理区**：每篇文稿三至多行：
   ```
   R3-234110                       ← 文稿号（单独一行）
   (TP for SON 38.413) …… (CATT)   ← 标题，末尾括号为来源公司
   CR0990r2, TS 38.413 …… / discussion / other   ← 类型行
   <讨论评论若干行>
   Rev in R3-234625  Agreed        ← 结论（可能有多级修订链）
   ```
   结论词汇：`agreed`（正式同意）、`agreed unseen`（同意但修订稿未再走读）、`endorsed (as BL CR)`（认可为基线 CR）、`noted`（记录不采纳/仅供参考）、`withdrawn`（撤稿）、无结论（仅讨论）。
3. **CB（Come-Back）区**：`# 标签名` + `(moderator - 公司)` 开头，是会中线下讨论的结论汇总。此区的行是**当次会议的新共识**；此区还会出现"`<描述> in R3-xxxxxx Agreed`"格式的直接产出文稿（无原始提交条目）。

## 已知解析坑

- `Rev in R3-xxxx` 与结论词可能分行、可能同行、可能连续多级（`Rev in A … Rev in B Agreed`——B 才是最终稿）；
- 同一 CB 块内多条修订行相邻时，修订链可能交叠（脚本对此标 `ambiguous: true`），需下载原文确认身份；
- 关键词过滤必须区分大小写：`SON` 会匹配 `Ericsson`，用 `\bSON\b`（脚本内已注意，但自定义 filter_keywords 时同样要小心）；
- .doc 转文本后表格结构丢失，文稿号必须依赖"单独成行"的模式识别；
- `agreed unseen` 与 `endorsed … unseen` 效力等同 agreed/endorsed，统计时合并、报告中注明即可；
- 转文本偶见全角/不间断空格（ ）与乱码字符（�），匹配正则用 `\s` 而非空格字面量。

## 迁移到其他工作组

- RAN2/RAN1 会议记录主要在 Chairman Notes / Session notes，决议词汇类似（agreed/endorsed/noted）但版式不同（RAN1 常用表格、RAN2 分 session notes 文件），需要调整 `parse_chair_notes.py` 中的 TDOC_RE（如 `R1-\d{7}`、`R2-\d{7}`）与小节标题正则；
- SA2 用 "approved/revised/noted/merged"，DEC_WORD 需扩充；
- CT/SA 全会用 TDoc list Excel 更可靠，可另行解析 xlsx 替代步骤 1。
