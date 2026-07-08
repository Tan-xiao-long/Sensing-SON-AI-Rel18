# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-234752 (TP for AI/ML BLCR to TS38.423) AI/ML Network Energy Saving
- **来源**: Ericsson, Huawei, Nokia, Nokia Shanghai Bell, ZTE, Samsung
- **类型**: TP，并入 TS 38.423 (XnAP) 的 AI/ML BL CR；rev of R3-234297
- **会议结论**: agreed unseen
- **所属议题**: Rel-18 AI/ML for NG-RAN WI (WID RP-231159)，议程 12.2.2.3 网络节能（Network Energy Saving, NES）用例

#### 内容总结
**背景与要解决的问题**：RAN3 已同意引入 Energy Cost（EC）作为 gNB 间经 Xn 接口共享的 AI/ML 节能度量，并在 AI/ML INFORMATION REQUEST 的 Report Characteristics 位图中预留了第 8 比特 "Energy Cost"，但 BL CR 中还缺两块内容：(1) 过程文本中没有规定第 8 比特置 1 时 node2 应在 UPDATE 消息中回送 Energy Cost IE；(2) UPDATE 消息中 Energy Cost IE 的类型与语义一直是 FFS。本 TP 补齐这两点，是 NES 用例的核心 Stage 3 落地文稿之一（本次会议因时间原因按 "agreed unseen" 方式通过）。

**与三大用例的关系**：直接服务于**网络节能（NES）**用例——邻区 gNB 交换 EC 后，AI/ML 节能模型可据此评估本节点动作（如小区关断、负载迁移）对邻节点/整体能耗的影响；所依托的 AI/ML Information Reporting Initiation/Reporting（后改名 Data Collection）过程本身对 LB、MO 同样通用。

**关键技术方案与具体改动点**：
1. **8.4.AA.2 Successful Operation**：在"与其他过程的交互"列表末尾新增一条——若 REQUEST 中 Report Characteristics 的第 8 比特 "Energy Cost" 置 "1"，NG-RAN node2 应在 AI/ML INFORMATION UPDATE 消息中包含 **Energy Cost IE**（文中该句沿用了 "DATA COLLECTION REQUEST" 字样，属并行改名文稿留下的痕迹）。其余过程文本（start/stop 注册、Cell To Report List、部分接纳时的 Node/Per Cell Measurement Initiation Result、Reporting Periodicity、Requested Prediction Time、异常条件等）保持不变。
2. **9.1.3.CC AI/ML INFORMATION REQUEST**：消息表整体重申，Report Characteristics 位图第 8 比特为 Energy Cost（节点级请求，不在小区级列表内）。
3. **9.1.3.FF AI/ML INFORMATION UPDATE**：把节点级 Energy Cost IE 的类型由 FFS 确定为 **INTEGER (0..10000, ...)**，语义为"节点级实测能耗指数（Energy Consumption index）"：0 表示测得的最小能耗，10000 表示最大能耗，**能耗应按线性刻度度量**——即 EC 是经归一化的相对指数而非绝对瓦时值，具体测量方法留给实现/SA5 指标。Energy Cost 为可选 IE，与小区级预测结果（预测无线资源状态/激活 UE 数/RRC 连接数）和 UE 关联结果（UE Performance、UE Trajectory）并列。

**split 架构处理**：本 TP 仅涉及 Xn（gNB 间/CU 间）接口；CU-DU 分离场景下 DU 侧能耗信息获取由 F1（38.473）相关讨论处理，不在本 TP 范围。

---
