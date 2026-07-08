# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 README.md。

# 6. agreed / endorsed 文稿逐篇详细总结

以下按议题分组逐篇总结全部 35 篇 agreed / endorsed 文稿。每篇给出来源、类型、影响规范、会议结论与内容详解。


## 6.1 SON/MDT — 基线 CR（议程 10.1，endorsed）

### R3-233748 (BLCR to 38.413) for MDT

- **来源**: Ericsson
- **类型**: BL CR，影响 TS 38.413 (NGAP)，CR0990 rev 2，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本BL CR汇集Rel-18 MDT增强(重点是NPN网络中的MDT支持)对NGAP协议的全部已同意改动，rev1纳入了RAN3#120同意的R3-233470，rev2重新基于38.413 v17.5.0。

核心内容是在 MDT Configuration-NR IE (9.3.1.169) 的 Area Scope of MDT CHOICE 中新增面向NPN的MDT区域范围选项：
- **PNI-NPN Based MDT**：按CAG(闭合接入组)定义MDT范围，含 CAG List for MDT (PLMN ID + CAG ID，maxnoofCAGforMDT=256)；
- **SNPN Cell Based MDT**：按SNPN小区(NR CGI + NID)定义；
- **SNPN TAI Based MDT**：按SNPN TAI(TAI + NID)定义；
- **SNPN Based MDT**：按整个SNPN(PLMN Identity + NID，maxnoofMDTSNPNs取值FFS)定义。

同时新增独立IE **PNI-NPN Area Scope of MDT** (9.3.3.x，CAG列表)作为MDT Configuration-NR的可选扩展。当该IE存在时，原有Cell based/TA based/TAI based/PLMN wide范围仅覆盖非CAG小区(即仅提供公共接入的小区)，PNI-NPN区域的MDT测量采集范围则完全由该IE中列出的CAG区域定义。

过程文本方面，在 Initial Context Setup (8.3.1.2/8.3.1.4)、Handover Resource Allocation (8.4.2.2/8.4.2.4) 和 Trace Start (8.11.1.2/8.11.1.3) 三个过程中增加了对PNI-NPN Area Scope of MDT IE的处理规则；并规定异常情况：若PNI-NPN Area Scope of MDT IE与设置为"PNI-NPN based"的Area Scope of MDT IE同时出现，NG-RAN节点应使用后者(CHOICE内的PNI-NPN based分支)推导PNI-NPN区域的MDT范围并忽略前者。ASN.1相应新增 PNI-NPN-AreaScopeofMDT、PNI-NPNBasedMDT、SNPN-CellBasedMDT、SNPN-TAIBasedMDT、SNPN-BasedMDT 类型及协议IE ID(编号待MCC分配)。

配合关系：与XnAP的MDT BL CR (R3-233757) 相互对应——NGAP侧由AMF经Trace Start/初始上下文建立/切换资源分配下发NPN MDT配置，XnAP侧则保证该配置在Xn切换、Retrieve UE Context和MR-DC Trace Start中传递，二者共同实现签约/管理MDT在SNPN与PNI-NPN场景的端到端配置传递。

---

### R3-233794 (BLCR to 38.413) for SON

- **来源**: Ericsson
- **类型**: BL CR，影响 TS 38.413 (NGAP)，CR0964 rev 4，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本CR是Rel-18 SON增强(区别于MDT增强)在NGAP的基线文稿。rev0纳入RAN3#119同意的R3-231022，rev3剥离了MDT相关改动(移入新的MDT BL CR，即R3-233748)并纳入#119bis-e同意的R3-232021，rev4基于v17.5.0重新提交。

核心改动是扩展 **SON Information Report IE (9.3.3.35)**，该IE经NG接口的Uplink/Downlink RAN Configuration Transfer过程在无Xn连接的NG-RAN节点间中转SON信息。在既有的Failure Indication Information与HO Report Information两个分支之外：

1. 已有的 **Successful HO Report Information** 分支：携带Successful HO Report List(最多64条，每条为OCTET STRING容器，装载TS 38.331定义的SuccessHO-Report-r17)，支持SHR经核心网转发给源节点/配置节点；

2. 新增 **Successful PSCell Change Report Information** 分支：携带 Successful PSCell Change Report List(1..maxnoofSuccessfulPSCellChangeReports，取值FFS)，每条为 Successful PSCell Change Report Container (OCTET STRING，具体内容FFS，待RAN2确定SPR的RRC定义)，使SPR在取回节点与生成SPR时服务UE的MN之间无Xn时也能经NG接口转发。

ASN.1方面(9.4.5/9.4.7)：SONInformationReport CHOICE通过choice-Extensions新增 id-SuccessfulPSCellChangeReportList 分支(类型SuccessfulPSCellChangeReportInformation，criticality ignore)，新增 SuccessfulPSCellChangeReportList/-Item 类型定义、常量 maxnoofSuccessfulPSCellChangeReports(FFS) 及协议IE ID(3xx待分配)。

配合关系：本CR为SPR(成功PSCell变更报告)提供NG接口(经AMF中转)的传输路径，与XnAP侧ACCESS AND MOBILITY INDICATION中的Successful PSCell Change Report List (R3-233758)、38.300 stage-2的SPR转发规则(R3-233781第15.5.2.X节)以及37.340的SPR职责划分(R3-233775)配套，共同保证SPR最终到达执行根因分析的源/目标SN。

---

### R3-233757 (BLCR to 38.423) for MDT

- **来源**: Huawei
- **类型**: BL CR，影响 TS 38.423 (XnAP)，CR1050 rev 2，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本BL CR是Rel-18 MDT增强(NPN场景MDT支持)在XnAP接口的基线文稿，rev0合并了RAN3#119bis-e同意的R3-232091，rev1合并了RAN3#120同意的R3-233452，rev2基于v17.5.0重新提交。

主要改动与NGAP侧的MDT BL CR (R3-233748) 镜像对应：

1. **MDT Configuration-NR IE (9.2.3.126) 扩展NPN区域范围**：在Area Scope of MDT-NR CHOICE中新增 PNI-NPN based (CAG List for MDT：PLMN ID + CAG ID，最多256个)、SNPN Cell Based MDT (NR CGI + NID)、SNPN TAI Based MDT (TAI + NID)、SNPN Based MDT (PLMN Identity + NID，maxnoofMDTSNPNs为FFS)四种选项；并在该IE末尾新增可选的 **PNI-NPN Area Scope of MDT** 扩展IE (9.2.3.x)。原有Cell/TA/TAI based范围在PNI-NPN Area Scope of MDT存在时仅覆盖非CAG小区(只提供公共接入的小区)。

2. **过程文本**：在 Handover Preparation (8.2.1)、Retrieve UE Context (8.2.4) 和 Trace Start (8.3.14，MN向SN发起) 三个过程中增加对PNI-NPN Area Scope of MDT IE的处理——接收节点(目标NG-RAN节点/新NG-RAN节点/S-NG-RAN节点)据此推导PNI-NPN的MDT测量采集区域范围，并认为PNI-NPN区域范围仅由该IE定义；异常情况下若该IE与设为"PNI-NPN based"的Area Scope of MDT IE同时存在，则使用后者并忽略前者。

3. **ASN.1**：新增 PNI-NPNBasedMDT、PNI-NPN-AreaScopeofMDT、CAGListforMDT、SNPN-CellBasedMDT、SNPN-TAIBasedMDT、SNPN-NIDBasedMDT 等类型，AreaScopeOfMDT-NR通过choice-extension扩展，MDT-Configuration-NR通过IE扩展容器携带PNI-NPN-AreaScopeofMDT，新增常量maxnoofCAGforMDT=256、maxnoofMDTSNPNs=FFS及若干协议IE ID(编号待定)。

配合关系：确保NGAP下发的NPN MDT配置(签约MDT)能在Xn切换、RRC恢复取回UE上下文以及MR-DC下MN向SN启动Trace/MDT时无损传递，与R3-233748(NGAP)共同构成Rel-18 NPN MDT特性的接口信令基线。

---

### R3-233758 (BLCR to 38.423) Addition of SON features enhancement

- **来源**: Samsung
- **类型**: BL CR，影响 TS 38.423 (XnAP)，CR0934 rev 7，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

这是Rel-18 SON增强在XnAP接口的"总"基线CR，历经多次会议(#118、#119bis-e纳入R3-232002/232067/232142/232143、#120纳入R3-233491/233500)累积，rev7基于v17.5.0重新提交。覆盖四大特性：

1. **NR-U的SON/MLB增强**：在 RESOURCE STATUS UPDATE (9.1.3.21) 的小区测量结果中新增 NR-U Channel List，逐信道(NR-U Channel ID，最多16个)上报 DL信道占用时间百分比、DL能量检测门限(-100..-50 dBm)，并新增UL信道占用时间百分比和UL能量检测门限(gNB为UL信道侦听配置的最大ED门限平均值)，用于共享频谱负载均衡。

2. **MR-DC下RACH优化(RA Report取回)**：新增Class 2过程 **RACH Indication** (8.3.x)及 RACH INDICATION 消息(9.1.2.x)，由S-NG-RAN节点向M-NG-RAN节点指示UE处已有一个或多个仅SN可知的成功随机接入的RA report(携带RA Report Indication List，含M-NG-RAN UE XnAP ID)，MN据此从UE取回RA Report。同时在 ACCESS AND MOBILITY INDICATION (9.1.3.25) 的RACH Report List Item中新增 **PSCell List Container** IE(OCTET STRING，RAN2待定)，帮助接收节点确定RA Report Container应转发到哪个NG-RAN节点。

3. **SPR(成功PSCell变更报告)信令支持**：在 ACCESS AND MOBILITY INDICATION 中新增 **Successful PSCell Change Report List**(容器为OCTET STRING、内容待RAN2确定)，接收节点可用于优化PSCell变更/添加配置，条目内可含 **SN Mobility Information**(32比特位串，MN发往源SN时为源SN PSCell的移动性信息，发往目标SN时为目标SN PSCell的)；并在 S-NODE ADDITION REQUEST ACKNOWLEDGE (9.1.2.2) 与 S-NODE RELEASE REQUEST ACKNOWLEDGE (9.1.2.15) 中新增可选 SN Mobility Information IE(T-SN提供，用于事后分析导致错误PSCell变更的条件)，MN按TS 38.300存储使用。

4. ASN.1(9.3.3/9.3.4/9.3.5/9.3.7)同步新增上述过程、消息、IE与常量(maxnoofRAReportIndications、maxnoofSuccessfulPSCellChangeReports等部分取值FFS)。

配合关系：与38.300(R3-233781)、37.340(R3-233775)的stage-2描述对应；RACH Indication机制与F1接口(R3-233805/R3-234538)、X2接口EN-DC(R3-234372)的同名过程配套；SPR经NGAP转发由R3-233794支持。

---

