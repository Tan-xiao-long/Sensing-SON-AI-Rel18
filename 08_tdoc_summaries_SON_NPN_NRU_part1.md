# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

## 6.5 SON/MDT — 非公共网络 NPN（议程 10.2.4）

### R3-234718 (TP for MDT BLCRs for TS38.413) MDT support in NPN
- **来源**: ZTE, Ericsson, Huawei, Nokia, Nokia Shanghai Bell
- **类型**: TP（文本提案），面向 TS 38.413 (NGAP) 的 Rel-18 MDT Baseline CR
- **会议结论**: agreed unseen
- **所属议题**: 议程 10.2.4 —— Rel-18 SON/MDT 增强 WI (NR_ENDC_SON_MDT_enh2)：非公共网络（NPN）的 SON/MDT 支持

#### 内容总结
**背景与要解决的问题**：Rel-18 SON/MDT 增强 WI 的一项目标是使 MDT（最小化路测）数据采集能够在非公共网络（NPN）部署中进行，包括 PNI-NPN（公共网络集成的 NPN，通过 CAG 小区实现）和 SNPN（独立 NPN，由 PLMN ID + NID 联合标识）。此前会议已在 NGAP 的 MDT 区域范围（Area Scope）中引入了 NPN 相关分支，但 SNPN 列表的最大条目数仍标记为 FFS（待研究）。本篇 TP 的直接目的即为完成这一遗留问题：**将 MDT SNPN List 中 SNPN 的最大数目确定为 16**（把范围界 maxnoofMDTSNPNs 的取值从 "FFS" 改为 16），从而使 NGAP MDT 配置的 NPN 部分完整可用。选择 16 是为了支持"等效 SNPN (equivalent SNPN)"场景，与 RAN3 同次会议发出的 LS（R3-234744）中的说明一致。

**关键技术方案**：TP 展示了修改后的 NGAP 9.3.1.169 "MDT Configuration-NR" IE 的完整表格，其中 NPN 相关的 Area Scope of MDT 选择分支包括：
- **PNI-NPN Based MDT**：包含 CAG List for MDT（1..maxnoofCAGforMDT，最多 256 个），每项含 PLMN ID + CAG ID，即 MDT 仅在指定 CAG 内采集；
- **SNPN Cell Based MDT**：SNPN Cell ID List（最多 32 个 NR CGI，每项附 NID，NR CGI 中的 PLMN ID 与 NID 共同标识一个 SNPN）；
- **SNPN TAI Based MDT**：SNPN TAI List（最多 8 个 TAI，每项附 NID）；
- **SNPN Based MDT**：MDT SNPN List（1..maxnoofMDTSNPNs），每项含 PLMN Identity + NID，即整个 SNPN 范围内采集。
此外，传统的 Cell based / TA based / TAI based / PLMN wide 分支的语义描述中增加说明：若 PNI-NPN Area Scope of MDT IE 存在，则这些分支仅覆盖非 CAG 小区（即仅提供公共接入的小区），实现"公网区域 + 特定 CAG"混合采集（对应用例 2）。MDT 配置末尾还新增可选的 PNI-NPN Area Scope of MDT IE（9.3.3.x，Criticality YES/ignore）。

**对协议的具体改动点**：本次 TP 相对已 endorse 的 BL CR 的净改动是：范围界表中 maxnoofMDTSNPNs 的解释由 "Value is FFS" 改为 "Value is 16"；对应 ASN.1 常量定义 maxnoofMDTSNPNs INTEGER ::= 由 FFS 改为 16（文本中可见修订痕迹 "16FFS"/"FFS16"）。

**与 SON/MDT 功能的关系**：该 TP 完善了信令面（NG 接口）向 NG-RAN 传递 NPN 感知 MDT 区域范围的能力，是 signalling based MDT 在 NPN 场景下的核心信令支撑，与同次会议的 XnAP TP（R3-234719）和 TS 37.320 阶段 2 BL CR（R3-234720）配套，并通过 LS R3-234744 通知 RAN2/SA5 做相应的 stage-3/OAM 规范修改。

---

### R3-234719 (TP for MDT BLCRs for TS38.423) MDT support in NPN
- **来源**: Huawei, Ericsson, ZTE
- **类型**: TP（文本提案），面向 TS 38.423 (XnAP) 的 Rel-18 MDT Baseline CR
- **会议结论**: agreed unseen
- **所属议题**: 议程 10.2.4 —— Rel-18 SON/MDT 增强 WI (NR_ENDC_SON_MDT_enh2)：非公共网络（NPN）的 SON/MDT 支持

#### 内容总结
**背景与要解决的问题**：为在 NPN（非公共网络）部署中支持 MDT 数据采集，MDT 配置（含区域范围）需要在 Xn 接口上随 UE 上下文在 NG-RAN 节点间传递（例如切换时 MDT 配置的延续）。本文档是把本次会议就 NPN MDT 达成的协议改动落实到 XnAP 的 TP，与 NGAP 侧的 R3-234718 完全对齐，核心同样是完成 SNPN 列表最大条目数的确定（16，替换原来的 FFS）。

**关键技术方案**：TP 给出修改后的 XnAP 9.2.3.126 "MDT Configuration-NR" IE 表格。在 CHOICE Area Scope of MDT-NR 下，除既有的 Cell based / TA based / TAI based 分支外，包含以下 NPN 分支（均带 Criticality YES/ignore，保证与旧版本节点的后向兼容）：
- **PNI-NPN based**：CAG List for MDT（1..maxnoofCAGforMDT=256），每项含 PLMN ID（9.2.2.4）+ CAG ID（9.2.2.66），限定 MDT 只在指定 CAG（封闭接入组）小区内进行；
- **SNPN Cell Based MDT**：SNPN Cell ID List for MDT（最多 32 个），每项为 NR CGI + NID（9.2.2.65），NID 与 NR CGI 中的 PLMN ID 共同标识 SNPN；
- **SNPN TAI Based MDT**：SNPN TAI List（最多 8 个），每项为 TAI + NID；
- **SNPN Based MDT**：MDT SNPN List（1..maxnoofMDTSNPNs），每项为 PLMN Identity + NID，表示在整个 SNPN 范围内采集。
同时，Cell based / TA based / TAI based 分支的语义栏说明：若 PNI-NPN Area Scope for MDT IE 存在，则这些分支只覆盖非 CAG 小区（仅提供公共接入的小区），从而支持"公网区域与特定 CAG 组合"的采集用例。IE 末尾另有可选的 PNI-NPN Area Scope of MDT（9.2.3.x，YES/ignore）。表格同时覆盖 Immediate MDT（M1/M2/M4–M7 测量位图及各测量配置、位置信息、蓝牙/WLAN/传感器测量配置）和 Logged MDT（logging interval/duration、周期/事件触发上报、邻区范围、早测量指示）等既有内容。

**对协议的具体改动点**：范围界 maxnoofMDTSNPNs 的解释由 FFS 确定为 "Value is 16"；ASN.1 常量定义部分相应将 maxnoofMDTSNPNs INTEGER ::= FFS 改为 16（文本中留有 "16FFS"/"FFS16" 修订痕迹）；其余 NPN 分支（CAG 列表、SNPN 小区/TAI/SNPN 列表）为此前已 endorse 到 BL CR 的内容在本 TP 中一并呈现。

**与 SON/MDT 功能的关系**：该 TP 保证 NPN 感知的 MDT 区域范围信息可经 Xn 接口在 gNB 间传递，使 signalling based 与 management based MDT 在 UE 移动（Xn 切换/上下文获取）时保持 NPN 限定的采集范围，与 NGAP TP（R3-234718）、TS 37.320 BL CR（R3-234720）构成一套完整方案。

---

### R3-234720 Introduction of MDT enhancements to support Non-Public Networks (BL CR to TS 37.320)
- **来源**: Nokia, Nokia Shanghai Bell, Ericsson, ZTE, Huawei（R3-234132 的修订版）
- **类型**: CR（Change Request，类别 B，新增特性），TS 37.320 v17.4.0，Rel-18，工作项目 NR_ENDC_SON_MDT_enh2-Core；影响条款 3.3、5.1.1.1.1、5.1.3、5.4.x（新增）
- **会议结论**: endorsed as BL CR unseen
- **所属议题**: 议程 10.2.4 —— Rel-18 SON/MDT 增强 WI：非公共网络（NPN）的 SON/MDT 支持

#### 内容总结
**背景与要解决的问题**：TS 37.320 是 MDT 的阶段 2 总体描述规范。为便于在 NPN 部署中开展 MDT 数据采集，RAN3 已就以下内容达成一致并需写入该规范：支持三个用例——用例 1：增强区域范围信息使 MDT 测量可仅在特定 PNI-NPN（特定 CAG）内采集；用例 2：可同时在特定 PNI-NPN（CAG）和公网区域（特定公网小区、TAI 等）内采集；用例 3：在 UE 注册的 SNPN 内采集。同时约定：NPN 场景下同时支持基于信令（signalling based）和基于管理（management based）的 MDT，同时支持 immediate MDT 和 logged MDT；在 MDT 区域范围中引入面向 NPN 的独立 CAG 列表；并根据 SA3 在 S3-231399 中的反馈，明确 MDT 用户同意（user consent）不适用于由 SNPN 服务的 UE。

**具体改动点**：
1. **3.3 缩写**：新增 NPN（Non-Public Network）、PNI-NPN（Public Network Integrated NPN）、SNPN（Stand-alone NPN）等缩写。
2. **5.1.1.1.1 Logged MDT 配置参数**：扩展日志区域（logging area）配置——原有"最多 32 个全球小区标识"和"最多 8 个 TA/LA/RA"两类范围改为面向 PLMN，并对 NR 增加：最多 256 个 PNI-NPN 的列表（可与小区/TA 列表之一或两者组合配置，UE 仅在驻留于所列小区和/或 CAG 时记录测量）；单独的最多 256 个 PNI-NPN 列表；最多 16 个 SNPN 的列表；面向 SNPN 的最多 32 个全球小区标识列表；面向 SNPN 的最多 8 个 TA 列表。并规定所配置的日志区域可跨越 MDT PLMN List 中的各 PLMN（未配置区域时 UE 在整个 MDT PLMN List 范围内记录），或跨越任何已配置的 SNPN 区域。留有编者注：PNI-NPN 的区域范围与术语更新待 RAN2 完成相应 stage-3 工作后再定（FFS）。
3. **5.1.3 MDT 发起**：在用户同意相关描述后新增一句关键规则："User consent does not apply if the UE is served by an SNPN"（UE 由 SNPN 服务时不适用用户同意），这是对 SA3 回复 LS 的落实——SNPN 属专网，不涉及公网意义上的路测同意机制。
4. **新增 5.4.x "Support of NPN"**：声明 MDT 在 PNI-NPN 和 SNPN 中均被支持。

**与 SON/MDT 功能的关系**：本 CR 是 NPN MDT 特性的阶段 2 框架，定义了 UE/网络行为层面的区域范围与用户同意规则；其信令面实现分别由 NGAP TP（R3-234718）、XnAP TP（R3-234719）承载，并作为附件随 LS R3-234744 发送给 RAN2 和 SA5，请其在 RRC（TS 38.331）与 OAM/Trace（TS 32.422）规范中做对应修改。

---

