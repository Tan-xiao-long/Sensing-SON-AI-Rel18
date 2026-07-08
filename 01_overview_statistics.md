# 3GPP Release 18 SON 与 AI 相关议题调研报告
## ——基于 RAN3#121 会议主席笔记（Chairs Notes）的分析

**调研对象**：3GPP TSG-RAN WG3 第 121 次会议（RAN3#121，2023 年 8 月 21–25 日，法国图卢兹）
**数据来源**：`3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121/Inbox/Chairs_Notes/` 目录中日期最近的两个压缩包：

| 压缩包 | 服务器时间戳 | 说明 |
|---|---|---|
| `RAN3_121_agenda_20230825_EOM1.zip` | 2023-09-01 | 会后修订终版（End of Meeting rev.1），本报告以此为准 |
| `RAN3_121_agenda_20230825_EOM.zip` | 2023-08-25 | 会议结束版（End of Meeting） |

两版全文比对仅有 3 行差异，且均不影响 SON / AI 议题的结论：其一为第 9 章（Rel-17 及更早版本纠错）中一处结论由 "Agreed" 更正为 "Rev in R3-234775 Agreed unseen"；其二为 10.2.4 节中 R3-234641 的规范号笔误修正（38.413→38.423）；其三为第 17 章附近一处 LS 草稿状态补记 withdrawn。因此下文统计对两个压缩包同时成立。

---

## 1. 调研范围与背景

RAN3 是 3GPP 中负责 RAN 架构与接口协议（NGAP/XnAP/F1AP/E1AP/X2AP 等）的工作组。Release 18 中与 **SON（自组织网络）** 和 **AI（人工智能）** 直接相关、且由 RAN3 主导的两个核心工作项（WI）在本次会议的议程如下：

| 议程 | 工作项 | WID | 目标版本 | 相关性 |
|---|---|---|---|---|
| AI 10 | Enhancement of Data Collection for SON/MDT in NR standalone and MR-DC（SON/MDT 数据收集增强） | RP-231157（NR_ENDC_SON_MDT_enh2-Core） | RAN #102 | SON 直接相关 |
| AI 12 | AI/ML for NG-RAN（NG-RAN 人工智能/机器学习） | RP-231159（NR_AIML_NGRAN-Core） | RAN #100 | AI 直接相关，其三大用例（网络节能、负载均衡、移动性优化）本质上是 SON 功能的智能化 |

> 说明：本次会议中其他议程（如 AI 24 网络节能 WI、AI 11 QoE 等）与 SON/AI 存在间接联系，但按调研要求，本报告聚焦上述两个议程下 **达成 agree 结论的议题与文稿**。

### 1.1 结论用语说明

RAN3 主席笔记中的文稿结论分为几类，本报告统计口径如下：

- **agreed**：内容获会议正式同意（TP 文本并入基线 CR，或 LS 正式发出）——本报告的统计主体；
- **agreed unseen**：会上达成一致后按修订指示更新、未再走读即视为同意（"agreed 未走读"），效力等同 agreed；
- **endorsed as BL CR**：被认可为基线 CR（Baseline CR）。Rel-18 特性以 BL CR 为载体持续演进，各次会议 agreed 的 TP（Text Proposal）都合入 BL CR，最终打包提交 RAN 全会批准。endorsed 文稿同样属于"会议同意的输出物"，本报告一并列出并总结；
- **noted / discussion / other**：仅记录、未形成结论或作为讨论输入；**withdrawn**：撤稿。

---

## 2. 总体统计

### 2.1 SON 议题（AI 10，Rel-18 SON/MDT 增强 WI）

本议程共处理文稿 71 篇（不含会中修订版），其中 **agreed 16 篇**（含 agreed unseen 5 篇）、**endorsed 为基线 CR 12 篇**、noted 4 篇、withdrawn 2 篇（R3-233740 及会中撤回的 R3-234672），其余为 discussion/other 类输入稿。按子议程分布：

| 子议程 | 主题 | 处理文稿数 | agreed 文稿（最终版本号） | endorsed BL CR |
|---|---|---|---|---|
| 10.1 | General（基线 CR 维护、工作计划） | 13 | — | 11 篇（见 §3.1） |
| 10.2.1 | SHR 与 SPR（成功切换报告/成功 PSCell 变更报告） | 13 | R3-234716（回复 RAN2 的 LS） | — |
| 10.2.2 | MRO（移动鲁棒性优化） | 15 | R3-234665、R3-234625、R3-234666 | — |
| 10.2.3 | RACH 增强 | 11 | R3-234643（LS）、R3-234647、R3-234649、R3-234650、R3-234695、R3-234742、R3-234743 | — |
| 10.2.4 | 非公共网络（NPN）的 SON/MDT 增强 | 9 | R3-234718、R3-234719、R3-234744（LS） | R3-234720 |
| 10.2.5 | SON for NR-U（免许可频段） | 8 | R3-234544、R3-234545 | — |
| 10.2.6 | MDT 增强（记录型 MDT 覆盖保护） | 2 | —（2 篇均 noted，无共识） | — |

### 2.2 AI 议题（AI 12，Rel-18 AI/ML for NG-RAN WI）

本议程共处理文稿 89 篇，其中 **agreed 4 篇**（含 agreed unseen 1 篇）、**endorsed 为基线 CR 3 篇**、noted 7 篇（工作计划、各线下讨论纪要及 1 篇未获通过的 TP），其余为 discussion/other。按子议程分布：

| 子议程 | 主题 | 处理文稿数 | agreed 文稿（最终版本号） | endorsed BL CR |
|---|---|---|---|---|
| 12.1 | General（基线 CR 维护、工作计划） | 4 | — | R3-233756（38.423）、R3-233780（38.300）、R3-233789（38.401） |
| 12.2.1 | Stage 2 相关 + 通用流程设计 | 22 | R3-234663（预测时间）、R3-234658（38.300 Stage2）、R3-234724（过程改名 DATA COLLECTION） | — |
| 12.2.2.1 | 负载均衡（LB）与 Xn 过程 | 13 | —（R3-234689 被 noted，未 agree） | — |
| 12.2.2.2 | 移动性优化（ME/MO）与 Xn 过程 | 17 | —（达成多项共识但未形成 agreed TP） | — |
| 12.2.2.3 | 网络节能（ES/NES）与 Xn 过程 | 15 | R3-234752（Energy Cost 上报 TP） | — |
| 12.2.2.4 | 其他接口（E1/F1，split 架构） | 6 | —（分歧明显，未 agree） | — |
| 12.3 | Others（面向 AI 的 MDT 连续采集等） | 12 | —（LS 草稿均未发出） | — |

### 2.3 统计小结

- 两个议程合计处理 160 篇文稿，**最终 agreed 20 篇、endorsed 基线 CR 15 篇**；
- SON/MDT WI 已进入 Stage 3 收敛期：本次会议在 SHR/SPR 转发、MRO 语音回落新报告类型、RACH Indication 新过程、NPN 的 MDT 支持、NR-U 负载均衡等方向产出了大量可直接合入 BL CR 的 agreed TP；
- AI/ML WI 处于 Stage 2 向 Stage 3 过渡期：agreed 文稿集中在"通用数据收集框架"（新 Xn 过程命名、请求预测时间编码）与节能用例（Energy Cost 上报），负载均衡与移动性优化用例形成了较多口头共识（agreements）但 TP 大多留待下次会议；
- 值得注意的是，AI/ML 议题下多项关键结论以"会议共识（agreements）"而非文稿形式确立（如 DATA COLLECTION 过程族命名、EC 为节点级参数等），这些共识在 §5 中逐条列出。

---
