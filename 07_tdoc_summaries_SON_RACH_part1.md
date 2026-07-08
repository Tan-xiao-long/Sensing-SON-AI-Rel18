# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 6.4 SON/MDT — RACH 增强（议程 10.2.3）

### R3-234643 LS on RACH enhancement
- **来源**: RAN3 (联络人: Huawei, Hongzhuo Zhang)
- **类型**: LS(发给 RAN2 的联络函，非回复某具体来函)；不直接修改规范，涉及 RA Report (TS 38.331) 及 RACH 分区配置相关的潜在增强
- **会议结论**: agreed
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core) 下的 RACH 优化

#### 内容总结
**背景与问题**：Rel-17/18 中 NR 引入了 RACH 分区(RACH partitioning)：不同特性组合(feature combination，如 RedCap、切片、SDT、覆盖增强等)可映射到不同的前导/RACH 资源分区。RACH 优化 SON 功能依赖网络取回 UE 记录的 RA Report 来评估和调整 RACH 配置。但 RA Report 的取回可能滞后于其生成，**如果 gNB 在此期间修改了 RACH 配置(例如 RACH 分区配置)，网络取回 RA Report 时就无法把报告与 UE 记录当时实际生效的 RACH 配置对应起来**，导致优化依据失真。RAN3 在本次会议讨论了解决该关联问题的三个备选方案，但未能达成共识，故发 LS 征询 RAN2 意见。

**LS 陈述的三个备选方案 (Alt1/2/3)**：
- **Alt1**：在 RA Report 中增加 UE 触发 RACH 接入时所用特性组合(feature combination)中**每个特性的优先级(feature priority)**。这使 NG-RAN 能判断是否需要针对"不同优先级的特性被组合到同一 RACH 分区"的方式进行优化。
- **Alt2**：在 RA Report 中增加 **RACH 分区配置信息**，具体为生成该 RA Report 的分区的**起始前导索引(start preamble index)和分区内前导个数(number of preambles)**。这使 NG-RAN 能直接确定当时使用的 RACH 分区。
- **Alt3**：在 RA Report 中增加**从触发生成 RA Report 的 RACH 接入到该 RA Report 被取回之间的时间**。若 NG-RAN 保存了历史 RACH 分区配置、特性优先级与特性组合的时间记录，则可利用该时间倒推出当时生效的 RACH 配置、特性优先级和特性组合。

**行动请求**：请 RAN2 就上述三个备选方案的**可行性(feasibility)及其偏好**提供反馈——因为三个方案都涉及对 UE 侧 RA Report 内容(TS 38.331 定义)的扩充或对 UE 行为的要求，属 RAN2 职责范围。

**与 SON 的关系**：该 LS 体现 RACH 自优化闭环中"报告与配置版本对齐"这一实际部署问题：只有当 RA Report 能与生成时刻的 RACH 分区/特性组合配置正确关联，gNB 才能对分区大小、前导分配和特性组合策略做出正确的自优化调整。LS 末尾附 RAN3#121-bis (厦门) 与 #122 (芝加哥) 会议日期。

---

### R3-234647 (TP for SON BLCR for TS 36.423): Remaining issues for RACH optimisation
- **来源**: Huawei (rev of R3-234068)
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 36.423 (X2AP)。(注：任务清单中标注为 36.300/38.300/38.473，但文稿正文标题与内容均为 TS 36.423 的 X2AP 改动)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI 下的 RACH 优化 (RACH optimisation) 遗留问题

#### 内容总结
**背景与问题**：Rel-18 RACH 优化增强中，UE 在 EN-DC 下可同时收集 E-UTRA RA Report 和 NR RA Report(针对在 en-gNB PSCell 上的随机接入)。eNB 从 UE 取回 NR RA Report 后需要把它转发给服务相应 PSCell 的 en-gNB；但取报告的 eNB 与目标 en-gNB 之间可能没有直接 X2 连接，此时需要允许 eNB 先把 NR RA Report 经 X2 转发给另一个与该 en-gNB 有连接的 eNB，由后者再转发。这要求扩展 X2AP 的 Access and Mobility Indication 过程：一是支持 **eNB 到 eNB** 方向，二是携带用于辨识目标 en-gNB 的 PSCell 列表信息。

**协议改动点 (TS 36.423)**：
1. **8.3.16 Access and Mobility Indication 过程**：总体描述改为"在 E-UTRAN 节点之间传递接入与移动性相关信息"；除原有 eNB→en-gNB 流程图外，新增 **eNB1→eNB2** 的流程(新增图 8.3.16.2-2)，并新增流程文字：eNB1 向 eNB2 发送 ACCESS AND MOBILITY INDICATION 消息；若消息中包含 **PSCell List Container IE**，eNB2 可据此**识别应把 RA Report Container 转发给哪个 en-gNB**。异常情况不适用。
2. **9.1.2.50 ACCESS AND MOBILITY INDICATION 消息**：适用方向扩展为 "eNB → en-gNB, eNB1 → eNB2"。消息含 Message Type (M, YES/reject) 和 NR RACH Report List (0..1, YES/ignore)；列表项 (1..maxnoofRACHReports, EACH/ignore) 原有：NR RACH Report Container (M, OCTET STRING，承载 TS 38.331 §6.2.2 定义的 RACH-ReportList-r16)、UE Assistant Identifier (O, en-gNB UE X2AP ID 9.2.100)；**新增可选 IE "PSCell List Container"**(O, OCTET STRING, criticality YES/ignore)，承载 TS 36.331 中定义的 PSCell 列表 IE——其具体名称和所在子条款标注为 FFS，待 RAN2 确定(即 UE 在 E-UTRA RA Report 中随 NR RA Report 一起上报的关联 PSCell 列表)。

**与 SON 的关系**：该改动补齐了 EN-DC 场景 RACH 自优化的信息回传链路：即使取回 NR RA Report 的 eNB 与 PSCell 所属 en-gNB 无直接接口，报告也能经中转 eNB 送达，使 en-gNB 能基于 UE 实际随机接入经历(前导发送次数、竞争冲突等)优化其 PRACH 资源配置，属于 SON RACH 优化功能在网络接口侧的遗留问题收尾，与同次会议的 36.300/38.300/37.340 Stage-2 TP (R3-234649/234650/234695) 相配套。

---

### R3-234649 (TPs for SON BLCR for TS 36.300): Remaining issues for RACH optimisation
- **来源**: Huawei
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 36.300 (E-UTRAN Stage-2)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI 下的 RACH 优化遗留问题

#### 内容总结
**背景与问题**：TS 36.300 第 22.4.3 节描述 E-UTRAN 的 RACH 优化 SON 功能。原文本主要面向 E-UTRA 小区自身的 RACH 参数优化，而 Rel-18 SON/MDT 增强把 EN-DC 场景纳入：UE 在 en-gNB (NR PSCell) 上执行的随机接入所产生的 NR RA Report 由 LTE 侧 eNB 取回后转发给 en-gNB。为此需要在 36.300 的 RACH 优化条款中体现"EN-DC 下 NR 小区"这一新适用范围。本 TP 即对 22.4.3 节做结构化重写与补充。

**具体改动点 (TS 36.300 §22.4.3)**：
1. **新增 22.4.3.1 General**：明确 RACH 优化功能由"UE 上报信息"和"节点间 RACH 参数交换"两类手段支撑，适用对象扩展为：(a) E-UTRA 小区；(b) **EN-DC 情形下的 NR 小区**。
2. **新增 22.4.3.2.1 E-UTRA cell case**(原有内容整理归入)：可优化的 RACH 参数设置包括 RACH 配置(资源单元分配)、RACH 前导划分(dedicated、group A、group B、RSRP 门限、NB-IoT 的 NRSRP 门限与 NPRACH 资源池、EDT)、RACH 退避(backoff)参数、RACH 发射功率控制参数；优化依赖 UE 上报信息以及 eNB 间的 PRACH 参数(NB-IoT 为 NPRACH 参数)交换。收到轮询(polling)信令的 UE 应上报：成功完成 RACH 前发送的前导个数、竞争解决失败情况、BL UE/增强覆盖 UE/NB-IoT UE 启动随机接入时所处的 RSRP(NB-IoT 为 NRSRP)等级、以及 EDT 回退指示；使用控制面 CIoT EPS 优化的 NB-IoT UE 不支持 RACH 信息上报。
3. **新增 22.4.3.2.2 NR cell in EN-DC case**：适用于支持 EN-DC 的 en-gNB。其 RACH 优化依赖 UE 上报的 RACH 信息报告(见 TS 38.300)——该报告先在 eNB 侧获得、再**转发给 en-gNB**——以及 en-gNB 与 eNB 之间的 PRACH 参数交换(见 TS 38.300)；并明确 **eNB 可按 TS 37.340 的规定取回并转发 NR RA Report**。

**与 SON 的关系**：这是 Stage-2 层面的文字增强，不定义新消息，但为 X2AP 侧 Access and Mobility Indication 扩展(R3-234647)和 37.340 的 RA Report 取回/转发流程(R3-234695)提供总体架构描述，使 LTE 锚点网络能够参与 NR 辅节点小区的 RACH 自优化闭环(采集 UE 随机接入统计→回传给拥有该 PSCell 的节点→调整 PRACH 配置)，完善 EN-DC 下 SON RACH 优化功能。

---

