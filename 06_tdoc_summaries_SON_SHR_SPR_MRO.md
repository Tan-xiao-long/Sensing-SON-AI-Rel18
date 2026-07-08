# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 6.2 SON/MDT — SHR 与 SPR（议程 10.2.1）

### R3-234716 Reply LS on SHR and SPR
- **来源**: RAN3 (联络人: Huawei, Henrik Olofsson)
- **类型**: LS(回复联络函)，回复 R3-233718/R2-2306896；不直接修改规范，涉及 Rel-18 SON/MDT 中 SHR/SPR 相关的 Stage-2/3 后续工作
- **会议结论**: agreed
- **所属议题**: 议程 10.2.1，Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core) 下的 SHR/SPR (成功切换报告/成功PSCell变更报告) 相关 MRO 增强

#### 内容总结
本文是 RAN3 在 #121 会议上批准的、发给 RAN2 的回复 LS，回应 RAN2 在 R2-2306896 (RAN3 编号 R3-233718) 中就 SHR (Successful Handover Report，成功切换报告) 和 SPR (Successful PSCell change/addition Report，成功 PSCell 变更/添加报告) 提出的问题。

背景是 Rel-18 SON/MDT 增强工作中，RAN2 定义了 UE 侧的 SHR/SPR 记录与上报机制，其中涉及网络侧哪个节点负责配置触发条件、以及跨 RAT 场景下报告如何在网络节点间关联和传递等问题，需要 RAN3 从网络接口(Xn/X2/NG)角度给出结论。

LS 传达了 RAN3 达成的两点共识：

1. **关于 SPR**：对于 MN 发起的 PSCell change (主节点发起的辅小区组主小区变更)，RAN3 认为由 **MN 来决定基于 T310/T312 定时器的 SPR 触发条件**是有益的。同时 RAN3 说明仍在继续讨论：MN 在确定这些触发门限时，是否还需要源 SN 通过 Xn 接口提供进一步的辅助信息(即源 SN 是否要把与 T310/T312 相关的信息传给 MN)，这一点尚无结论。

2. **关于 inter-RAT SHR (NR 到 LTE 的跨系统切换成功报告)**：RAN3 认为在"成功切换后不久即发生失败"的场景下，把 SHR 与 RLF Report (无线链路失败报告) 进行**关联(correlation)** 是有价值的，这有助于 MRO 识别"太晚切换/太早切换"等根因。为实现该关联，RAN3 同意让 UE 在 SHR 中上报：(a) 一个 **C-RNTI**(可以来自源小区或目标小区)，以及 (b) **从收到切换命令到该事件上报之间的时间**。至于具体采用源小区 C-RNTI 还是目标小区 C-RNTI，RAN3 把决定权交给 RAN2。

行动请求(Action)为：请 RAN2 在后续工作中考虑上述反馈。这体现了 SON MRO 功能中网络侧利用 UE 报告(SHR/SPR/RLF Report)进行移动性参数自优化的典型跨工作组协作：RAN2 负责 UE 记录/上报的 RRC 细节，RAN3 负责节点间信息交互和报告关联机制。LS 末尾还附了 RAN3 下两次会议(#121-bis 厦门、#122 芝加哥)的日期。

---


## 6.3 SON/MDT — MRO（议程 10.2.2）

### R3-234665 (TP for SON BLCR for 38.423) SON enhancements for CPAC
- **来源**: Samsung, Cybercore (rev of R3-233933)
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 38.423 (XnAP)。(注：会议议程曾标注 38.423/37.340，但最终批准版本仅含 Annex 3 即 TS 38.423 的 TP)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.2，Rel-18 SON/MDT WI 下的 MRO 子议题——CPAC (Conditional PSCell Addition/Change，条件PSCell添加/变更) 的 SON/MRO 增强

#### 内容总结
**背景与问题**：Rel-18 SON/MDT 工作项将 MRO 范围扩展到 CPAC。当 UE 在 CPAC 场景下发生 SCG 失败(如 PSCell 变更过早、过晚或变到错误小区)时，MN 会通过 XnAP 的 SCG FAILURE INFORMATION REPORT 消息把失败信息转给"上一次为 UE 服务的 S-NG-RAN 节点"以便其做根因分析。但要正确分析 CPAC 相关失败，做出 CPAC 配置决策的节点还需要知道当时给 UE 配置的候选小区集合和执行条件，本 TP 即为此在 Xn 上引入 CPAC 配置信息的传递。

**协议改动点 (TS 38.423)**：
1. **9.1.2.29 SCG FAILURE INFORMATION REPORT 消息**(M-NG-RAN node → S-NG-RAN node)中新增一个可选 IE：**CPAC Configuration** (9.2.2.xx，criticality: YES/ignore)，与既有的 Source PSCell CGI、Failed PSCell CGI、SCG Failure Report Container、SN Mobility Information 等 IE 并列。
2. **新增 9.2.2.xx CPAC Configuration IE**，承载 CPC 或 CPA 的配置信息，结构为：
   - CPAC Candidate Cell List → CPAC Candidate Cell Item (1..maxnoofPSCellsinCPAC，**取值 8**)；
   - 每个候选小区项含：CPAC Candidate Cell ID (Global NG-RAN Cell Identity, 9.2.2.27，必选) 和 CPAC Execution Condition List → CPAC Execution Condition Item (1..maxnoofCPACexecutioncond，**取值 2**)；
   - 每个执行条件项含两个必选 OCTET STRING 容器：**MeasObject Container**(携带 TS 38.331 RRCReconfiguration 中为该候选小区配置的 MeasObjectToAddMod)和 **ReportConfig Container**(携带对应的 ReportConfigToAddMod)，即以 RRC 容器方式透传 CPAC 执行条件(如 CondEvent A3/A5 的测量对象与上报配置)。
3. **ASN.1 改动**：在 XnAP-PDU-Contents 的 ScgFailureInformationReport-IEs 中增加 { id-CPACConfiguration, ignore, CPACConfiguration, optional }；在 XnAP-IEs 中新增 CPACConfiguration、CPACCandidateCell-List/-Item、CPACExecutionCondition-List/-Item 等类型定义；在常量部分新增 maxnoofPSCellsinCPAC ::= 8、maxnoofCPACexecutioncond ::= 2，以及新的 ProtocolIE-ID id-CPACConfiguration (编号待定 xxx)。

**与 SON 的关系**：该增强使接收 SCG 失败报告的节点(通常是配置了 CPAC 的源 SN 或 MN)能把 UE 上报的 SCGFailureInformation 与当时的 CPAC 候选小区/执行条件对照，判断失败是由于执行条件门限设置不当、候选小区选择不当等原因，从而实现 CPAC 参数的移动性鲁棒性自优化 (MRO)，是 Rel-18 将传统 PSCell change MRO 扩展到条件式移动性的关键 Stage-3 改动之一。

---

### R3-234666 (TP for SON BLCR for 37.340) UHI for CPAC
- **来源**: Samsung, Ericsson, Nokia, Nokia Shanghai Bell, Cybercore
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 37.340 (MR-DC Stage-2)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.2，Rel-18 SON/MDT WI 下的 MRO 子议题——UE History Information (UHI) 在 CPAC/CHO 场景下的增强

#### 内容总结
**背景与问题**：SCG UE History Information (SCG UHI) 记录 UE 依次驻留过的 PSCell 及在每个 PSCell 中的停留时长，是网络进行移动性优化(如乒乓检测、切换/PSCell 变更参数调整)的重要 SON 输入。Rel-17 已引入 SCG UHI 的收集与传递，但在**条件式移动性**(CHO 条件切换、CPC 条件 PSCell 变更)场景下存在计时空口问题：条件配置从"准备"到 UE "实际执行接入"之间可能间隔较长时间，若目标节点简单沿用准备时刻收到的停留时长，最后一个 PSCell 条目的"停留时间"会明显偏短，导致 SON 统计失真。本 TP 在 TS 37.340 第 13.3 节 (SCG UE history information) 中补充针对 CHO 与 CPC 的时长更新规则。

**关键技术方案/具体改动 (TS 37.340 §13.3)**：
1. 维持既有框架：MN 存储并关联来自 MN 与 SN 的 UHI，并把 UHI (及可选的来自 UE 的 UHI) 转发给所连 SN；SN 负责收集 SCG UHI，并在 SN Release、SN 发起的 SN Change、MN 请求时的 MN 发起 SN Modification、以及(若在 SN Addition 时订阅)PSCell 变更时的 SN 发起 SN Modification 等过程中提供给 MN；UE 在同一 PSCell 停留超过 Time Stay 最大值时可用同一 PSCell 标识的连续条目累计。
2. **新增 CHO 场景规则**：当目标 NG-RAN 节点在 CHO 的 Handover Request 消息中收到源节点提供的 SCG UHI 后，在 UE 成功接入目标节点的候选小区时，目标节点应**更新最新一条 PSCell 条目(即源 PSCell)的停留时长**：更新值 = 切换准备时从源节点收到的值 + 从收到 Handover Request 到收到 UE 的 RRC Reconfiguration Complete 之间经历的时间。
3. **新增 CPC 场景规则**：当目标 SN 通过 SN Addition Request 从 MN 收到 SCG UHI 后，在 UE 成功接入目标 SN 的候选小区时，目标 SN 同样更新最新 PSCell 条目的停留时长：更新值 = SN Addition Request 中收到的值 + 从收到 SN Addition Request 到收到 MN 发来的 SN Reconfiguration Complete 之间的时间。

**与 SON 的关系**：该 TP 属 Stage-2 文字性增强，不新增消息或 IE，而是规范条件式移动性下 UHI 停留时长的口径，保证 CHO/CPC 执行延迟被计入源 PSCell 停留时间，使 SCG UHI 在 CPAC 时代仍能准确反映 UE 移动轨迹，为 MRO、乒乓抑制和候选小区优选等 SON 功能提供可靠数据基础。

---

### R3-234625 (TP for SON BL CR 38.413) Introduce a new handover report type for inter-RAT voice fallback
- **来源**: CATT, Nokia, Nokia Shanghai Bell, ZTE, Samsung
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 38.413 (NGAP)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.2，Rel-18 SON/MDT WI 下的 MRO 子议题——inter-system (跨系统) 语音回落 (EPS fallback for voice) 移动性失败的 MRO

#### 内容总结
**背景与问题**：Rel-18 SON/MDT 将 MRO 扩展到跨系统语音回落场景：UE 在 NR 上发起语音业务后被切换/回落到 E-UTRAN (EPS Fallback)，若该跨系统切换失败(UE 在目标 LTE 小区失败并可能重连到其它小区)，NR 侧节点需要获知失败信息以便优化语音回落相关的切换参数。由于失败信息可能经由 EPC/5GC 跨系统传递，需要在 NGAP 的 Inter-system SON 信息传递框架(UPLINK/DOWNLINK RAN CONFIGURATION TRANSFER 中的 Inter-system HO Report)中新增报告类型。本 TP 落实 RAN3#121 达成的相关协议。

**协议改动点 (TS 38.413)**：
1. **9.3.3.40 Inter-system HO Report IE**：其 CHOICE Handover Report Type 原有两个分支(Too early Inter-system HO、Inter-system Unnecessary HO)，新增第三分支 **"Inter-system Mobility Failure for Voice Fallback"**(经 CHOICE 扩展分支引入，criticality YES/ignore)，包含：
   - **Source Cell ID** (M，NG-RAN CGI 9.3.1.73)：切换的源 NR 小区；
   - **Failure Cell ID** (M，E-UTRA CGI 9.3.1.9)：切换失败的目标 LTE 小区；
   - **Re-connect Cell ID** (O，E-UTRA CGI)：UE 失败后重连的 E-UTRA 小区，**名称尚标注 FFS**；
   - **UE RLF Report Container** (O，9.3.3.41)：UE 的 RLF 报告容器，**presence 尚标注 FFS**。
2. **ASN.1 改动 (9.4.5/9.4.7)**：InterSystemHandoverReportType CHOICE 通过 choice-Extensions 的 ProtocolIE-SingleContainer 增加 { id-intersystemMobilityFailureforVoiceFallback, ignore, IntersystemMobilityFailureforVoiceFallback, mandatory }；新增 SEQUENCE 类型 IntersystemMobilityFailureduringVoiceFallback { sourcecellID NGRAN-CGI, targetcellID EUTRA-CGI, reconnectCellID EUTRA-CGI OPTIONAL(FFS), uERLFReportContainer OPTIONAL(FFS), iE-Extensions } (文中类型名 during/for 拼写尚不一致，属编辑遗留)；常量部分新增 id-intersystemMobilityFailureforVoiceFallback ProtocolIE-ID ::= xxx (编号待定)。

**与 SON 的关系**：借助该新报告类型，检测到语音回落切换失败的 LTE 侧(经 MME→AMF 的 Configuration Transfer 通道)可把失败小区、重连小区及 UE RLF Report 回传给做出回落决策的 NG-RAN 源节点，源节点据此区分"回落目标选择不当/触发过早或过晚"等根因，自优化 EPS FB 目标小区选择与切换参数，属于 Rel-18 MRO 对跨系统语音连续性场景的补强。文中若干 FFS (重连小区 IE 命名、RLF 容器的存在性) 留待后续会议解决。

---
