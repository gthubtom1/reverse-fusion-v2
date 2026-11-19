# 单写者规则（R7 防线 4）

只有阶段负责人写 lifecycle/STATE.yaml 和 MANIFEST.yaml；并行子智能体只写自己领域的目录（cases/<领域>/）。冲突先行者优先，后者在原文件上 append，不覆盖。
