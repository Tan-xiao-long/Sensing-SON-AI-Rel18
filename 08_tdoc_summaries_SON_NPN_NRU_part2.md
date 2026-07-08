# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-234744 LS on MDT for NPN
- **来源**: RAN3（起草：Ericsson，联系人 Angelo Centonza；系 R3-234717/R3-234723 的修订版）
- **类型**: LS（联络函），Rel-18，工作项目 NR_ENDC_SON_MDT_enh2-Core；附件为两份 endorse 的 BL CR（R3-233748 对 TS 38.413 的 BL CR、R3-234720 对 TS 37.320 的 BL CR）
- **会议结论**: agreed unseen
- **所属议题**: 议程 10.2.4 —— Rel-18 SON/MDT 增强 WI：非公共网络（NPN）的 SON/MDT 支持

#### 内容总结
**发给谁**：主送 RAN2 和 SA5（无抄送）。注意文件名中写作 "LS to RAN2-SA2"，但函件正文明确 To: RAN2, SA5。

**背景**：RAN3 在 Rel-18 SON/MDT 增强 WI 下开展了 NPN 场景 MDT 支持的工作，并已在 RAN3#121 会议取得阶段性成果。这些成果体现在两份已 endorse 的 Baseline CR 中：TS 38.413 (NGAP) BL CR 的 9.3.1.169 节（MDT Configuration-NR IE，见附件 R3-233748）和 TS 37.320 BL CR 的 5.1.1.1.1 节（Logged MDT 配置参数，见附件 R3-234720）。本 LS 的目的是把 RAN3 的进展正式通知负责 UE 空口行为的 RAN2 和负责网管/Trace 管理（TS 32.422 等 OAM 规范）的 SA5，以便相关规范同步修改。

**内容要点**：LS 说明 RAN3 的工作主要集中在**更新 MDT 区域范围（Area Scope）信息以适配 NPN 网络**——即在 MDT 区域范围中引入面向 PNI-NPN 的 CAG 列表以及面向 SNPN 的小区/TAI/SNPN 级范围。LS 特别指出：为支持"等效 SNPN (equivalent SNPNs)"，已在 MDT Area Scope 中增加**最多 16 个 SNPN 的列表**；至于本 Release 中是否对该 SNPN 列表的使用施加限制，取决于其他工作组在 eSNPN（增强 SNPN）支持方面的进展。

**请求动作（ACTION）**：RAN3 请 RAN2 和 SA5：(1) 将上述进展纳入考虑；(2) 如有需要，对各自负责的规范（如 RAN2 的 TS 38.331 RRC、SA5 的 TS 32.422 Trace/MDT 管理规范）做相应修改；(3) 如有进展，就 NPN MDT 向 RAN3 提供反馈。LS 末尾附 RAN3 后续会议日程（RAN3#121-bis，2023 年 10 月 9–13 日厦门；RAN3#122，2023 年 11 月 13–17 日芝加哥），提示对方回复的时间窗口。

**与 SON/MDT 功能的关系**：NPN 场景的 MDT 是跨工作组特性——RAN3 负责 NGAP/XnAP/F1AP 等网络接口信令及 37.320 阶段 2 描述，RAN2 负责 UE 侧 RRC（logged MDT 配置、日志区域判断），SA5 负责基于管理的 MDT 激活与 Trace 参数。本 LS 是保证三方规范（信令面 CAG list、SNPN area scope、用户同意规则等）一致演进的协调机制，也是本议程下 R3-234718/R3-234719/R3-234720 等文稿的配套输出。

---


## 6.6 SON/MDT — SON for NR-U（议程 10.2.5）

### R3-234544 (TP for SON BL CR for TS 38.423) NR-U enhancements for MLB
- **来源**: Ericsson, ZTE, Nokia, Nokia Shanghai Bell, Qualcomm Incorporated, Huawei
- **类型**: TP（文本提案），面向 TS 38.423 (XnAP) 的 Rel-18 SON Baseline CR
- **会议结论**: agreed
- **所属议题**: 议程 10.2.5 —— Rel-18 SON/MDT 增强 WI：SON for NR-U（免许可频谱 NR），移动性负载均衡（MLB）增强

#### 内容总结
**背景与要解决的问题**：在 NR-U（免许可频谱）部署中，小区负载不仅取决于自身业务量，还受共享频谱上其他系统/节点竞争信道（LBT，先听后说）的影响。传统 MLB 使用的负载指标（PRB 使用率、复合可用容量等）无法反映免许可信道的实际可用性，因此 Rel-18 SON 增强为 MLB 引入了按 NR-U 信道粒度的负载/信道占用信息交换。本次会议将此前的工作假设（WA）"在 XnAP 和 F1AP 的 RESOURCE STATUS UPDATE 消息中按 NR-U 信道引入可选的 Radio Resource Status 负载度量"转为正式协议，本 TP 将其落实到 XnAP BL CR。

**关键技术方案**：在 XnAP 资源状态报告过程（Mobility Load Management）中，NG-RAN node2 向 node1 发送的 9.1.3.21 RESOURCE STATUS UPDATE 消息的 Cell Measurement Result Item 内包含 **NR-U Channel List**（0..1，YES/ignore），列表含 1..maxnoofNR-UChannelIDs 个 NR-U Channel Item，每项包括：
- **NR-U Channel ID**（M，INTEGER(1..maxnoofNR-UChannelIDs,...)）：标识上一上报周期内使用的 NR-U 信道；
- **Channel Occupancy Time Percentage DL**（M，INTEGER(0..100)）：该 NR-U 信道用于服务小区 DL 业务的信道占用时间百分比，100 表示占满整个上报间隔；
- **Energy Detection Threshold DL**（M，INTEGER(-100..-50,...) dBm）：gNB DL 信道侦听所用的平均 ED 门限；
- **Channel Occupancy Time Percentage UL**（O）与 **Energy Detection Threshold UL**（O）：UL 侧对应量，后者为 gNB 配置给 UE 的最大 ED 门限的平均值；
- **本 TP 新增的 Radio Resource Status NR-U**（O，9.2.2.xx，YES/ignore）：按 NR-U 信道的无线资源状态。

**对协议的具体改动点**：(1) 新增 IE 定义 9.2.2.xx "Radio Resource Status NR-U"，包含 DL Total PRB Usage 和 UL Total PRB Usage 两个必选字段（均 INTEGER(0..100)），语义为该 NR-U 信道上 DL/UL 全部业务的 PRB 使用量占小区总 PRB 数的百分比；(2) ASN.1 中在 NR-U-Channel-Item-ExtIEs 协议扩展容器中增加 { id-RadioResourceStatusNR-U, ignore, RadioResourceStatusNR-U, optional }，并新增 RadioResourceStatusNR-U ::= SEQUENCE { dL-Total-PRB-usage INTEGER(0..100), uL-Total-PRB-usage INTEGER(0..100), ... }；(3) 常量定义新增 id-RadioResourceStatusNR-U ProtocolIE-ID ::= xx5（编号待 MCC 分配，同批还列有 id-ChannelOccupancyTimePercentageUL、id-EnergyDetectionThresholdUL 等）。

**与 SON/MDT 功能的关系**：该 TP 属于 SON 中 MLB 功能的 Rel-18 NR-U 增强。邻区 gNB 通过 Xn 资源状态上报获得对端小区每个 NR-U 信道的占用率、ED 门限和 PRB 使用率后，可更准确地评估免许可载波上的真实剩余容量，从而做出更合理的负载均衡切换/重选决策。与 F1AP 侧的 R3-234545 为同一特性在两个接口上的配套 TP。

---

### R3-234545 (TP for SON BL CR for 38.473) NR-U enhancements for MLB
- **来源**: ZTE, Ericsson, Nokia, Nokia Shanghai Bell, Qualcomm Incorporated, Huawei
- **类型**: TP（文本提案），面向 TS 38.473 (F1AP) 的 Rel-18 SON Baseline CR
- **会议结论**: agreed
- **所属议题**: 议程 10.2.5 —— Rel-18 SON/MDT 增强 WI：SON for NR-U（免许可频谱 NR），移动性负载均衡（MLB）增强

#### 内容总结
**背景与要解决的问题**：在 CU/DU 分离架构中，NR-U 小区的信道占用和资源使用信息由 gNB-DU 掌握，需经 F1 接口上报给 gNB-CU，gNB-CU 才能进一步通过 Xn 与邻节点交换并用于 MLB 决策。本文档明确对应本次会议在线达成的协议：将工作假设（WA）"在 XnAP 和 F1AP 的 RESOURCE STATUS UPDATE 消息中按 NR-U 信道引入可选的 Radio Resource Status 负载度量"转为正式 agreement，并把 F1AP 部分落实到 SON BL CR。它与 XnAP 侧的 R3-234544 是同一特性的镜像改动。

**关键技术方案**：在 F1AP 资源状态报告过程中，gNB-DU 向 gNB-CU 发送的 9.2.1.23 RESOURCE STATUS UPDATE 消息的 Cell Measurement Result Item 内包含 **NR-U Channel List**（0..1，YES/ignore），每个 NR-U Channel Item 含：
- **NR-U Channel ID**（M）：标识上一上报周期内执行共享频谱信道接入过程的 NR-U 信道带宽部分（F1AP 语义比 XnAP 更细化）；
- **Channel Occupancy Time Percentage DL**（M，0..100）：该 NR-U 信道用于服务小区 DL 业务的信道占用时间百分比；
- **Energy Detection Threshold DL**（M，-100..-50 dBm）：gNB DL 信道侦听平均 ED 门限；
- **Channel Occupancy Time Percentage UL**（O，0..100）：UL 侧信道占用时间百分比（F1AP 中未含 UL ED 门限，这点与 XnAP 不同）；
- **本 TP 新增的 Radio Resource Status NR-U**（O，9.3.1.x，YES/ignore）：按 NR-U 信道的无线资源状态。

**对协议的具体改动点**：(1) 新增 IE 9.3.1.x "Radio Resource Status NR-U"，含必选的 DL Total PRB Usage 与 UL Total PRB Usage（均 INTEGER(0..100)），表示该 NR-U 信道上 DL/UL 全部业务 PRB 使用量占小区总 PRB 数的百分比；(2) ASN.1：在 NR-U-Channel-Item-ExtIEs（F1AP-PROTOCOL-EXTENSION）中新增 { id-RadioResourceStatusNR-U, ignore, RadioResourceStatusNR-U, optional }；新增类型 RadioResourceStatusNR-U ::= SEQUENCE { dl-Total-PRB-usage INTEGER(0..100), ul-Total-PRB-usage INTEGER(0..100), ... } 及其扩展容器；(3) 常量定义新增 id-RadioResourceStatusNR-U ProtocolIE-ID ::= xxx（编号待 MCC 分配），IE 定义段导入列表相应增加 id-RadioResourceStatusNR-U。

**与 SON/MDT 功能的关系**：本 TP 是 SON MLB 的 NR-U 增强在 F1 接口上的实现，使 gNB-CU 能从 DU 获得每个 NR-U 信道的占用时间百分比、ED 门限和 PRB 使用率，进而在整个 NG-RAN（经 XnAP，见 R3-234544）范围内进行免许可频谱感知的负载均衡；PRB 使用率与信道占用率结合可区分"本小区业务造成的负载"与"外部竞争导致的信道不可用"，提升 MLB 决策准确性。

---
