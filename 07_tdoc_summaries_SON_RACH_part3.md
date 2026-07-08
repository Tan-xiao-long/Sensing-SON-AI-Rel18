# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-234743 (TPs for SON BLCRs for TS 38.423): RACH enhancements
- **来源**: ZTE, Ericsson, Huawei, Nokia, Nokia Shanghai Bell
- **类型**: TP (text proposal)，并入 SON BL CR；影响 TS 38.423 (XnAP)
- **会议结论**: agreed unseen (未经会上逐条审阅直接批准)
- **所属议题**: 议程 10.2.3，Rel-18 SON/MDT WI 下的 RACH 优化 (RACH enhancements)

#### 内容总结
**背景与要解决的问题**：MR-DC 下，UE 在 SN (PSCell) 侧因波束失败恢复、上行失步、调度请求失败等原因执行的成功随机接入只有 SN 知晓；而 RA Report 需由 MN 经 RRC 从 UE 取回，MN 若不知情就无法及时取回报告，SN 也就得不到优化其 RACH 配置所需的 UE 侧数据。Rel-18 为此在 XnAP 中引入新的 Class 2 消息 **RACH INDICATION**，由 SN 告知 MN "UE 中有可用的 RA Report"。本 TP 给出该消息的表格定义和相应 ASN.1。

**协议改动点 (TS 38.423)**：
1. **新增 9.1.2.x RACH INDICATION 消息**：由 S-NG-RAN node 发往 M-NG-RAN node，用于告知 M-NG-RAN 节点"一个或多个 RA report 在 UE 处可用"。方向：S-NG-RAN node → M-NG-RAN node。消息结构：
   - Message Type (M, 9.3.1.1, YES/ignore)；
   - **RA Report Indication List** (1, YES/reject)：其下为 RA Report Indication List Item，重复度 **1..maxnoofRAReportIndications**，即一条消息可批量指示多个 UE 的 RA Report 可用性；
   - 每个列表项含 **M-NG-RAN node UE XnAP ID** (M, NG-RAN node UE XnAP ID, 9.2.3.16，"Allocated at the M-NG-RAN node")，用于标识对应的 UE。文本中可见修订痕迹：早期版本曾命名为 "M-NG-RAN UE Assistant Identifier"，修订后统一改用既有的 M-NG-RAN node UE XnAP ID；条目级 criticality 也由 EACH/ignore、YES/reject 调整(相应字段划改为 "-")。
2. **ASN.1 改动**：新增 RaReportIndicationList ::= SEQUENCE (SIZE(1..maxnoofRaReportIndications)) OF RaReportIndication-Item；RaReportIndication-Item ::= SEQUENCE { m-NG-RAN-node-UE-XnAP-ID (NG-RANnodeUEXnAPID), iE-Extensions OPTIONAL, ... }(同样带有删除 m-NG-RANAssistantIdentifier 命名的修订痕迹)。RachIndication 消息级 PDU 定义与 maxnoofRAReportIndications 常量取值在本 TP 摘录中未展开。

**与 SON 的关系**：RACH INDICATION 是 Rel-18 RACH 自优化闭环的关键 Stage-3 信令：SN 侧随机接入完成 → SN 经 Xn 发 RACH INDICATION(可聚合多个 UE) → MN 依据其中的 M-NG-RAN node UE XnAP ID 定位 UE 并经 UEInformationRequest 取回 RA Report → 报告回传给 SN 用于 PRACH 前导/SSB 资源与门限的自优化。与 TS 38.420 过程清单更新(R3-234742)及 38.300/37.340 的 Stage-2 描述(R3-234650/R3-234695)配套。

---
