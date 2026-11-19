# unknowns.md — cases/netwin-1

- 样本是自建 .NET 程序（学习目标），非真实第三方 .NET/厚客户端项目。真实 .NET 可能带混淆/加固，未测。
- 未做 dnSpyEx/de4dot 的实际反编译流程（本案例直接读源码 + 静态分析）；技能要求的「优先用 dnSpyEx」本机未跑。
- 未覆盖厚客户端 GUI、native 混合、脱壳等场景；仅覆盖托管 .NET 校验算法。
- 合法序列号是暴力解出的单例（AAA-AAA-AAA|）；规则本身的弱校验（mod 256）是自建目标的固有属性。
