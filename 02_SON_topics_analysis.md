# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 3. SON 议题详细分析（AI 10）

### 3.0 工作项背景

Rel-18 SON/MDT 增强 WI 是 Rel-16/Rel-17 "SON/MDT 数据收集增强"的延续（WID RP-231157），本阶段目标特性包括：

- **SHR/SPR**：成功切换报告（Successful Handover Report）扩展到 NR→LTE 的系统间切换；新引入成功 PSCell 变更报告（Successful PSCell Change Report，SPR/SPCR），覆盖 NR-DC 下 SN/MN 发起的经典 PSCell 变更、CPC（条件 PSCell 变更）与 CPA（条件 PSCell 添加）；
- **MRO 增强**：面向 CPAC（条件 PSCell 添加/变更）失败场景、快速 MCG 恢复失败、NR→E-UTRAN 语音回落切换失败、MR-DC SCG 失败的移动鲁棒性优化；
- **RACH 增强**：RACH 分区（feature combination）信息上报、RACH 报告获取的网络侧方案（gNB-DU→gNB-CU 的 RACH INDICATION 新过程、SN→MN 的可用性指示）、MR-DC 场景 SN RACH 报告转发；
- **NPN 的 SON/MDT**：PNI-NPN（CAG）与 SNPN 场景下 MDT 区域范围、用户同意（user consent）处理；
- **SON for NR-U**：免许可频段下 MLB/MRO 所需的信道占用等负载信息交互；
- **MDT 增强**：信令型记录 MDT 的跨 RAT 覆盖保护。

### 3.1 子议程 10.1：基线 CR（11 篇 endorsed）

本次会议将 Rel-18 SON/MDT 特性所涉全部接口规范的基线 CR 重新 endorse（多数为版本刷新或吸收上次会议 agreed TP 后的重提），覆盖 NGAP（38.413，SON 与 MDT 各一篇）、XnAP（38.423，SON 与 MDT 各一篇）、X2AP（36.423）、F1AP（38.473）、F1 总体（38.470）、NG-RAN 架构（38.401）以及 Stage 2 规范 36.300/38.300/37.340。各 BL CR 的详细内容见 §6 逐篇总结，其分工可概括为：

- **Stage 2 层**（36.300/38.300/37.340）：定义 SHR 系统间扩展、SPR/SPCR、CPAC MRO 场景与失败类型定义、语音回落失败检测、RACH 上报增强等特性行为；
- **NGAP（38.413）**：MDT 相关（NPN 区域范围、跨系统追踪）与 SON 相关（系统间 SON 信息传递、语音回落切换报告）改动；
- **XnAP（38.423）**：SHR/SPR 转发、CPAC MRO 信息交互、RACH 报告转发与可用性指示等；
- **F1AP（38.473）/38.470**：gNB-DU 与 gNB-CU 间的 RACH 上报（RACH INDICATION）等 split 架构支撑；
- **X2AP（36.423）**：EN-DC 场景对应增强。

### 3.2 子议程 10.2.1：SHR 与 SPR

**会议达成的主要共识（agreements）**：

- SPR 触发与优化归属细化：SN 发起的经典 PSCell 变更中，源 SN 决定 T310/T312 触发门限、目标 SN 决定 T304 门限；CPA 及 MN/SN 发起的 CPC 由目标 SN 决定 T304 触发并做根因分析；SN 内部 PSCell 变更由源 SN 决定 T310/T312 触发并做根因分析；
- 若触发原因为 T310/T312，SPR 优化目标是源 PSCell 底层问题与 PSCell 变更配置；MN 发起场景下由 MN 优化变更配置与门限、源 SN 优化底层定时器；
- SPR 由"新节点"取回时，一律先送回"旧 MN"，由旧 MN 转发至应执行优化的节点；为此复用 XnAP/F1AP 的 ACCESS AND MOBILITY INDICATION 与 NGAP 的 Uplink/Downlink RAN Configuration Transfer 过程转发 SPR；旧 MN 借助存储的 SN Mobility Information 定位旧源/目标 SN 的 UE 上下文（SN 发起场景经 SN Change Required / SN Addition Request Acknowledge 获取，MN 发起场景经 SN Release Request Acknowledge / SN Addition Request Acknowledge 获取）；
- 系统间 SHR（NR→LTE）：T310/T312 触发纳入考虑；有用参数包括源 NR 小区、目标 LTE 小区、源/目标/邻区测量结果、触发原因、UE 位置信息，发 LS 请 RAN2 确认（即 agreed 的 R3-234716）；SHR 转发采用"方案 3"（取回节点做初步分析后转发给产生触发条件的节点）；
- 反向系统间 SHR（LTE→NR，T304 触发）在不影响 LTE 规范的前提下于 Rel-18 支持：目标 gNB 经 MobilityFromEUTRACommand 的 NR 容器下发 SHR 配置、UE 以 NR 格式记录并只向 gNB 上报，请 RAN2 确认（并入 R3-234716）；
- SPCR 内容（源/目标 PSCell 信息、原因、最新测量结果等）与 RAN2 并行讨论，RAN2 已定内容不再重复发 LS。

**agreed 文稿**：R3-234716（Reply LS on SHR and SPR，详见 §6）。

### 3.3 子议程 10.2.2：MRO

**会议达成的主要共识**：

- **CPAC MRO**：在 MN 收到 SCGFailureInformation 后由 MN 做初步分析（区分 CPA/CPC、MN/SN 发起）；将 CPC 候选小区列表及执行条件纳入 MN→源 SN 的消息（后续落入 R3-234665 的 Xn 改动）；CPAC 的 MRO 事件定义将在 TS 37.340 新章节引入；UE 上报首个触发的 CPAC 事件及两次触发事件间时长；沿用 R17 信令机制经 Xn 从 MN 向源/末服务 SN 上报 CPA/CPC 失败信息；
- **快速 MCG 恢复 MRO**：UE 至少上报 SCG 失败发生的 PSCell、快速 MCG 恢复失败原因（T316 超时、SCG 失败、SCG 去激活等）及 SCG 失败类型（t310-Expiry、randomAccessProblem、rlc-MaxNumRetx）；场景 a 重定义为"T316 运行期间 SCG 失败"；是否支持 pre-R18 UE 待 RAN2 进展；
- **语音回落 MRO**：将此前的工作假设升级为正式共识——"在 S1/NG 的系统间切换报告中定义新的切换报告类型"，即 agreed 的 R3-234625 所落地的 "Inter-system mobility failure for voice fallback"；RLF 报告需指示最近一次系统间切换因语音回落触发（RAN2 已决定在 LTE RLF 报告中引入语音回落指示）；
- **UHI for CPAC**：为条件 PSCell 变更引入 UE 历史信息（UHI）记录的 Stage 2 描述（agreed 的 R3-234666），并明确 CPAC 配置期间 S-NODE ADDITION REQUEST 中源 PSCell UHI 的 Time Stay 值不能精确反映驻留时长的问题。

**agreed 文稿**：R3-234665（XnAP CPAC MRO TP）、R3-234625（NGAP 语音回落新切换报告类型 TP）、R3-234666（37.340 UHI for CPAC TP），详见 §6。

### 3.4 子议程 10.2.3：RACH 增强

**会议达成的主要共识**：

- 确认网络侧 RACH 报告获取方案：在 F1 上定义新的 Class 2 非 UE 关联消息（RACH INDICATION），由 gNB-DU 向 gNB-CU 指示其不可见的成功 RACH 事件（波束失败恢复、无 PUCCH 资源、上行失步等触发）；在 Xn 上定义对应的非 UE 关联 RACH INDICATION，使 S-NG-RAN 节点告知 M-NG-RAN 节点 UE 存在可取回的 RACH 报告；
- SN RACH 报告转发：当取回报告的节点与报告涉及 PSCell 所属节点间无 X2/Xn 连接时，是否及如何转发留给 gNB 实现；
- RA 报告增强的候选方案收敛：就"上报 RACH 分区配置信息（Opt2）"与"上报 RACH 接入到上报之间的时间（Opt3）"两个方向连同 RAN3 分析发 LS 请 RAN2 评估可行性与偏好（Opt1 特性优先级 FFS）——即 agreed 的 R3-234643；
- 不考虑 RA 报告经 NG/S1 转发。

**agreed 文稿**：R3-234643（LS 致 RAN2）、R3-234647 / R3-234649 / R3-234650 / R3-234695（分别面向 36.423【注：文稿内容实为 X2AP 改动】、36.300、38.300、37.340 的 RACH 遗留问题 TP）、R3-234742（38.420 引入 RACH Indication）、R3-234743（38.423 RACH 增强），详见 §6。

### 3.5 子议程 10.2.4：NPN 的 SON/MDT 增强

**会议达成的主要共识**：

- MDT SNPN 列表最大数目定为 16；不引入 SNPN-wide 区域范围；
- 此前会议已定框架延续：为 MDT 区域范围引入 CAG 列表（choice 结构内外各一处）、增加 SNPN Cell Based / SNPN TAI Based 区域范围、maxnoofCAGforMDT=256、接口上无需传递 SNPN 用户同意；
- 向 RAN2/SA5 发 LS 通报 RAN3 进展并附 37.320/38.413 基线 CR（agreed 的 R3-234744）；针对用户同意问题的另一 LS 草稿（R3-234721）被 noted 未发出。

**agreed/endorsed 文稿**：R3-234718（38.413 的 MDT NPN TP）、R3-234719（38.423 的 MDT NPN TP）、R3-234744（LS 致 RAN2/SA5）、R3-234720（37.320 NPN MDT 基线 CR，endorsed unseen），详见 §6。

### 3.6 子议程 10.2.5：SON for NR-U

**会议达成的主要共识**：

- 在 XnAP RESOURCE STATUS UPDATE 与 F1AP RESOURCE STATUS UPDATE 消息中引入按 NR-U 信道粒度的可选负载指标（Radio Resource Status per NR-U Channel）；
- 无需在 F1AP RESOURCE STATUS UPDATE 中传递 UL EDT。

**agreed 文稿**：R3-234544（38.423 NR-U MLB TP）、R3-234545（38.473 NR-U MLB TP），详见 §6。

### 3.7 子议程 10.2.6：MDT 增强（无 agreed 产出）

关于信令型记录 MDT 覆盖保护，会议仅确认既有理解（R17 保护特性仅适用于 NR 内重选、Intra-5GS），跨 RAT 记录 MDT 上报及 LTE 记录 MDT 报告转发待 RAN2 进展；Nokia 的优先级配置提案与 ZTE 的 NGAP 新原因值提案均被 noted，未形成结论。

---
