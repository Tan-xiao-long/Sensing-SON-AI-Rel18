# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-234650 (TP for SON BLCR for TS 38.300): Remaining issues for RACH optimisation
- **来源**: Huawei
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 38.300 (NR Stage-2)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI 下的 RACH 优化遗留问题

#### 内容总结
**背景与问题**：TS 38.300 第 15.5.3 节描述 NR 的 RACH 优化 SON 功能。Rel-17 已支持 UE 记录 RA Report 并由网络取回，但在 MR-DC 场景存在遗留问题：UE 在 SN (PSCell) 侧执行的某些随机接入(如波束失败恢复、上行失步、调度请求失败等)只有 SN 知晓，而 RA Report 只能由 MN 通过 SRB1 从 UE 取回，MN 并不知道 UE 中已产生了可取回的 RA Report。Rel-18 为此引入 SN→MN 的 "RACH 指示 (RACH indication)" 机制。本 TP 更新 38.300 §15.5.3 的 Stage-2 描述。

**具体改动点 (TS 38.300 §15.5.3)**：
1. 文字整理：明确 RACH 优化由 UE 按 TS 38.331 上报的信息(在 NG-RAN 节点获得)和 NG-RAN 节点间的 PRACH 参数交换支撑；RA Report ("RACH information report"改为规范措辞) 内容包括：每次 RACH 尝试的竞争检测指示、按时间顺序列出的各次尝试所选 SSB 索引及在每个 SSB 上发送的前导数、每次尝试所选 SSB 是否高于/低于配置的 RSRP 门限的指示、以及 TS 38.331 §5.7.10.4 规定的 2-step RACH 信息。
2. **SN RA Report**：修订原"SgNB RACH information report"的表述，明确 **NR-DC 下 UE 可支持在 SN 的 PSCell 上收集 RA Report**；NGEN-DC 情形下 RA Report 的取回与转发在 TS 37.340 中规定。
3. **新增双连接下 RA Report 取回的描述**：在 MR-DC 中，当 UE 在 SN 侧成功完成随机接入过程时，**SN 可通过 "RACH indication" 告知 MN "UE 中可能存在可用的 RA Report"**；MN 随后可基于经 **XnAP 信令**从 SN 收到的 RACH indication，去 UE 取回 RA Report。

**与 SON 的关系**：该 TP 与 XnAP 侧引入 RACH INDICATION 消息的 R3-234743、38.420 增加过程列表的 R3-234742 配套，构成 Rel-18 RACH 优化增强的 Stage-2 总述：解决了"SN 侧随机接入事件对 MN 不可见导致 RA Report 无法及时取回"的问题，使 MR-DC 下 SN 小区的 RACH 相关配置(SSB/前导资源、门限等)也能纳入基于 UE 真实接入体验的 SON 自优化闭环。

---

### R3-234695 (TP for SON BLCR for TS 37.340): Remaining issues for RACH optimisation
- **来源**: Huawei
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 37.340 (MR-DC Stage-2)
- **会议结论**: agreed
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI 下的 RACH 优化遗留问题

#### 内容总结
**背景与问题**：MR-DC 下与 RACH 优化相关的两个遗留问题需要在 TS 37.340 中补充 Stage-2 描述：其一，UE 在 SN 侧发生的部分随机接入(波束失败恢复、上行失步、调度请求失败、无可用 PUCCH 资源等触发)只有 SN 知晓，MN 无从得知 UE 已生成 RA Report，需要 SN→MN 的指示机制；其二，EN-DC/NGEN-DC 下 eNB/ng-eNB 从 UE 取回 NR RA Report 后，可能与服务相应 PSCell 的 (en-)gNB 没有直接接口，需要定义经中间节点的转发路径。本 TP 在 37.340 新增 10.18.C "RA Report retrieval" 一节。

**具体改动点 (TS 37.340 §10.18.C，新增条款)**：
1. **RACH indication 机制**：在 MR-DC 中，当 UE 执行了**仅 SN 可知**的成功随机接入(示例列举：beam failure recovery、UL 同步问题、scheduling request failure、无 PUCCH 资源可用)时，SN 可通过 **RACH indication** 通知 MN 在 SN 中发生了成功的随机接入过程；MN 随后可基于从 SN 收到的 RACH indication，向 UE(可为多个 UE)发起 RA Report 取回。
2. **EN-DC/NGEN-DC 下 NR RA Report 的取回与关联**：UE 在 EN-DC 和 NGEN-DC 下可在 MN、SN 分别执行 RACH 时收集 E-UTRA RA Report 和 NR RA Report；E-UTRAN 节点取回 E-UTRA RA Report 时可**同时请求 UE 包含 NR RA Report**；若有，UE 将 NR RA Report 以容器方式连同**与其关联的 PSCell 列表**一起置于 E-UTRA RA Report 内上报；取回的 E-UTRAN 节点再把它转发给服务这些 PSCell 的相应 SN。
3. **无直接接口时的中转转发**：NGEN-DC 情形，若取回 NR RA Report 的 ng-eNB 与 UE 所指示 PSCell 的服务 gNB 之间没有 Xn 连接，ng-eNB 可**经 Xn 把 NR RA Report 转发给一个与该 gNB 相连的 ng-eNB**(由其继续转发)；EN-DC 情形对应地：eNB 可经 **X2** 把 NR RA Report 转发给与目标 en-gNB 相连的另一 eNB。

**与 SON 的关系**：本 TP 把 RACH 自优化所需的 UE 报告获取链路在 MR-DC 各形态下补齐——SN 触发的 RACH indication (对应 XnAP 新消息 RACH INDICATION，见 R3-234742/234743) 解决"报告存在性不可见"问题，PSCell 列表与多跳转发解决"报告送达正确优化节点"问题——确保拥有 PSCell 的节点最终获得 UE 的 RA Report 用于 PRACH 参数自优化，与 36.300/38.300/36.423 各 TP 共同构成完整方案。

---

### R3-234742 (TP for SON BLCR for TS 38.420): Introduction of RACH Indication
- **来源**: Huawei, China Telecom, CMCC, Ericsson, ZTE
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 38.420 (Xn 通用方面与原则, Xn general aspects and principles)
- **会议结论**: agreed unseen (未经会上逐条审阅直接批准)
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI 下的 RACH 优化

#### 内容总结
**背景与要解决的问题**：Rel-18 RACH 优化增强中，RAN3 同意在 MR-DC 场景引入 SN→MN 的 "RACH Indication" 机制：当 UE 在 SN 侧完成仅 SN 可知的成功随机接入(如波束失败恢复、上行失步、调度请求失败等触发的 RACH)时，SN 通过 Xn 向 MN 指示 UE 中可能存在可取回的 RA Report，MN 据此从 UE 取回报告并转发，支撑 SN 小区的 RACH 参数自优化。该机制在 Stage-3 体现为 XnAP (TS 38.423) 新增 RACH INDICATION 消息/过程(见配套文稿 R3-234743)。按照规范体系要求，Xn 接口的总体规范 TS 38.420 中列举 Xn-C 支持的各类功能/过程清单，也需同步把新过程补入，本 TP 即完成这一配套性(mirror)修改。

**具体改动点 (TS 38.420 §6.2.9 "Data exchange for self-optimisation procedures")**：该节描述"用于自优化的数据交换过程"，其作用是在 NG-RAN 节点间传递失败、接入和移动性相关信息以支撑自优化。修改内容为：
1. 在该节引言句中把传递的信息范围表述为"failure, access and mobility related information"(加入 access，覆盖随机接入类信息)；
2. 在既有过程列表——Failure Indication、Handover Report、Mobility Settings Change、Access and Mobility Indication、SCG Failure Information Report、SCG Failure Transfer——之后**新增列表项 "RACH Indication"**，将其正式登记为 Xn 自优化数据交换过程之一。

本 TP 不定义消息的 IE 结构、方向或触发条件等细节(这些在 TS 38.423 的 TP 中规定)，属于纯 Stage-2/接口总述层面的一致性修改，篇幅很小，因此以 "agreed unseen" 方式获批。

**与 SON 的关系**：TS 38.420 §6.2.9 所列过程正是 Xn 接口上承载 SON 自优化(MRO、RACH 优化等)信息交换的过程集合。把 RACH Indication 纳入其中，标志着"SN 侧随机接入事件向 MN 的可见性通知"正式成为 NG-RAN 自优化功能框架的一部分，与 R3-234650 (38.300)、R3-234695 (37.340) 的 Stage-2 描述和 R3-234743 (38.423) 的 Stage-3 消息定义共同构成 Rel-18 RACH 优化增强的完整规范链条。

---

