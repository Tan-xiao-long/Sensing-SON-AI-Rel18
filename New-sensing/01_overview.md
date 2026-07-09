# 3GPP Release 18 全周期 SON 与 AI 相关 agreed 议题调研

## ——RAN3 #119 ~ #124 共 9 次会议主席笔记汇总（含各议题增强内容）


**数据来源**：您提供的 R18_sensing 文件夹中 8 次会议的主席笔记终版（EOM/EOM1/EOM2 取最新），加上此前已详查的 RAN3#121。

**范围说明**：
- **SON 相关**：Rel-18 WI《Enhancement of Data Collection for SON/MDT in NR standalone and MR-DC》（NR_ENDC_SON_MDT_enh2，WID RP-231157），#119~#122 位于议程 10，#123 起转入议程 9"Corrections to Rel-18"；
- **AI 相关**：Rel-18 WI《AI/ML for NG-RAN》（NR_AIML_NGRAN，WID RP-231159），#119~#122 位于议程 12，#123 起转入议程 9；
- 两个 WI 的特性开发在 **RAN3#122（2023 年 11 月）收官**（基线 CR 打包提交 RAN 全会批准），#123/#123bis/#124 为 Rel-18 纠错维护阶段；
- #123bis 起议程 10 与 11 已是 **Rel-19** 的 SON/MDT WI（NR_ENDC_SON_MDT_Ph4）与 AI/ML SI（FS_NR_AIML_NGRAN_enh），不计入本报告；
- ⚠️ **覆盖缺口**：两个 Rel-18 WI 自 2022 年（约 RAN3#116 起）即开始工作，本报告从 #119（2023.02）开始，缺 #116~#118（2022 年）的早期阶段（以场景与方案选型共识为主，其成果已累积体现在后续基线 CR 中）。

**统计口径**：agreed / agreed unseen 为正式同意的 TP、LS、CR；endorsed（as BL CR）为认可的基线 CR 或待复审 CR。"原稿"列为会中修订前的提交稿号；(CB) 表示由线下讨论（Come-Back）直接产出。少数修订链交叠、原稿存疑的条目已标注"下载后确认"。

## 总体统计

| 会议 | SON agreed | SON endorsed | AI agreed | AI endorsed |
|---|---|---|---|---|
| RAN3#119 (2023.02.27–03.03, 雅典) | 6 | 3 | 2 | 3 |
| RAN3#119bis-e (2023.04.17–26, 线上) | 21 | 5 | 2 | 3 |
| RAN3#120 (2023.05.22–26, 仁川) | 14 | 9 | 6 | 3 |
| RAN3#121 (2023.08.21–25, 图卢兹)【已详查】 | 16 | 12 | 4 | 3 |
| RAN3#121bis (2023.10.09–13, 厦门) | 8 | 13 | 7 | 3 |
| RAN3#122 (2023.11.13–17, 芝加哥；R18 两 WI 收官) | 13 | 13 | 7 | 4 |
| RAN3#123 (2024.02.26–03.01, 雅典；R18 纠错阶段) | 10 | 6 | 5 | 1 |
| RAN3#123bis (2024.04.15–19, 长沙) | 0 | 0 | 0 | 1 |
| RAN3#124 (2024.05.20–24, 福冈) | 6 | 5 | 4 | 2 |
| **合计** | **94** | **66** | **37** | **23** |

> 注：endorsed 的基线 CR 每次会议都重新认可一版（累计吸收当次 agreed 的 TP），存在跨会议重复。若目的是取每个特性的最终文本，只需下载 **#122 的 endorsed 基线 CR（终版）** 加上 **#123/#124 的纠错 CR** 即可。

## 文稿下载位置

所有文稿位于 `https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/<会议目录>/` 下（目录名已逐一核实）：

| 会议 | 会议目录 | 原稿位置 | 会中修订稿（最终 agreed 版本）位置 |
|---|---|---|---|
| RAN3#119 | `TSGR3_119` | `TSGR3_119/Docs/` | `TSGR3_119/Inbox/`（若不在则查 `Docs/`） |
| RAN3#119bis-e | `TSGR3_119bis-e` | `TSGR3_119bis-e/Docs/` | `TSGR3_119bis-e/Inbox/`（若不在则查 `Docs/`） |
| RAN3#120 | `TSGR3_120` | `TSGR3_120/Docs/` | `TSGR3_120/Inbox/`（若不在则查 `Docs/`） |
| RAN3#121 | `TSGR3_121` | `TSGR3_121/Docs/` | `TSGR3_121/Inbox/`（若不在则查 `Docs/`） |
| RAN3#121bis | `TSGR3_121-bis` | `TSGR3_121-bis/Docs/` | `TSGR3_121-bis/Inbox/`（若不在则查 `Docs/`） |
| RAN3#122 | `TSGR3_122` | `TSGR3_122/Docs/` | `TSGR3_122/Inbox/`（若不在则查 `Docs/`） |
| RAN3#123 | `TSGR3_123` | `TSGR3_123/Docs/` | `TSGR3_123/Inbox/`（若不在则查 `Docs/`） |
| RAN3#123bis | `TSGR3_123-bis` | `TSGR3_123-bis/Docs/` | `TSGR3_123-bis/Inbox/`（若不在则查 `Docs/`） |
| RAN3#124 | `TSGR3_124` | `TSGR3_124/Docs/` | `TSGR3_124/Inbox/`（若不在则查 `Docs/`） |

规律：编号较小的原始提交稿在 `Docs/`；会中修订产生的最终 agreed 稿（编号在当次会议号段末端）通常在 `Inbox/`。用 `R3-2xxxxx.zip` 文件名直接拼 URL 即可。


---
