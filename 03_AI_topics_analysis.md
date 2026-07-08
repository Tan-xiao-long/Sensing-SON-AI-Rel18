# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 4. AI 议题详细分析（AI 12）

### 4.0 工作项背景

Rel-18 AI/ML for NG-RAN WI（WID RP-231159）承接 Rel-17 研究项目 TR 37.817，目标是在**既有 NG-RAN 接口与架构内**（含 split 与非 split 架构）为三大用例提供数据收集增强与信令支持：

- **AI/ML 网络节能**（Network Energy Saving，NES）；
- **AI/ML 负载均衡**（Load Balancing，LB）；
- **AI/ML 移动性优化**（Mobility Optimization，MO/ME）。

模型训练/推理的位置遵循 TR 37.817（训练在 OAM 或 gNB、推理在 gNB），Rel-18 不涉及模型本身的标准化——工作重心是节点间交换 AI/ML 所需的输入/输出/反馈数据（预测资源状态、UE 性能反馈、UE 轨迹、能耗指标等）的新 Xn 过程与 IE。

### 4.1 子议程 12.1：基线 CR（3 篇 endorsed）

- **R3-233756**（XnAP 38.423 BL CR）：AI/ML 信息上报框架的主体——新增 Class 1 过程（AI/ML INFORMATION REQUEST/RESPONSE/FAILURE）与 Class 2 过程（AI/ML INFORMATION UPDATE），切换请求中新增小区级 UE 轨迹预测 IE 与 AI/ML Measurement ID（用于切换后 UE 性能反馈闭环）；
- **R3-233780**（38.300 draft CR）：Stage 2 总体描述——AI/ML 功能框架引用、缩略语、用例无关的数据收集原则；
- **R3-233789**（38.401 CR）：split 架构下 AI/ML-RAN 特性的架构性描述。

详见 §6 逐篇总结。

### 4.2 子议程 12.2.1：Stage 2 与通用流程（3 篇 agreed，核心进展）

**会议达成的主要共识**：

- **过程/消息正式命名**（本次会议标志性结论，落地为 agreed 的 R3-234724）：将此前暂名的 AI/ML 信息过程族改名为
  - Class 1：**DATA COLLECTION REPORTING INITIATION**（消息：DATA COLLECTION REQUEST / DATA COLLECTION RESPONSE / DATA COLLECTION FAILURE）；
  - Class 2：**DATA COLLECTION REPORTING**（消息：DATA COLLECTION UPDATE）；
- **Requested Prediction Time 编码**：采用 INTEGER、最大值 60 秒、可扩展结构（落地为 agreed 的 R3-234663）；一次性上报与周期性上报均可配置；周期上报时预测时间点随上报周期顺延；Rel-18 不引入"时间区间（time interval）"；
- **预测精度**：Rel-18 不在 Xn 上传递预测精度信息；
- 过程设计原则延续并强化：用例无关（use case agnostic）、数据类型无关（data type agnostic，不指示数据用作输入/输出/反馈）、非 UE 关联为起点、基于请求的上报（类似资源状态上报过程）、Rel-18 不做 NG 接口方案、能力交互经由信息请求/响应/失败过程隐式达成；
- Stage 2 文本更新（落地为 agreed 的 R3-234658）。

### 4.3 子议程 12.2.2.1：负载均衡（LB）用例（无 agreed TP，共识丰富）

**会议达成的主要共识**：

- Rel-18 不追加 Data Collection Request 中的"部分上报指示"；
- 同意引入指示"定时类失败"的原因值（具体定时问题待续）；不引入"请求信息组合失败"原因值；
- 在 DATA COLLECTION REQUEST 中新增 **Reporting Duration** IE：UE 性能反馈的上报时长自切换执行成功起算，反馈上报不得晚于该时长到期；支持周期性与一次性两种 UE 性能反馈；复用既有 Reporting Periodicity 还是新建专用周期 IE 待续；
- UE 在 Reporting Duration 内转入 Idle/Inactive 或再次切换时终止反馈收集（是否显式指示待续）。

相应 TP（R3-234689，UE Performance Feedback Configuration）因部分公司对 Stage 3 细节保留意见仅被 **noted**。

### 4.4 子议程 12.2.2.2：移动性优化（MO）用例（无 agreed TP，共识丰富）

**会议达成的主要共识**：

- 实测 UE 轨迹（Measured UE Trajectory）上报为**一次性上报**；触发条件至少包括：A）UE 状态切换（转入 IDLE/INACTIVE）、B）UE 离开目标节点、C）上报时长到期、D）同一目标节点内切换次数达到配置值；
- Report time duration 与"节点内小区间切换配置次数"携带于 DATA COLLECTION REQUEST 消息；
- Measured UE Trajectory 中小区 ID 列表为必选，驻留时长的存在性 FFS；复用 UHI IE 还是新 IE 待续；
- 延续既有框架：小区粒度 UE 轨迹预测经 HANDOVER REQUEST 传递（结构同 UHI，逐小区带预计驻留时长，可跨多个 NG-RAN 节点，但预测仅限下一跳目标节点）；UE 性能反馈支持平均包时延、DL/UL 平均吞吐、平均误包率。

### 4.5 子议程 12.2.2.3：网络节能（NES）用例（1 篇 agreed）

**会议达成的主要共识**：

- **Energy Cost（EC）为节点级参数**，Rel-18 不做更细粒度；
- 工作假设：EC 编码为线性刻度索引（0..Max）时，由 OAM 配置归一化规则，且在触发 EC 上报请求的区域内所有相邻 NG-RAN 节点规则一致；
- 同意把**实测 EC** 纳入 AI/ML 信息上报发起过程与上报过程（即 DATA COLLECTION 过程族）——落地为 agreed 的 R3-234752（XnAP TP：Report Characteristics 位图第 8 比特定义为 Energy Cost，UPDATE 消息携带节点级 EC 值）；
- 工作假设：用 Class 1 过程向目标节点描述"附加负载"、用 Class 2 过程回报推断 EC（inferred EC 是否进 Rel-18 仍 FFS）。

### 4.6 子议程 12.2.2.4 与 12.3：split 架构接口与面向 AI 的 MDT（无 agreed 产出）

- **E1/F1 影响**（12.2.2.4）：对于 AI/ML 特性在 split 架构下 E1AP/F1AP 是否需要改动，SS/ZTE/CATT 持肯定态度、Nokia/Ericsson/Huawei 反对，未形成结论；
- **面向 AI 的 MDT 连续采集**（12.3）：形成的共同理解是——信令型 MDT 可对特定 UE 连续采集但大规模选 UE 存在扩展性问题且缺少小区级粒度；管理型 MDT 可扩展性好但无法跨 RRC 状态关联同一 UE 的报告、UE 选择不受 OAM 控制。Ericsson 与 ZTE 各自的 LS 草稿（连续 MDT、UE 选择粒度、连续 AI-ML 信息上报）均未发出；Nokia 提交的 38.413 CR（连续 MDT 测量收集）未获通过。

---
