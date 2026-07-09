# 3GPP R18 全周期 SON/AI agreed 议题调研（RAN3 #119–#124）

> 本文件为拆分版之一，目录见 00_README.md。

## RAN3#119bis-e (2023.04.17–26, 线上)

### 本次会议 SON/MDT 主要共识与增强内容

**SHR/SPR**
- 确定 SHR/SPR 转发机制：复用 ACCESS AND MOBILITY INDICATION 消息（XnAP/F1AP）及 Uplink/Downlink RAN Configuration Transfer 过程（NGAP），将非源节点取回的 inter-RAT SHR（NR→LTE）转发至源 NR 节点；SPR 转发同样复用上述消息/过程。
- intra-NR SHR 由第三方节点取回时确认 Option 3：接收节点做初步分析后转发给产生触发条件的对应节点。
- 同意支持 LTE→NR 成功切换的 SHR 采集（T304 触发、对 LTE 无影响），原则为：目标 gNB 经 MobilityFromEUTRACommand 的 NR 容器（targetRAT-MessageContainer）下发 SHR 配置，UE 以 NR 格式存储/记录并仅向 gNB 上报；内容至少含 Source LTE cell 与 Target NR cell；发 LS（R3-232140）请 RAN2 确认。
- 确认 NR→LTE SHR 无需包含 RACH 相关信息（RACH 尝试次数、竞争标志），因 RA Report 已有。
- SPR：新节点取回的 SPR 一律先发给 old MN，由其转发给执行优化的节点；为辅助转发，UE 可在 SPR 中包含下发配置的 PCell CGI，WA 加入 MN/SN 发起指示；WA SPR 触发以百分比值表示（类似 SHR）。
- 明确 MN 发起 PSCell change 时 SPR 优化由 MN（PSCell change 配置及门限）与 source SN（T310/T312 定时器等底层问题）共同完成；old MN 存储经 SN Change Required / SN Release Request Ack / SN Addition Request Ack 获得的 SN Mobility Information，随 SPR 一并发给 old source/target SN 用于 UE 上下文识别。
- Stage3 TP agreed：38.423（R3-232002）、38.413（R3-232021）、38.473（R3-232137）。

**MRO**
- 确定在 TS 37.340 新章节中引入 CPAC 的 MRO 事件定义；对应 TP（R3-232062）agreed。
- CPAC UHI：确认 S-NODE ADDITION REQUEST 中源 PSCell UHI 的 Time Stay IE 不反映真实驻留时长，Rel-18 不为 CPAC UHI 引入额外信令（仅 stage2 说明）。
- fast MCG recovery 新增场景：同意处理 Case f1（UE 发送 MCGFailureInformation 之前 SCG 已失败/去激活）与 Case c（near-failure）；场景 a 重定义为"T316 运行期间发生 SCG failure"。
- WA：为支持 pre-Rel-18 UE，MN 向 SN 传递 T316（节省 Uu 资源），细节待续。
- 语音回落 MRO：在 TS 38.300 引入检测机制的 stage2 描述；36.300/38.300/38.423 综合 TP（R3-232151）agreed。

**RACH Enhancements**
- RACH INDICATION 消息细节确定：仅包含 gNB-CU UE F1AP ID，不需要 Random Access Indication IE，RACH indication list IE 的 criticality 为 reject；38.473 TP（R3-232141、R3-232099、R3-232142 等）agreed。
- 命名统一：在 38.300/38.401/38.423/36.423/38.473 中统一采用 "RA report"，与 RAN2 规范对齐（4 份 naming TP agreed）。
- 回复 RAN2 LS（R3-232144）agreed：RAN3 倾向 Alt 1，请 RAN2 澄清相关协议。
- RA report 在 inter-MN 切换下的转发及 RACH 上报优化（feature priority、partition 配置、时间戳、网络控制）留待下次会议。

**NPN**
- PNI-NPN MDT Area Scope 的 XnAP TP（R3-232091，38.423）及 ZTE 38.413/38.423 TP（R3-232027）agreed。
- 发 LS 给 RAN2（R3-232118）：关于公网/非公网分开 MDT report，及 UE 从 SNPN 移动到 PLMN 时 logged MDT report 可能被覆盖的问题。
- 确认 UHI 中是否携带 PNI-NPN 信息由配置和运营商策略决定；NID/PNI-NPN ID 引入 SON/MDT report 取决于 RAN2。
- SNPN Area Scope 方案（"SNPN based"、"SNPN cell based"、"SNPN TA based" CHOICE IE）及 maxnoofCAGforMDT 取值（256 或 12）FFS。

**SON for NR-U**
- NR-U metrics 的 stage3 TP agreed：38.423（R3-232067）与 38.473（R3-232068）。
- MRO：同意增强 RLF report 与 RA report 以区分移动性错误与 LBT 相关错误，可包含 RA 过程中 LBT failure 信息，粒度等细节待 RAN2 进展。
- MLB：WA gNB 经 Xn 资源状态上报的 EDT UL 至少反映为 UE 配置的最大 EDT UL；F1 中 COT percentage UL 的 presence 定为 optional。

**MDT Enhancements**
- 发 LS 给 SA5（R3-232070）：MR-DC 下 MDT 测量采集问题。
- 确认 inter-RAT signalling based logged MDT 覆盖保护包含两个场景：EPC→5GC（inter-system）与 LTE→NR（intra-5GC）。
- 确认 NR 的 management based logged MDT 不得覆盖 LTE 的 signalling based logged MDT；OAM 提供保护指示/新增 NGAP cause 的提案无共识。

### 本次会议 AI/ML 主要共识与增强内容

**Stage2（12.2.1）**
- 将 WA 升级为 agreement 并明确含义：AI/ML 过程为 "data type agnostic"，即不指示数据的用途（input/output/feedback）。
- 引入 Requested Prediction Time 概念：在 AI/ML INFORMATION REQUEST 中为 one-time reporting 配置，定义为"请求预测信息所对应的未来时间点"；是否为时间区间 FFS。
- 周期上报场景下 requested prediction time 需显式信令，细节待续；stage2 TP（R3-232125）本次仅 noted。

**LB（12.2.2.1）**
- Xn 影响 TP（R3-232148，38.423）agreed：引入 NG-RAN node1/node2 Measurement ID 对以标识 AI/ML 信息上报上下文，含 UE Assistant Identifier（细节 FFS）、Predicted Radio Resource Status（细节 FFS）。
- HO 后 UE 性能反馈：确定若 UE performance feedback 仅作为 feedback，则 AI/ML INFORMATION REQUEST 中不需额外显式指示；在 HO REQUEST 消息中引入 Measurement ID 对，与 AI/ML INFORMATION REQUEST 建立关联。
- UE performance feedback IE 结构：在 AI/ML INFORMATION UPDATE 消息中引入 UE performance feedback 列表，支持 one-time 与 periodic 两种上报。
- Partial reporting：确定在 response 消息中引入 failed measurement 以指示部分上报结果；请求消息中是否引入"允许部分上报"指示为 WA，3 个 Option 待下选。
- 范围收敛：R18 停止讨论 predicted TNL capacity indicator、predicted slice available capacity、predicted CAC group；预测精度（accuracy）信息是否传递无共识。

**ME/移动性（12.2.2.2）**
- 确定 HO REQUEST 中携带的 Predicted UE Trajectory 可跨越多个 NG-RAN 节点。
- 确定 R18 中源节点不支持从多个邻区 NG-RAN 节点收集未来的实际 UE 轨迹反馈，也不做"向一跳以外 gNB 请求 UE 轨迹"的增强。
- 源节点如何获知实际 UE 轨迹（经其他 UE 的 UHI vs 用已同意的 Class1/2 过程向目标节点收集）无共识；time stay of UE 的 presence（O/M）仍 FFS。

**ES/节能（12.2.2.3）**
- ES 过程 TP（R3-232149，38.423）agreed，明确 Energy Cost 指实际（actual）EC。
- 确定 EC 为节点级参数，其他粒度超出 Rel-18 范围；编码方式 FFS，WA：若 EC 编码为线性刻度索引（0..Max），由 OAM 配置归一化规则，且同一 EC 上报请求区域内所有邻节点规则一致。
- 确定 "Additional Load" 的描述信息集合：待卸载的 RRC 连接数、Active UE 数、PRB 负载、平均 UL/DL PDCP SDU 数据量，以及卸载动作的目标小区。
- WA：复用已引入的 Class 1（AI/ML INFORMATION REQUEST/RESPONSE）过程向目标节点传递 additional load 描述，用 Class 2（AI/ML INFORMATION UPDATE）过程上报 EC 估计。
- 同意在上述两过程中携带 measured EC；排除"inferred EC 为增量、measured EC 为实际值"的组合，剩余两种 inferred/measured EC 定义待下选；触发针对 additional load 的 inferred EC 请求的时机由实现决定。

**其他接口（12.2.2.4）**
- 本次无实质新共识：F1/E1 影响继续等待非拆分架构工作充分后再讨论。

**Others / MDT 增强（12.3）**
- 确定以现有 MDT 框架为 UE 数据采集基线；采用 s-based、m-based MDT 或两者 FFS。
- 明确 Continuous MDT 定义与定位：使同一 UE 跨 RRC 状态（Connected/Idle/Inactive）连续采集 MDT 数据，且仅对 OAM 侧 AI/ML 训练有益。
- 4 种候选方案（现有机制、logged MDT 配置加连续位置采集指示、m-based "Continuous MDT" flag + HO Request 指示、多 s-based MDT 配置）列出待下选；R18 用例是否需要 Continuous MDT 亦 FFS。

