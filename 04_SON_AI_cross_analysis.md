# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 5. SON 与 AI 的交叉分析

**（1）AI/ML WI 的三大用例与传统 SON 功能一一对应。** 网络节能（NES）对应传统 SON 的节能（Energy Saving）功能、负载均衡（LB）对应 MLB、移动性优化（MO）对应 MRO——Rel-18 AI/ML for NG-RAN 实质上是把 Rel-15/16/17 SON 数据收集框架升级为"支持预测信息交换"的智能化框架。这一点在协议设计上体现得非常直接：XnAP AI/ML BL CR（R3-233756）中预测资源状态、预测激活 UE 数、预测 RRC 连接数等 IE 直接**复用 Rel-17 SON/MDT 引入的既有 IE 类型**（如 9.2.2.50、9.2.2.62、9.2.2.56）。

**（2）数据收集是两个 WI 的共同主线。** SON/MDT WI 的正式名称即"数据收集增强"（Enhancement of Data Collection for SON/MDT）；AI/ML WI 的 WID 目标同样是"数据收集增强与信令支持"。本次会议 AI/ML 过程族正式改名为 **DATA COLLECTION**（REQUEST/RESPONSE/FAILURE/UPDATE），命名本身就表明 RAN3 把 AI/ML 信息交互定位为通用数据收集机制——过程"用例无关、数据类型无关"，未来可承载 AI 之外的数据收集需求。

**（3）MDT 正被探索作为 AI 数据管道。** 12.3 议程下多家公司（Ericsson/AT&T/InterDigital/DT、ZTE/Lenovo/Samsung、Nokia、Qualcomm）推动"面向 AI-ML 连续信息上报的 MDT 增强"（连续 MDT、改进 UE 选择粒度），试图让 MDT 成为 AI 训练数据的采集通道；本次会议虽未形成 agreed 结论，但形成的"信令型/管理型 MDT 能力差距"共同理解为后续版本（Rel-19 AI/ML 演进）铺垫了方向。

**（4）UE 轨迹与 UHI 的贯通。** SON 侧 agreed 的 R3-234666 为 CPAC 引入 UHI（UE 历史信息）记录；AI/ML 侧的小区级 UE 轨迹预测明确"结构与 UHI IE 相同"、实测 UE 轨迹是否复用 UHI IE 仍在讨论——SON 积累的 UHI 机制正成为 AI 移动性优化的输入/反馈数据基础。

**（5）节能维度的分工。** AI/ML WI 的 NES 用例聚焦小区级节能策略与节点级 EC 指标交换，并明确"避免与网络节能 SI/WI（AI 24）重复"；EC 定义上采纳"以 SA5 定义的 EE 为基线"的工作假设，体现 RAN3-SA5 在能耗指标上的协同。

**（6）SON 与 AI 议题的推进节奏差异。** SON/MDT WI 本次会议 agreed 文稿多达 16 篇、特性基本收敛（SHR/SPR 转发机制、RACH 双接口新过程、NPN 区域范围等均已落栓）；AI/ML WI 的 agreed 文稿仅 4 篇，大量结论以口头共识形式存在、Stage 3 细节（消息名 FFS 清理、UE 性能反馈配置、轨迹上报格式、E1/F1 影响）留待 RAN3#121bis 及后续会议——这与两个 WI 分别定于 RAN#102、RAN#100 完成的时间表相符。

---
