# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 6.7 AI/ML for NG-RAN — 基线 CR（议程 12.1，endorsed）

### R3-233756 (BLCR to 38.423) for AI/ML for NG-RAN
- **来源**: Ericsson, Nokia, Nokia Shanghai Bell
- **类型**: BL CR（Baseline CR）CR0959 rev 7，TS 38.423 (XnAP) v17.5.0，Category B，WI 代码 NR_AIML_NGRAN-Core
- **会议结论**: endorsed as BL CR
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.1（BL CR 维护）

#### 内容总结
**背景**：这是 Rel-18 AI/ML for NG-RAN 在 XnAP（TS 38.423）上的基线 CR 第 7 版（rev7 为 rebase 重提交，已累积吸收 R3-230978/230855、R3-232148/232149、R3-233512/233513/233112/232568 等历次 agreed TP），作为本次会议各 TP（如 R3-234663、R3-234724、R3-234752）的合并底稿，会议 endorse 后继续演进。覆盖 NES、LB、MO 三大用例所需的 Xn 信令。

**主要内容与协议改动**：
1. **缩略语**：3.2 节新增 AI、ML。
2. **新增两条 Xn 过程**（8.1 过程表 + 8.4.AA/8.4.BB，名称均挂 FFS）：
   - Class 1 过程 **AI/ML Information Reporting Initiation**（AI/ML INFORMATION REQUEST/RESPONSE/FAILURE）：node1 用 REQUEST 发起/停止上报（Registration Request = start/stop），start 时携带 32 位 Report Characteristics 位图（比特 1-8：预测无线资源状态、预测激活 UE 数、预测 RRC 连接数、DL/UL 平均 UE 吞吐、平均包时延、平均丢包、Energy Cost）、小区级请求的 Cell To Report List（上限 16384 小区）、可选 Reporting Periodicity（500/1000/2000/5000/10000ms，兼作平均窗长）和 Requested Prediction Time（类型 FFS）。node2 全部可满足回 RESPONSE；部分满足时在 RESPONSE 中带 Node Measurement Initiation Result（节点级失败位图，首比特 Energy Cost）和/或 Per Cell Measurement Initiation Result（小区级失败位图+Cause）；全不满足回 FAILURE。定义了无响应重发、stop 时 ID 不存在、位图全 0、重复 start 等异常处理。过程采用非 UE 关联信令。
   - Class 2 过程 **AI/ML Information Reporting**（AI/ML INFORMATION UPDATE）：node2 上报已接受的信息，含小区级 Cell AI/ML Info Result（Cell ID + 预测无线资源状态 9.2.2.50、预测激活 UE 数 9.2.2.62、预测 RRC 连接数 9.2.2.56——复用 Rel-17 SON/MDT 既有 IE 类型）、UE 关联的 UE Associated Info Result（UE Assistant Identifier=node1 分配的 XnAP ID + UE Performance 9.2.3.Y + UE Trajectory(FFS)）以及节点级 Energy Cost（FFS）。
3. **切换准备过程增强**（8.2.1、9.1.1.1 HANDOVER REQUEST）：
   - 新增 **Cell Based UE Trajectory Prediction IE**（9.2.3.x）：源节点在 HANDOVER REQUEST 中携带按时间顺序排列的预测小区列表（每项为 Predicted Trajectory Cell Information 9.2.3.Z：Global NG-RAN Cell Identity + 可选 Predicted Time UE Stays in Cell，INTEGER 0..4095 秒），目标节点可用于后续移动性决策——服务 MO 用例；
   - 新增 **AI/ML Measurement ID IE**（9.2.3.M，含 node1/node2 两个 Measurement ID）：目标节点在切换完成后按其标识的既有上报上下文，经 AI/ML Information Reporting 过程向源节点回送 **UE 性能反馈**——用于 LB/MO 的模型反馈闭环。
4. **新 IE**：9.2.3.Y UE Performance（DL/UL 平均 UE 吞吐 9.2.3.4、平均包时延与平均丢包类型 FFS）。
5. **ASN.1**（9.3.4/9.3.5/9.3.7）：HandoverRequest-IEs 加入 id-CellBasedUETrajectoryPrediction（criticality ignore，Protocol IE ID 待定），新增 CellBasedUETrajectoryPrediction、PredictedTrajectoryNGRANCellInfo 等定义及常量 maxnoofCellsTrajectoryPredict（值 FFS）；新过程的 ASN.1 尚未加入。

大量名称/编码仍挂 FFS（过程与消息名、Measurement ID 名、Requested Prediction Time 类型、Energy Cost 类型、UE Trajectory 上报格式等），正是本次会议多个 TP 逐项解决的对象。本 CR 仅涉及 Xn 接口，split 架构由 38.401/38.473 的 BL CR 处理。

---

### R3-233780 Draft CR to 38.300 on AI/ML for NG-RAN
- **来源**: CMCC, ZTE, Ericsson, Nokia, Nokia Shanghai Bell, Huawei, CATT, Samsung, Lenovo, Intel Corporation
- **类型**: Draft (BL) CR，TS 38.300 v17.5.0，Category B，WI 代码 NR_AIML_NGRAN-Core
- **会议结论**: endorsed as BL CR
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.1（BL CR 维护）

#### 内容总结
**背景与要解决的问题**：本文稿是 AI/ML for NG-RAN 特性在 Stage 2 总体规范 TS 38.300 中的基线 CR，累积了 RAN3#117（增加 AI/ML 缩略语、新建 AI/ML 章节）、#117bis（将章节拆分为 General 与 Mechanisms and Principles 两小节并完善描述）、#120（补充"新流程对用例和数据类型不可知"）等历次会议 agreed TP（rev0-rev3 分别对应 R3-225211、R3-226056、重提交、R3-233342）。若不批准，AI/ML for NG-RAN 特性将无 Stage 2 依据。本次 RAN3#121 会议将其 endorse 为 BL CR，作为同会 agreed 的 Stage 2 TP（R3-234658）的合并底稿。

**与三大用例的关系**：新增章节明确 AI/ML for NG-RAN 的目标是通过分析 NG-RAN 收集并自主处理的数据获得进一步洞察，从而提升网络性能与用户体验，示例用例即**网络节能（Network Energy Saving）、负载均衡（Load Balancing）、移动性优化（Mobility Optimization）**——这也是 Rel-18 WI 的三大规范化用例的 Stage 2 锚点。

**关键内容与具体改动点**：
1. **第 1 处改动（3.1 缩略语）**：新增 AI（Artificial Intelligence）与 ML（Machine Learning）。
2. **第 2 处改动（新增 X.X 节 "AI/ML for NG-RAN"，章节号待定）**：
   - **X.X.1 General**：AI/ML for NG-RAN 作为 **RAN 内部功能**，通过 AI/ML 技术实现；目标与三大用例如上。
   - **X.X.2 Mechanisms and Principles**：(a) AI/ML 功能需要来自邻 NG-RAN 节点（如预测信息、反馈信息、测量）和/或 UE（如测量结果）的输入，用以支持 **AI/ML 模型推理（Model Inference）与模型训练（Model Training）**等处理过程；(b) 用于交换 AI/ML 相关信息的信令流程是**用例与数据类型不可知**的，即不指示所交换数据的预期用途（输入/输出/反馈）；(c) **AI/ML 算法与模型不在 3GPP 标准化范围内**，模型性能反馈的细节亦然；(d) 支持两种功能部署场景——**模型训练位于 OAM、模型推理位于 gNB**，以及**模型训练与推理均位于 gNB**（不支持标准化的 gNB 间模型传递）。

该版本尚未包含预测资源状态内容、UE 轨迹经 Handover Request 传递、Energy Cost（EC）度量、Data Collection 两阶段上报流程等描述——这些正是同会 R3-234658 TP 在其上补充的内容。split（CU/DU）架构下的功能划分由 TS 38.401 的对应 BL CR（R3-233789）处理，本 CR 不涉及。

---

### R3-233789 CR to TS 38.401 for addition of AI/ML-RAN feature in the case of split architecture
- **来源**: ZTE, Ericsson, Nokia, Nokia Shanghai Bell, Lenovo, Huawei, Samsung, Intel Corporation, CMCC
- **类型**: BL CR，CR0265 rev 7，TS 38.401 v17.5.0，Category B，WI 代码 NR_AIML_NGRAN-Core
- **会议结论**: endorsed as BL CR
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.1（BL CR 维护）

#### 内容总结
**背景与要解决的问题**：TS 38.300 的 AI/ML 章节只定义了非分离（aggregated）gNB 下的部署场景（训练在 OAM/推理在 gNB，或训练与推理均在 gNB），而 **gNB CU-DU 分离（split）架构**下 AI/ML 功能的分布在规范中缺失。本 CR 在 NG-RAN 总体架构规范 TS 38.401 中补充该内容。rev1 起加入 split 架构部署描述并增加联署公司，rev2-rev7 主要为封面更新与重提交；本次会议继续 endorse 为 BL CR。CR 声明对同版本规范具有隔离性影响（isolated impact）。

**与三大用例的关系**：本 CR 不针对具体用例，而是为网络节能（NES）、负载均衡（LB）、移动性优化（MO）三大用例在 split 架构下的实现提供统一的架构前提：三个用例的模型推理（如产生预测资源状态、Energy Cost、UE 轨迹预测等输出）在 split 场景下均由 **gNB-CU** 承载，gNB-DU 侧所需的输入/辅助信息交互则通过 F1 接口（TS 38.473 的配套 BL CR）解决。

**关键技术方案与具体改动点**：
1. **3.2 缩略语**：新增 AI（Artificial Intelligence）与 ML（Machine Learning）。
2. **第 7 章（NG-RAN 功能描述）新增 7.x 节 "Support of AI/ML in NG-RAN"**（位于 7.10 RAN visible QoE 之后）：
   - 首先指明 AI/ML for NG-RAN 功能本身在 TS 38.300 中规定（Stage 2 主体不重复）；
   - 核心新增内容为：**在 CU-DU 分离架构下，可支持以下场景：(a) AI/ML 模型训练位于 OAM，模型推理位于 gNB-CU；(b) AI/ML 模型训练与模型推理均位于 gNB-CU**。
   即 Rel-18 中 split 架构下模型训练/推理的宿主统一为 gNB-CU（而非 gNB-DU），与 38.300 中非分离 gNB 的两种部署场景一一对应；DU 不承载标准化的模型推理功能，仅按需经 F1 提供数据。

**协议影响**：改动极小且自包含（缩略语 + 一个新功能小节），不涉及新消息或 IE；具体的 F1 信令增强（如 CU 向 DU 请求能耗/资源信息等）不在本 CR 内，由 38.473 的 AI/ML BL CR 及后续 TP 处理。其意义在于把 AI/ML-RAN 特性的 split 架构功能定位写入架构规范，避免 Rel-18 特性在分离部署场景下无规范依据。

---


## 6.8 AI/ML for NG-RAN — Stage 2 与通用流程（议程 12.2.1）

