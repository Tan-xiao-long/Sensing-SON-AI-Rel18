# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-234658 (TP for AI/ML BL CR for TS 38.300) Stage 2 updates on the introduction of RAN AI/ML
- **来源**: Huawei, CATT, China Unicom, Ericsson, Nokia, Nokia Shanghai Bell, ZTE, InterDigital, Qualcomm Incorporated, Lenovo
- **类型**: TP，并入 TS 38.300 的 AI/ML BL CR（基于 R3-233780）；rev of R3-234279
- **会议结论**: agreed
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.2.1 Stage 2 总体描述

#### 内容总结
**背景与要解决的问题**：前几次 RAN3 会议在 Stage 2 和 Stage 3 层面达成了多项关于 RAN AI/ML 功能的协议，其中若干 Stage 3 结论也需要反映到 Stage 2（TS 38.300）中。本 TP 把以下已有共识写入 38.300 BL CR：(1) 支撑 AI/ML 的既有（legacy）信息通过既有流程传递，无需新流程；(2) 新 AI/ML 流程中上报的预测资源状态信息包括预测无线资源、预测激活 UE 数和预测 RRC 连接数；(3) UE 轨迹预测经 Handover Request 传给目标 gNB；(4) 引入 Energy Cost（EC）作为 gNB 间经 Xn 接口共享的 AI/ML 度量。

**与三大用例的关系**：新增的 X.X 节明确 AI/ML for NG-RAN 的目标是通过分析 NG-RAN 收集并自主处理的数据提升网络性能与用户体验，典型用例即网络节能（Network Energy Saving）、负载均衡（Load Balancing）、移动性优化（Mobility Optimization）。本 TP 进一步把各用例的关键信息落到 Stage 2：EC 服务于 NES，小区级 UE 轨迹预测服务于 MO，预测资源状态与 UE 性能反馈可用于所有用例。

**关键技术方案与改动点**：
1. 第 1 处改动：在 3.1 缩略语中加入 AI（Artificial Intelligence）与 ML（Machine Learning）。
2. 第 2 处改动：新增/更新 X.X "AI/ML for NG-RAN" 节：
   - X.X.1 General：AI/ML for NG-RAN 是 RAN 内部功能；
   - X.X.2 Mechanisms and Principles：AI/ML 功能需要邻 NG-RAN 节点（预测信息、反馈信息、测量）和/或 UE（测量结果）的输入，用于支持模型推理（Inference）与模型训练（Training）；信令流程对用例和数据类型不可知（不指示数据用作输入/输出/反馈）；AI/ML 算法与模型、模型性能反馈细节均在 3GPP 范围之外；部署场景为"训练在 OAM、推理在 NG-RAN 节点"或"训练与推理均在 NG-RAN 节点"（本 TP 将原文 gNB 改为 NG-RAN node）。
3. 本 TP 新增的三段核心描述：(a) **预测资源状态信息和 UE 性能反馈**可配置为一次性或周期性上报，可用于所有用例；上报通过 Data Collection Reporting Initiation 流程配置、通过 Data Collection Reporting 流程执行（对应 Xn 上新的 AI/ML 信息请求/上报类流程）；(b) **小区级 UE 轨迹预测**（可用于 MO 用例）经 Handover Request 消息传给目标 NG-RAN 节点，用于后续移动性决策等；(c) 引入 **Energy Cost（EC）度量**（可用于 NES 用例），可应邻节点请求交换。

本 TP 不直接处理 split（CU/DU）架构，该部分由 TS 38.401 的 CR（R3-233789）覆盖。

---

### R3-234663 (TP to 38.423) Requested Prediction Time
- **来源**: ZTE, Samsung, Lenovo, Ericsson, Nokia, Nokia Shanghai Bell, Huawei, CATT, CMCC, Qualcomm Incorporated
- **类型**: TP (Text Proposal)，并入 TS 38.423 (XnAP) 的 AI/ML BL CR；rev of R3-234376
- **会议结论**: agreed
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.2.1 Stage 3 通用流程/消息设计（CB:# AIRAN1_Timeinfo 结论落地）

#### 内容总结
本文稿是 RAN3#121 会议上 CB（Comeback）讨论 "AIRAN1_Timeinfo" 达成一致后的落地 TP，目的是把 "Requested Prediction Time（请求预测时间）" IE 的具体编码和语义写入 TS 38.423 AI/ML BL CR 中的新消息 AI/ML INFORMATION REQUEST（消息名仍标注 FFS）。

**背景与要解决的问题**：Rel-18 AI/ML for NG-RAN 引入了节点间预测信息交互（预测资源状态等），但请求方（NG-RAN node1）需要一种手段告知被请求方（NG-RAN node2）"预测应针对未来哪个时间点"。此前 BL CR 中 Requested Prediction Time 的 IE 类型一直标为 FFS，本 TP 将其确定下来。

**与三大用例的关系**：该 IE 是用例无关（use case agnostic）的通用配置参数，网络节能（NES）、负载均衡（LB）、移动性优化（MO）三个用例请求预测类信息（如预测无线资源状态、预测激活 UE 数、预测 RRC 连接数、Energy Cost 等）时均可使用，用于对齐预测的时间基准。

**关键技术方案**：
1. Requested Prediction Time IE 类型由 FFS 改为 **INTEGER (0..60, ...)，单位为秒**，可选（O）存在，criticality 为 ignore。
2. 语义定义（本 TP 的核心增量）：
   - **一次性上报**时，它指示从收到请求消息（文中沿用旧名 DATA COLLECTION REQUEST，留有修订痕迹）起算的未来时间点，预测针对该时间点提供；
   - **周期性上报**时，指示从收到请求消息起算、并随每个上报周期顺延（shifted by each reporting period）的一系列时间点，每次上报的预测均对应相应顺延后的时间点。
3. IE 位于 AI/ML INFORMATION REQUEST 消息中，与 Registration Request（start/stop）、Report Characteristics 位图（8 个比特分别对应预测无线资源状态、预测激活 UE 数、预测 RRC 连接数、DL/UL 平均 UE 吞吐、平均包时延、平均丢包、Energy Cost）、Cell To Report List、Reporting Periodicity（500ms~10000ms 枚举）等 IE 并列，构成完整的 AI/ML 信息上报发起参数集。

**对协议的具体改动点**：仅修改 38.423 BL CR 的 9.1.3.CC 节（AI/ML INFORMATION REQUEST 消息表格），把 Requested Prediction Time 的 "FFS" 类型替换为 INTEGER (0..60,...) 并补充上述语义描述；消息其余 IE 保持不变。消息名、Measurement ID 名称等仍保留 FFS 标注，留待后续会议解决。本 TP 不涉及 split 架构（CU/DU）改动，相关 F1 影响在 38.401/38.473 相关文稿中处理。

---

### R3-234724 (TP for AI/ML BLCR to TS38.423) Procedure Name
- **来源**: Ericsson, InterDigital, Nokia, Nokia Shanghai Bell, Deutsche Telekom, AT&T, CATT, Orange, Huawei, Lenovo, ZTE
- **类型**: TP，并入 TS 38.423 (XnAP) 的 AI/ML BL CR；rev of R3-234289
- **会议结论**: agreed
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.2.1 Stage 3 通用流程（新过程/消息命名）

#### 内容总结
**背景与要解决的问题**：AI/ML BL CR 中引入的两条新 Xn 过程及其消息的名称一直是 FFS，此前 BL CR 使用 "AI/ML Information Reporting (Initiation)" / "AI/ML INFORMATION REQUEST/RESPONSE/FAILURE/UPDATE"，也有公司主张 "Data Collection ..."。本 TP 把整个 BL CR 相关章节按会议达成的命名统一改为 **Data Collection Reporting Initiation / Data Collection Reporting** 过程与 **DATA COLLECTION REQUEST / RESPONSE / FAILURE / UPDATE** 消息（文本中呈现为 "AI/ML Information→Data Collection" 的修订替换痕迹，名称仍暂挂 FFS 标注），并同步刷新所有引用处。

**与三大用例的关系**：这两条过程是用例与数据类型不可知的通用数据收集框架，NES、LB、MO 三个用例的预测信息（预测无线资源状态、预测激活 UE 数、预测 RRC 连接数）、UE 性能反馈、UE 轨迹以及 Energy Cost（EC，Report Characteristics 第 8 比特及 UPDATE 消息中的节点级 Energy Cost IE）都通过它们请求与上报。

**改动点与流程/消息设计**（覆盖 BL CR 大部分正文，属整体性重命名并保持技术内容）：
1. **8.1 基本过程表**：Class 1 过程改名为 Data Collection Reporting Initiation（消息 DATA COLLECTION REQUEST/RESPONSE/FAILURE），Class 2 过程改名为 Data Collection Reporting（消息 DATA COLLECTION UPDATE）。
2. **8.2.1 Handover Preparation**："与 AI/ML 上报过程的交互"一节改用新名：若 HANDOVER REQUEST 中携带 AI/ML Measurement ID IE（含 node1/node2 Measurement ID，9.2.3.M），目标节点在切换完成后应经 Data Collection Reporting 过程向源节点上报此前经 Initiation 过程配置的信息——即切换后 **UE 性能反馈**机制。
3. **8.4.AA Initiation 过程**：node1 发 REQUEST（Registration Request=start/stop；start 时携带 Report Characteristics 32 位位图，8 个比特对应预测无线资源状态、预测激活 UE 数、预测 RRC 连接数、DL/UL 平均 UE 吞吐、平均包时延、平均丢包、Energy Cost；小区级上报时含 Cell To Report List；可选 Reporting Periodicity 与 Requested Prediction Time）。node2 全部可满足时回 RESPONSE，部分满足时在 RESPONSE 中带 Node/Per Cell Measurement Initiation Result（含失败位图与 Cause），全部失败回 FAILURE；并定义了重复 Measurement ID、位图全 0、stop 时 ID 不存在等异常处理。
4. **8.4.BB Reporting 过程**：node2 用 DATA COLLECTION UPDATE 上报已接受的信息，包含小区级结果（Cell ID + 预测无线资源状态 9.2.2.50 / 预测激活 UE 数 9.2.2.62 / 预测 RRC 连接数 9.2.2.56）、UE 关联结果（UE Assistant Identifier + UE Performance 9.2.3.Y + UE Trajectory，后者 FFS）以及节点级 Energy Cost（FFS）。
5. **9.1.3.CC/DD/EE/FF 消息表及 9.2.3.M AI/ML Measurement ID IE** 全部同步改名。

本 TP 不涉及 split 架构；CU/DU 间的对应 F1 处理在 38.401/38.473 相关文稿中进行。

---


## 6.9 AI/ML for NG-RAN — 网络节能用例（议程 12.2.2.3）

