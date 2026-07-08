# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

# 7. 附录

## 7.1 调研方法与文档获取说明

1. 从 `3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121/Inbox/Chairs_Notes/` 获取日期最近的两个压缩包（EOM 与 EOM1）并全文比对；
2. 解析主席笔记议程第 10 章（SON/MDT WI）与第 12 章（AI/ML WI）下全部 160 条文稿处理记录，提取结论（agreed / agreed unseen / endorsed as BL CR / noted / withdrawn）及会中修订链（Rev in R3-xxxxxx）；
3. 按最终版本号从 `TSGR3_121/Docs/` 与 `TSGR3_121/Inbox/` 逐一取回全部 35 篇 agreed/endorsed 文稿原文（限速抓取，间隔 1.2–2 秒），逐篇阅读并总结；
4. 会议基础信息（会议号、时间、地点、文稿号段）与文稿状态经 3GPP Portal（portal.3gpp.org，meetingId=39970）交叉核对。

## 7.2 agreed / endorsed 文稿速查表

| 最终文稿 | 会中修订自 | 规范 | 议程 | 结论 |
|---|---|---|---|---|
| R3-233748 | — | TS 38.413 (CR0990r2) | 10.1 | endorsed BL CR |
| R3-233794 | — | TS 38.413 (CR0964r4) | 10.1 | endorsed BL CR |
| R3-233757 | — | TS 38.423 (CR1050r2) | 10.1 | endorsed BL CR |
| R3-233758 | — | TS 38.423 (CR0934r7) | 10.1 | endorsed BL CR |
| R3-234372 | R3-233740 | TS 36.423 (CR1747r3) | 10.1 | endorsed BL CR |
| R3-233805 | — | TS 38.473 (CR1105r5) | 10.1 | endorsed BL CR |
| R3-234538 | R3-233802 | TS 38.470 (CR0114r2) | 10.1 | endorsed BL CR unseen |
| R3-233790 | — | TS 38.401 (CR0282r3) | 10.1 | endorsed BL CR |
| R3-233772 | — | TS 36.300 (draft CR) | 10.1 | endorsed BL CR |
| R3-233781 | — | TS 38.300 (draft CR) | 10.1 | endorsed BL CR |
| R3-233775 | — | TS 37.340 (draft CR) | 10.1 | endorsed BL CR |
| R3-234716 | R3-234612 | LS → RAN2 | 10.2.1 | agreed |
| R3-234665 | R3-233933 | TS 38.423 TP | 10.2.2 | agreed |
| R3-234666 | —（CB 产出） | TS 37.340 TP | 10.2.2 | agreed |
| R3-234625 | R3-234110 | TS 38.413 TP | 10.2.2 | agreed |
| R3-234643 | —（CB 产出） | LS → RAN2 | 10.2.3 | agreed |
| R3-234647 | R3-234068 | TS 36.423 TP（X2AP） | 10.2.3 | agreed |
| R3-234649 | —（CB 产出） | TS 36.300 TP | 10.2.3 | agreed |
| R3-234650 | —（CB 产出） | TS 38.300 TP | 10.2.3 | agreed |
| R3-234695 | —（CB 产出） | TS 37.340 TP | 10.2.3 | agreed |
| R3-234742 | R3-234069→R3-234648 | TS 38.420 TP | 10.2.3 | agreed unseen |
| R3-234743 | R3-234415→R3-234671 | TS 38.423 TP | 10.2.3 | agreed unseen |
| R3-234718 | R3-234417→R3-234675 | TS 38.413 TP | 10.2.4 | agreed unseen |
| R3-234719 | R3-234641 | TS 38.423 TP | 10.2.4 | agreed unseen |
| R3-234720 | R3-234132→R3-234607 | TS 37.320 BL CR | 10.2.4 | endorsed BL CR unseen |
| R3-234744 | R3-234717→R3-234723 | LS → RAN2/SA5 | 10.2.4 | agreed unseen |
| R3-234544 | R3-234315（部分） | TS 38.423 TP | 10.2.5 | agreed |
| R3-234545 | R3-234315（部分） | TS 38.473 TP | 10.2.5 | agreed |
| R3-233756 | — | TS 38.423 (CR0959r7) | 12.1 | endorsed BL CR |
| R3-233780 | — | TS 38.300 (draft CR) | 12.1 | endorsed BL CR |
| R3-233789 | — | TS 38.401 (CR0265r7) | 12.1 | endorsed BL CR |
| R3-234658 | R3-234279 | TS 38.300 TP | 12.2.1 | agreed |
| R3-234663 | R3-234376 | TS 38.423 TP | 12.2.1 | agreed |
| R3-234724 | R3-234289 | TS 38.423 TP | 12.2.1 | agreed |
| R3-234752 | R3-234297→R3-234728 | TS 38.423 TP | 12.2.2.3 | agreed unseen |

## 7.3 参考来源

- 主席笔记（本报告主数据源）：[Chairs_Notes 目录](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121/Inbox/Chairs_Notes/)（RAN3_121_agenda_20230825_EOM.zip、RAN3_121_agenda_20230825_EOM1.zip）
- 文稿原文：[TSGR3_121/Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121/Docs/) 与 [TSGR3_121/Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121/Inbox/)
- 会议与文稿状态核对：[3GPP Portal TDoc 列表（meetingId=39970）](https://portal.3gpp.org/ngppapp/TdocList.aspx?meetingId=39970)
- 工作项描述：RP-231157（Rel-18 SON/MDT 增强 WID）、RP-231159（Rel-18 AI/ML for NG-RAN WID）；Rel-17 研究基础：TR 37.817

---
*报告生成日期：2026-07-08。本报告基于 RAN3#121（2023-08）主席笔记终版（EOM1）编制；agreed unseen 表示会上达成一致、修订稿未再走读即视为同意；BL CR 为持续演进的基线 CR，其最终版本以后续 RAN 全会批准版本为准。*
