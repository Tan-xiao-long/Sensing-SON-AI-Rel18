# 3GPP Release 18 SON 与 AI 相关议题调研报告（RAN3#121）

> 本文件为调研报告拆分版之一，完整目录见 00_README.md。

### R3-233772 (BLCR to 36.300) Addition of SON features enhancement

- **来源**: Lenovo
- **类型**: BL draft CR，影响 TS 36.300 (E-UTRAN总体描述，stage-2)，CR号未分配(draftCR)，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本BL CR为Rel-18 SON增强在LTE侧stage-2规范36.300中的基线文稿，rev1(R3-233536)在RAN3#120纳入两项改动，本版为向RAN3#121的重新提交。改动集中在两个条款：

1. **22.4.2.2a (inter-RAT移动性导致的连接失败) —— 语音回落(Voice Fallback)MRO增强**：在MRO需检测的问题中，除Too Early/Too Late inter-RAT切换外新增 **Inter-system Mobility Failure for Voice Fallback**，定义为：因语音回落从NG-RAN小区向E-UTRAN小区触发的切换成功后不久发生RLF、或切换过程中失败，UE尝试重连到E-UTRAN或NG-RAN小区。并给出eNB侧的检测机制：连接失败发生在LTE小区，且失败前存在最近一次由NR语音回落触发的inter-system切换(UE上报的timer小于门限如Tstore_UE_cntxt)，同时UE的RLF Report中带有voice fallback指示(该指示名称留有编者按，待RAN2确定细节)。这使得目标LTE小区中发生的语音回落切换失败能被正确归类，而不被误判为普通Too Early inter-RAT切换。

2. **22.4.3.2.2 (EN-DC下NR小区的RACH优化) —— RA报告命名更新**：将UE上报的"RACH information report"统一更名为 RACH information report(RA report相关的naming update)，明确EN-DC场景下RACH优化由UE上报信息(RACH information report，见TS 38.300)在eNB侧获得并进一步转发给en-gNB，以及en-gNB与eNB间的PRACH参数交换来支持。

配合关系：本CR是LTE侧stage-2，与38.300 BL CR (R3-233781) 中NG-RAN侧的Inter-system Mobility Failure for Voice Fallback定义及检测机制相互对应(一个描述最后服务节点为E-UTRAN节点的情形，一个描述NG-RAN节点情形)；语音回落失败指示的跨接口传递由36.423/38.423/38.413相关CR支撑，RA report命名更新与X2AP(R3-234372)、XnAP(R3-233758)保持一致。

---

### R3-233781 (BLCR to 38.300) Addition of SON features enhancement

- **来源**: CMCC
- **类型**: BL draft CR，影响 TS 38.300 (NR总体描述，stage-2)，CR号未分配(draftCR，rev 8)，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本CR是Rel-18 SON增强的NR侧stage-2"总"基线，自RAN3#117bis-e起历经8个版本，累积了#119(R3-231043)、#119bis-e(R3-232099/232151)、#120(R3-233397/233408)等成果，改动集中在15.5自优化章节：

1. **15.5.2.1 MRO总述扩展**：MRO检测目标新增 **Inter-system voice fallback failure** 与 **Fast MCG recovery failure** 两类问题；可观测的次优成功事件除intra-NR成功切换外新增 **inter-RAT成功切换** 以及 **成功PSCell添加/变更**。

2. **15.5.2.2.3 inter-system移动性连接失败**：新增 **Inter-system Mobility Failure for Voice Fallback** 的定义(因语音回落从NG-RAN向E-UTRAN切换成功后不久RLF或切换中失败)及NG-RAN侧检测机制——语音回落切换期间/之后失败且RLF Report含voice fallback指示(名称留编者按待RAN2)；失败指示经Xn的Failure Indication或NG的Uplink/Downlink RAN Configuration Transfer送达最后服务节点。

3. **15.5.2.4 inter-system乒乓**：注明由Voice Fallback触发的inter-system移动不计为乒乓。

4. **15.5.2.7 成功切换(SHR)转发增强**：针对inter-RAT SHR，规定当取回SHR的NG-RAN节点既非该切换的源也非目标时，可将其转发给配置了产生该SHR的触发条件的节点(经Xn的ACCESS AND MOBILITY INDICATION或NG的RAN配置传递过程)。

5. **新增15.5.2.X 成功PSCell添加/变更报告(SPR)**：UE按网络配置记录SPR(存储至被取回或48小时)，任一gNB取回后经Xn AMI消息或NG RAN配置传递转发给SPR生成时服务该UE的MN。

6. **15.5.3 RACH优化**：RACH report更名为RA report(naming update)；新增"SN RA Reports"——NR-DC下UE可在SN的PSCell收集RA Report；MR-DC下UE在SN成功随机接入后，SN经RACH indication告知MN其RA Report可用性，MN经XnAP指示从UE取回。

配合关系：作为stage-2总纲，对应stage-3落地为XnAP(R3-233758)、NGAP(R3-233794)、F1AP(R3-233805)、38.401(R3-233790)、37.340(R3-233775)与36.300(R3-233772)等各BL CR。

---

### R3-233775 (BLCR to 37.340) Addition of SON Rel.18 features

- **来源**: Nokia, Nokia Shanghai Bell
- **类型**: BL draft CR，影响 TS 37.340 (MR-DC stage-2)，CR号未分配(draftCR)，Cat B，基于 v17.5.0
- **会议结论**: endorsed as BL CR (基线CR，未来打包提交RAN全会批准)
- **所属议题**: Rel-18 SON/MDT WI (NR_ENDC_SON_MDT_enh2-Core，WID RP-231157) 议程10.1

#### 内容总结

本BL CR为Rel-18 SON增强中与MR-DC/EN-DC相关特性的stage-2基线，累积了RAN3#119bis(R3-232062)与#120(R3-233379、R3-233456)的成果，新增三块stage-2描述(10.18.A/B/C)并在3.2缩写表中加入CPA、CPAC、CPC、SPR等缩写：

1. **10.18.A CPAC失败的MRO**：定义条件PSCell添加/变更(CPAC)的三类失败事件——**Too Late CPC Execution**(收到CPC配置但执行条件满足前发生SCG失败，且测量显示存在不同于源PSCell的合适PSCell)；**Too Early CPC/CPA Execution**(CPC/CPA执行失败或执行成功后不久SCG失败，CPC情形源PSCell仍合适、CPA情形无合适PSCell)；**CPC/CPA Execution to wrong PSCell**(执行失败或成功后不久SCG失败，且合适PSCell既非源也非目标)，后者进一步区分两个子情形：若合适PSCell在发起节点提供给(候选)目标SN的候选列表中但未被目标SN选中，属目标SN的wrong target PSCell selection；否则属发起CPC的节点或发起CPA的MN的wrong candidate PSCell list selection。"成功CPC/CPA执行"以UE完成RA过程为准。

2. **10.18.B 成功PSCell变更报告(SPR)**：目的是检测次优的成功PSCell变更/CPC及成功PSCell添加/CPA。UE按网络配置记录SPR并按TS 38.331提供给网络。触发门限的职责划分：PSCell添加/CPA及MN或SN发起的PSCell变更/CPC，**T304触发始终由目标SN决定**并由其做根因分析；SN发起的PSCell变更/CPC的**T310/T312触发由源SN决定**并分析。SPR的取回规则：UE仍连接MN时只能由MN取回；若UE已不连接该MN，可由其他节点取回，此时须先转发给下发SPR配置的MN，再由该MN转发给应执行SPR优化的相应SN。

3. **10.18.C RA Report取回**：当UE在SN执行仅SN可知的成功随机接入(如波束失败恢复、UL失步、SR失败、无PUCCH资源)时，SN可经RACH indication告知MN，MN据此从UE取回RA Report。

配合关系：对应的信令支持分别落在XnAP(R3-233758的RACH Indication过程、SPR相关IE)、X2AP(R3-234372)、38.300(R3-233781的SPR转发)与NGAP(R3-233794)。

---
