# 3GPP R18 全周期 SON/AI agreed 议题调研（RAN3 #119–#124）

> 本文件为拆分版之一，目录见 00_README.md。

## RAN3#121bis (2023.10.09–13, 厦门)

### 本次会议 SON/MDT 主要共识与增强内容

**SHR/SPR**
- SPR 触发协调达成方案：对 SN 发起的 PSCell change/CPC，source SN 应向 MN 提供其 T310/T312 SPR 触发（门限）；并发 LS 请 RAN2 确认可否增强节点间 RRC 信令（如 CG-Config）以携带 T310/T312/T304 Threshold。
- UE 上下文检索方案收敛：R18 中无需 UE 上报任何额外信息用于 SHR/SPR 的 UE context 检索（即沿用遗留方案，不采纳 "Configuration Information" 新方案）。
- 明确 T304 SPR 触发的优化目标是优化 target SN 的 RACH 接入问题（而非发起节点的移动性配置）。
- 通过 Reply LS to RAN2 on SON SPR（R3-235868）及 Samsung 的 37.340/38.423 SPR TP（R3-235848）。

**MRO**
- CPAC：通过 Samsung 的 37.340 CPAC 增强 TP（R3-235809）；CPA/MN 发起 CPC 及 SN 发起 CPC 的失败信息传递方案（Option 1 vs Option 2）本次仍未收敛。
- 语音回落：通过 36.300 与 38.300 的 voice fallback stage2 TP（R3-235865、R3-235866），落实 inter-system HO for voice fallback 的失败检测描述。
- 快速 MCG 恢复：认可 UE 上报 "MCG failure 与 SCG failure 之间的时间" 有益，发出 LS 至 RAN2（R3-235897）请求补充信息，措辞修正为针对 "successful Fast MCG Recovery" 场景。

**RACH Enhancements**
- 完成 RACH Indication 相关 BLCR 清理并通过三份 TP：36.423（R3-235729）、38.423（R3-235854）、38.473（R3-235855）。
- 参数取值确定：RACH INDICATION 消息中 RA Report Indication 的最大数目定为 64，常量更名为 maxnoofUEsforRAReportIndications。
- 移除 38.423/36.423 中 RACH Indication 的 Editor's note。

**NPN**
- 结论：在 RLF report 中加入 SNPN ID 对可观测性（observability）有益，但未找到对移动性优化有益的用例；关于 E-SNPN 的 LS（R3-235871）最终不再推进。
- Logged MDT 与 E-SNPN：确认 Rel-18 中 MDT 用 SNPN list 的使用无限制，RAN3 现有机制已支持 E-SNPN 的 logged MDT。
- UHI 中的 undisclosed cell 信息、PNI-NPN PLMN-wide 区域范围选项均不在 R18 推进。
- 通过 TP：R3-235870（38.413 NPN 增强）、R3-235885（37.320 移除 Editor's note，需 RAN2 确认）。
- FFS：Xn 上无 Area Scope for MDT IE 时是否忽略 PNI-NPN Area Scope for MDT IE。

**SON for NR-U**
- 达成 WA：在 HO 失败场景下，支持 target 节点向 source 节点上报 DL LBT 失败次数（前提是能识别 UE），细节 FFS。
- 其余问题维持 FFS：非 HOF 的 RLF 场景下 UL LBT 失败次数上报、DL LBT 问题导致 TEH/太晚切换（Too Early HO/HO to Wrong Cell）时 last serving node 的通知处理、Resource Status Update 中是否新增 UL consistent LBT failure 次数负载度量。
- Huawei 的 38.300 NR-U stage2 文稿改为 TP 格式继续处理（R3-235733）。

**MDT Enhancements**
- 本次无实质新共识（仅讨论 Nokia 的 logged MDT override protection 文稿并 noted，继续等待 RAN2 进展）。

### 本次会议 AI/ML 主要共识与增强内容

**Stage2**
- 明确范围限定：AI/ML 功能的支持不适用于 ng-eNB（连接 5GC 的 E-UTRA 节点），并据此更新 38.300 stage2 描述（通过 ZTE 的 38.300 TP，R3-235904）。
- 完成 stage2/stage3 文本清理（以 R3-235137、R3-235625 为起点），过程/消息名沿用上次会议改名后的 Data Collection 系列（DATA COLLECTION REQUEST/RESPONSE/UPDATE）。

**LB（负载均衡）**
- UE performance feedback 上报周期确定：复用 Data Collection Request 中现有 Reporting Periodicity IE，不引入专用周期 IE；对一对 Measurement ID，DATA COLLECTION UPDATE 的发送频率由该 Reporting Periodicity 决定；是否另引入测量收集周期 FFS。
- 收集时长方案确定：在 DATA COLLECTION REQUEST 中引入 UE Performance Configuration IE，包含 UE performance feedback 测量收集时长（自 HO 执行起算）；取值范围与命名 FFS。
- 明确 UE performance feedback 与 UE trajectory 的收集时长不用单一 IE 表达（分开配置）。
- 无共识：被请求节点向请求节点显式指示触发事件（如 UE 转 idle/inactive、切走）不引入。
- 术语澄清：UE performance 中的 "Average Packet Loss" 即现有 "Packet Loss Rate" IE。
- 通过 TP：Data Collection Reporting 过程通用文本（R3-235902，38.423）、38.420 Xn 通用规范支持（R3-235903）、Samsung LB 文稿修订（R3-235879）。

**ME（移动性优化）**
- 实测 UE 轨迹（Measured UE Trajectory）编码确定：定义新 IE（不复用 UHI），其中 Global NG-RAN Cell Identity 与 Time UE Stays in Cell 为必选。
- 在 DATA COLLECTION REQUEST 中为实测 UE 轨迹收集新定义 Time Duration IE 与 Number of Visited Cell IE（细节 FFS）。
- 参数取值确定：预测 UE 轨迹与实测 UE 轨迹的最大小区数均为 16。
- 无共识：不引入实测 UE 轨迹收集退出条件（exit condition）的显式指示信令。
- 通过 TP：R3-235834（ZTE，38.423 实测/预测 UE 轨迹遗留问题）、R3-235906（Ericsson，小区级 UE 轨迹预测配置，新 IE 细节加注 Editor's note）。

**ES（节能）**
- 通过 Reply LS to SA5（R3-235743），回应 SA5 关于 Energy Cost index 的来函：确认 ng-eNB 不在 Rel-18 AI/ML for NG-RAN WI 范围内；"能耗到 EC" 映射规则的适用区域由运营商决定。

**其他接口（F1/E1，拆分架构）**
- 会中曾形成 WA（按 Xn 设计为 F1 上的实测 EC 传输定义新过程），但最终 CB 结论推翻该 WA：R18 不再推进支持拆分 RAN 架构的 AI/ML 增强（即不引入 F1/E1 的 EC 等信令）。

**Others（AI/ML 用 MDT 增强）**
- 结论：面向 AI/ML 连续数据收集的 MDT 增强（连续 MDT、logged UE 轨迹获取、更细粒度 UE 选择等既列问题）在 Rel-18 不再推进解决方案。

### SON 相关 agreed 文稿

| 最终文稿 | 原稿 | 内容/议题 | 结论 | 下载 |
|---|---|---|---|---|
| R3-235848 | R3-235210 | TP 37.340/38.423：SPR 的 SON 增强 | agreed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235848.zip) |
| R3-235868 | (CB) | Reply LS 致 RAN2：SON SPR | agreed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235868.zip) |
| R3-235809 | R3-235211 | TP 38.423/37.340：CPAC 的 SON 增强 | agreed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235809.zip) |
| R3-235897 | R3-235553/R3-235867 | TP 37.340 CPAC 失败定义澄清 / LS 致 RAN2 快速MCG恢复（修订链交叠，下载后确认） | agreed unseen | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235897.zip) |
| R3-235854 | (CB) | TP：RACH 增强（会中修订） | agreed unseen | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235854.zip) |
| R3-235855 | R3-235444 | TP 36.423/38.423/38.473：RACH 增强 | agreed unseen | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235855.zip) |
| R3-235870 | R3-235555 | TP 38.413/38.423：NPN 的 SON 增强 | agreed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235870.zip) |
| R3-235885 | R3-235563 | TP 37.320：删除编者注 | agreed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235885.zip) |

### SON 相关 endorsed（基线 CR / 待批 CR）

| 最终文稿 | 原稿 | 内容/议题 | 结论 | 下载 |
|---|---|---|---|---|
| R3-235051 | — | BLCR 38.401（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235051.zip) |
| R3-235058 | — | BLCR 38.470（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235058.zip) |
| R3-235065 | — | BLCR 37.320（NPN MDT） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235065.zip) |
| R3-235077 | — | BLCR 36.300（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235077.zip) |
| R3-235078 | — | BLCR 36.423（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235078.zip) |
| R3-235079 | — | BLCR 37.340（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235079.zip) |
| R3-235080 | — | BLCR 38.300（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235080.zip) |
| R3-235081 | — | BLCR 38.413（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235081.zip) |
| R3-235082 | — | BLCR 38.423（MDT） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235082.zip) |
| R3-235083 | — | BLCR 38.423（SON） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235083.zip) |
| R3-235726 | R3-235084 | BLCR 38.473（SON） | endorsed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235726.zip) |
| R3-235116 | — | BLCR 38.420（RACH Indication） | endorsed | [Docs](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Docs/R3-235116.zip) |
| R3-235725 | R3-235133 | BLCR 38.413（MDT） | endorsed | [Inbox](https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_121-bis/Inbox/R3-235725.zip) |

