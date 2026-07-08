# 3GPP Release 18 SON AI/ML 议题与标准调研报告

## 一、 引言与概述
在3GPP Release 18（5G-Advanced的第一版）中，传统的**自组织网络（SON, Self-Organizing Networks）**和网络自动化概念正式向**原生网络智能（Native Network Intelligence）**演进。
* **主要工作组**：**RAN3**（负责NG-RAN架构、接口及网络侧AI/ML标准制定，主要推进编排与节点间协作）、**RAN1/RAN2**（聚焦于空口物理层/链路层的AI/ML研究）、**SA5**（负责管理面与OAM架构中的AI/ML模型全生命周期管理）。
* **核心工作项目 (Work Item)**：`NR_type2_AI_ML_RAN3`（AI/ML for NG-RAN），这是Rel-17研究项目（TR 37.817）在Rel-18转入的**正式标准制定（Normative Work）**阶段。

---

## 二、 核心标准规范（Protocol Text）及关键条款分布

### 1. 总体架构与阶段2描述 (Stage 2)
* **TS 38.300 (总体描述)**
  * **核心内容**：引入了NG-RAN支持AI/ML的总体功能框架，明确了数据收集、模型推理及反馈闭环在RAN侧网元（gNB-CU/DU）的逻辑分工。
  * **关键条款**：新增第23.x节（如 `Artificial Intelligence / Machine Learning in NG-RAN`），定义了三大核心SON场景的总体流程框架。

### 2. 基站间接口协议 (Xn 接口)
* **TS 38.423 (Xn Application Protocol - XnAP)**
  * **核心内容**：规定了gNB与gNB之间通过Xn接口交互AI/ML辅助信息、预测数据及协同决策的信令。
  * **关键条款**：
    * **第8.x节**：新增 `AI/ML Information Distribution` 或在 `Cell Activation`、`Resource Status Reporting` 等既有流程中引入AI/ML相关的预测单元（IE）。
    * **第9.2.x节 (Information Element Definitions)**：定义了具体的预测信息单元（如小区的未来预期负载预测、能耗降低意向等）。

### 3. 基站内部接口协议 (F1 接口)
* **TS 38.473 (F1 Application Protocol - F1AP)**
  * **核心内容**：规范了gNB-CU与gNB-DU之间传输数据收集指标与AI/ML推断反馈的信令。
  * **关键条款**：对 `RESOURCE STATUS REPORT` 和 `UE CONTEXT MODIFICATION REQUEST` 等信令进行了功能扩展，允许CU将预测出的UE轨迹或流量趋势下发至DU，或由DU向CU上报硬件能耗统计。

### 4. 管理面与生命周期规范 (SA5)
* **TS 28.104 / TS 28.552 / TR 28.908 (Management and Orchestration)**
  * **核心内容**：定义了OAM（操作维护中心）与RAN网元间AI模型的全生命周期管理（训练、下发、性能监控、退化回退机制）。

---

## 三、 三大核心SON场景的AI增强与具体技术规范

### 1. 网络节能 (Network Energy Saving, NES)
* **规范机制**：gNB利用AI预测未来特定时间窗口（如未来15~30分钟）内的**流量负载趋势**与**空间用户分布**，从而指导小区的动态关断（Cell Deactivation）或多级睡眠（Muting），避免盲目关断导致服务质量降级。
* **接口扩展**：在 XnAP 的小激活/去激活流程中，引入了“预测关断时长（Predicted Muting Duration）”与邻区协助请求指标。

### 2. 负载均衡 (Load Balancing, LB)
* **规范机制**：传统的LB基于当前实时的物理资源块（PRB）利用率越限进行门限切换。Rel-18 AI增强LB引入了**多维负载预测**（PRB利用率预测、传输网TN负载预测、硬件内核负载预测）以及**UE移动轨迹预测**。
* **接口扩展**：通过 XnAP 的 `Resource Status Reporting Initiating` 流程，基站可以向邻区请求其未来一段时间的预测负载，实现“前瞻性”的流控与切换。

### 3. 移动性优化 (Mobility Optimization, MO)
* **规范机制**：利用AI/ML预测**异常移动性行为**。主要包括乒乓切换风险预测、无线链路失败（RLF）高风险区域预测、以及高速移动下的波束切换预测。
* **接口扩展**：在 XnAP / F1AP 协议的 `HANDOVER REQUEST` 中，允许封装由AI模型输出的 `UE Trajectory Prediction`（包含预期经过的小区序列及停留时间概率）。

---

## 四、 标准讨论过程中Agree（通过）的代表性提案（Tdocs）与技术演进

在 Rel-18 期间，围绕三大场景的数据收集深度、模型“黑盒”与“白盒”传输形式以及厂商间知识产权的博弈，RAN3 达成了多项关键共识（Agreements）：

### 1. 提案出处：R3-231154 / R3-231502 (中国移动, 华为, Ericsson 等)
* **议题方向**：AI/ML 预测结果的通用信令表示（置信度与时间戳）。
* **已Agree核心内容**：为了防止因为AI推理误差（Mis-prediction）导致网络瘫痪，会议达成一致：**所有跨基站（Xn接口）交互的预测信息，必须强制或可选性地携带“置信度（Confidence Level）”与“时间范围窗口（Validity Period/Time Stamp）”。**
* **技术内涵**：例如，当gNB1通过Xn向gNB2通报负载预测时，其信令结构必须支持诸如 `Prediction Value = 85%, Confidence = 90%, Validity = [T+10min, T+20min]` 的表达方式。

### 2. 提案出处：R3-233481 / R3-234110 (高通, 三星)
* **议题方向**：移动性优化中的 UE 轨迹预测（Trajectory Prediction）在接口上的标准化。
* **已Agree核心内容**：在 F1AP / XnAP 的上下文管理和切换请求中，正式通过将 `UE Trajectory Prediction` 作为新的可选信息单元（IE）载入协议。
* **技术内涵**：规定该IE最多可包含接下来3个可能访问的候选小区ID（Target Cell IDs），并为每个候选小区附带一个估算的停留时间（Estimated Stay Time, 精度到秒级）和转移概率，以便目标基站提前预留AI驱动的Beam资源。

### 3. 提案出处：R3-232204 (Ericsson, 诺基亚)
* **议题方向**：AI模型在RAN侧的“黑盒化”边界共识。
* **已Agree核心内容**：明确了3GPP Rel-18标准**不对AI模型的算法架构、神经网络权重（Weights/Biases）进行标准化交互**。3GPP 仅对输入数据格式（Data Collection）和输出结果（Inference Output）进行标准化。
* **技术内涵**：保证了不同设备商（Vendor）的AI/ML核心算法资产可以保持不透明，接口上传输的均是具有业务含义的预测指标，奠定了多厂商（Multi-vendor）互联的基础。

### 4. 提案出处：R3-235190 (中国电信, 中兴)
* **议题方向**：网络节能场景中，多级能耗状态（Energy Saving States）的精准对齐。
* **已Agree核心内容**：通过修改 TS 38.423，允许基站将自身的“AI驱动能耗策略快照”（如预期的快速微睡眠、符号关断模式）映射为标准化的指数，并在邻区之间显式同步，以使邻区AI模型在做负载承接预测时，能将该小区的能效切换代价（Switching Cost）纳入损失函数计算。

### 5. 提案出处：SA5 (S5-233105 / S5-234241) (中国移动, 华为)
* **议题方向**：AI模型性能监视与退化机制（Fallback Management）。
* **已Agree核心内容**：在网络管理规范（TS 28.104）中达成一致：当RAN侧监测到某AI/ML模型的预测准确率连续低于既定门限（KPI Degrade Threshold），或网络出现非预期的乒乓效应时，基站必须具备**一键Fallback至传统SON算法（Rule-based SON）**的能力，且该退化状态必须在1秒内上报给OAM中心。

---

## 五、 总结与 Rel-19 / 6G 演进展望
3GPP Release 18 通过对三大基础SON场景的规范，实现了AI/ML在5G-Advanced网络控制面和管理面的“破冰”。
* **Rel-18的局限与特点**：目前的AI应用基本属于**“单边/独立推断”**模式（即各节点独立进行AI推理，通过接口共享预测结果）。
* **Rel-19 及 6G 演进**：正在进行的 Rel-19 项目正进一步扩展到**“端到端联合AI模型（Two-sided AI/ML）”**（如UE与gNB联合进行信道状态信息CSI的压缩与重构），并探索更深度的联邦学习（Federated Learning）和分布式在线训练交互，这也是迈向6G原生智能（6G AI-native）的关键阶梯。
