# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-234372 (BL CR to 36.423) Addition of SON features enhancement

- **来源**: CATT
- **类型**: BL CR，影响 TS 36.423 (X2AP)，CR1747 rev 3，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本CR是Rel-18 SON增强在X2AP(EN-DC场景)的基线文稿。rev0纳入RAN3#119bis-e同意的R3-232104，rev1纳入#120同意的R3-233499，rev3更新封面页。改动聚焦RACH优化增强在EN-DC下的支持，包括两项：

1. **RA report命名更新**：将"RACH report"统一改名为"RA report"。体现在 ACCESS AND MOBILITY INDICATION (9.1.2.50，eNB→en-gNB) 消息中：NR RACH Report List/NR RACH Report Container(OCTET STRING，装载TS 38.331定义的RA-ReportList-r16)及可选UE Assistant Identifier(en-gNB UE X2AP ID)的相关表述与引用同步更新，与RAN2及38.300/36.300的命名保持一致。

2. **新增RACH Indication过程**：在8.1 Class 2过程表中登记 **RACH Indication**，新增8.3.x流程文本：由 **en-gNB向MeNB** 发送RACH INDICATION消息，告知在en-gNB处执行了一次或多次(仅SN可知的)成功随机接入、UE处已有相应RA report；MeNB收到后可从UE取回RA report(流程文本留有编者按，可随后续协议进展更新)。新增 **RACH INDICATION消息 (9.1.2.x)**：携带RA Report Indication List(1..maxnoofRAReportIndications，取值FFS)，每项含MeNB UE X2AP ID(必选)及MeNB UE X2AP ID Extension(可选)以标识UE。

3. **ASN.1改动 (9.3.3/9.3.4/9.3.5/9.3.7)**：新增RachIndication过程定义(ProcedureCode编号xx待MCC分配，id-rachIndictaion)、RACH INDICATION消息PDU、RAReportIndicationList及Item类型、常量maxnoofRAReportIndications(FFS)等。

配合关系：本CR把38.300/36.300(R3-233781、R3-233772)与37.340(R3-233775)stage-2定义的"SN经RACH indication告知MN、MN取回RA Report"机制落地到EN-DC的X2接口，是XnAP RACH Indication (R3-233758，MR-DC/NG-RAN场景)与F1AP RACH Indication (R3-233805，CU-DU分离场景)在X2接口上的平行实现；RA report经eNB取回后仍通过ACCESS AND MOBILITY INDICATION转发给en-gNB用于其RACH参数优化。

---

### R3-233805 (BLCR to 38.473) Addition of SON features enhancement

- **来源**: Huawei
- **类型**: BL CR，影响 TS 38.473 (F1AP)，CR1105 rev 5，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本CR是Rel-18 SON增强在F1AP的基线文稿，累积了RAN3#118(R3-226911)、#119(R3-230980)、#119bis等会议成果，rev5为编辑性调整(9.4.7排序)后向#121重新提交。主要涵盖三块特性：

1. **RACH优化增强——新增RACH Indication过程**：在8.1的Class 2过程表中登记 **RACH Indication**，新增8.2.x流程文本：gNB-DU发起，向gNB-CU通知在DU发生、而CU不可知的一次或多次成功随机接入(非UE关联信令)；gNB-CU收到后可触发从UE取回RACH Report。新增 **RACH INDICATION消息 (9.2.1.x)**：携带RA Report Indication List(1..maxnoofRAReportIndications，FFS暂定256)，每项含gNB-CU UE F1AP ID用于标识相关UE。ASN.1中新增RachIndication过程(ProcedureCode 99，MCC分配)及RAReportIndicationList类型。

2. **SPR支持——扩展ACCESS AND MOBILITY INDICATION (9.2.10.1)**：在原有RACH Report Information List、RLF Report Information List、Successful HO Report Information List基础上新增 **Successful PSCell Change Report Information List**(1..maxnoofSuccessfulPSCellChangeReports，暂定64/FFS，容器内容待RAN2)，gNB-DU收到后可用于优化PSCell变更/添加相关参数。8.11.1流程文本同步增加该IE的处理句。

3. **NR-U的SON(负载上报)——扩展RESOURCE STATUS UPDATE (9.2.1.23)**：在小区测量结果中新增 **NR-U Channel List**(每小区最多maxnoofNR-UChannelIDs个信道)，每项含NR-U Channel ID、DL信道占用时间百分比(0..100)、DL能量检测门限(-100..-50 dBm)，并以扩展IE增加 **Channel Occupancy Time Percentage UL**，供CU掌握DU侧共享频谱各NR-U信道的占用情况。

ASN.1(9.4.3/9.4.4/9.4.5/9.4.7)同步新增过程定义、消息PDU、IE类型与常量(id-RAReportIndicationList=900、id-ChannelOccupancyTimePercentageUL=901、id-SuccessfulPSCellChangeReportList=902等，MCC分配)。

配合关系：RACH Indication与38.401(R3-233790)、38.470(R3-234538)的架构/功能描述配套，是XnAP/X2AP同名过程在CU-DU分离场景的对应物；SPR信息列表与XnAP(R3-233758)、NGAP(R3-233794)的SPR转发链路衔接，把SPR最终送到管理相应小区参数的gNB-DU；NR-U负载指标与XnAP RESOURCE STATUS UPDATE中的NR-U Channel List(R3-233758)对应。

---

### R3-234538 (BLCR to 38.470) Addition of SON features enhancement

- **来源**: CMCC
- **类型**: BL CR，影响 TS 38.470 (F1一般性规范与原则)，CR0114 rev 2，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本CR是Rel-18 SON增强(RACH优化增强)在F1接口一般性规范38.470中的基线文稿，篇幅极小。rev0纳入RAN3#120同意的R3-233498，rev2将基线版本更新为17.5.0。

改动包括两处：

1. **5.2.10 自优化支持功能(Self-optimisation support function)**：在原有"gNB-CU向gNB-DU提供信息以支持自优化"的单向功能描述基础上，新增反方向描述——该功能同样允许 **gNB-DU向gNB-CU提供信息** 以支持自优化功能。

2. **6.1.10 自优化支持过程(Self-optimisation support procedure)**：原有描述为自优化支持过程用于从gNB-CU向gNB-DU传递失败与移动性相关信息(即Access and Mobility Indication过程)；本CR新增：用于 **从gNB-DU向gNB-CU指示SON相关信息可用性** 的自优化支持过程——**RACH Indication**。

即本CR在F1功能与过程清单层面正式登记了Rel-18新引入的DU→CU方向RACH Indication过程，使38.470的功能划分与F1AP协议保持一致。

配合关系：具体消息与IE定义见F1AP BL CR (R3-233805)——其中定义了RACH INDICATION消息(携带RA Report Indication List/gNB-CU UE F1AP ID)及流程文本；架构层面的功能描述(gNB-DU告知gNB-CU仅DU可知的成功随机接入、CU据此从UE取回RA Report)在38.401 BL CR (R3-233790) 的7.5节；该机制与XnAP(R3-233758)、X2AP(R3-234372)中SN→MN的RACH Indication构成同一RACH优化增强特性在不同接口上的平行实现。

---

### R3-233790 (BLCR to 38.401) Addition of SON features enhancement

- **来源**: ZTE
- **类型**: BL CR，影响 TS 38.401 (NG-RAN架构)，CR0282 rev 3，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本CR是Rel-18 SON增强中RACH优化增强在CU-DU分离架构规范38.401的基线文稿，篇幅很小，仅改动7.5节"RACH Optimisation Function"。rev0纳入RAN3#119同意的R3-230996，rev2纳入RAN3#119bis-e同意的R3-232101，rev3为向#121重新提交。

两项改动：

1. **命名更新**：将gNB-CU经F1AP发给gNB-DU的"RACH report"表述改为从UE **取回(retrieved from)** 的 **RA Report**，与RAN2/其他RAN3规范中的RA report命名统一。CU-DU分离下RACH配置冲突检测与解决功能位于gNB-DU，gNB-CU把从UE取回的RA report经F1AP发给gNB-DU用于RACH优化，gNB-DU向gNB-CU上报每小区PRACH配置，gNB-CU可将邻gNB及其他gNB-DU的邻小区PRACH配置转发给gNB-DU以解决配置冲突(此为既有功能框架)。

2. **新增"RA Report retrieval"功能描述**：当UE执行了仅gNB-DU可知的成功随机接入(例如波束失败恢复、上行失步、调度请求失败、无PUCCH资源可用等场景)时，gNB-DU可经 **RACH indication** 告知gNB-CU这些成功随机接入过程的发生；gNB-CU随后可基于经F1AP收到的RACH indication从相应UE取回RA Report。

配合关系：本CR是该机制在CU-DU分离架构下的stage-2锚点，具体信令由F1AP BL CR (R3-233805) 的新Class 2过程RACH Indication与RACH INDICATION消息实现，38.470 BL CR (R3-234538) 在F1一般性规范中补充相应功能/过程描述；其架构思路与MR-DC场景下SN→MN的RACH indication (37.340 R3-233775、XnAP R3-233758、X2AP R3-234372) 完全平行，共同构成Rel-18 RACH优化增强(网络侧触发RA Report取回)的完整方案。

---

