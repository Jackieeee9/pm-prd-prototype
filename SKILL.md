---
name: pm-prd-prototype
description: Turn requirement changes into a synchronized PRD + high-fidelity prototype inside one self-contained HTML. Use when asked to write or iterate a PRD, update requirements, add or change prototype pages, sync requirement text with prototype, maintain a revision log, or run document consistency checks.
description_zh: "个人产品经理 · PRD 与高保真原型一体化交付：需求拆条、影响面清单、原型与正文同步、术语枚举一致、脚本校验"
description_en: "One-piece PRD + high-fidelity prototype delivery workflow for product managers"
version: 1.0.0
allowed-tools: Read,Grep,Glob,Edit,Write,Shell
display_name: "PRD 与原型一体化交付"
display_name_en: "PRD + Prototype Delivery"
visibility: "private"
---

# PRD 与原型一体化交付

把零散需求变成**一份可评审的单文件 HTML**：左侧高保真原型、右侧需求正文、顶部原型/需求双模式切换。适用于 0-1 新需求和小版本迭代，迭代是主路径。

## 何时使用

- 用户提出一批需求变更，要求"更新需求内容和原型"
- 需要在一个文档里同时看交互与规则，供业务/研发评审
- 需要在已上线基线上做 vN → vN+1 的增量迭代
- 需要补齐状态流转、权限矩阵、接口说明、修订记录

**不适用**：纯视觉稿、纯数据分析报告、无评审对象的临时草稿。UAT 计划、上线配置表、上线检查清单属于**可选子流程**，被明确要求时才启动。

## 核心原则

1. **一个真相源**：原型改了，正文必须同步；正文改了，原型不能自相矛盾。
2. **先定名，再动手**：术语与枚举先对齐，再改代码和文字；改完扫描旧名，残留必须为 0（修订记录中的"更名说明"除外）。
3. **需求编号贯穿**：每条需求编号 R#，同时出现在影响面清单、正文小标题、修订记录里。
4. **不是所有需求都改原型**：按三分法分流（见下）。
5. **可运行优先**：每次改动后文档都能打开、无脚本报错、标签闭合。

## 工作流（8 步，1 道门禁）

### Step 0 需求拆条与分流
把输入拆成 R1…Rn，每条标注：摘要、变更类型（A/B/C）、是否涉及原型、是否涉及数据源/接口、是否涉及状态与权限。编号一经确定，全程复用。

### Step 1 歧义澄清
只问**影响交付口径**的歧义（同一个东西两个名字、两种实现、范围边界）。一次问一个，每个问题先给出推荐选项和理由；能自己从文档里查到的，不要问。用户答复要落成一句决策，写进影响面清单。

### Step 2 影响面清单（**唯一门禁**）
按 [影响面清单模板](references/impact-analysis-template.md) 逐条填写：涉及页面/弹窗、涉及 JS 函数、涉及正文章节、涉及枚举/术语、涉及权限/状态、涉及数据源/接口、风险点、验证方式。**提交用户确认后才开工**；确认后连续执行，中途只在出现新歧义时打断。

### Step 3 原型改动
顺序固定：**数据结构/HTML → 交互/JS → 样式**。每个区块改完都保持文档可运行。
- 用唯一锚点定位：页面 `page-*`、弹窗 `modal-*`、函数名、表格首列编号。
- 一次只改一个区块，`old_string` 必须带足上下文；同一段静态结构在详情页/复检页各有一份时，用全量替换并复核两处。
- 新增弹窗必须同时补：DOM、打开函数、提交函数、重置逻辑；新增按钮必须确认函数已存在，避免"能点但报错"。

### Step 4 正文同步（六面必查）
1. 功能清单：新增/变更能力一句话可检索
2. 页面章节：查询条件、列表字段、交互逻辑、导出字段
3. 状态流转：新增状态必须同时进"枚举、筛选项、流转表、权限表"
4. 权限矩阵：新按钮/新入口落到角色列
5. 数据源/接口：入参、出参、异常与降级、生效范围
6. 术语：与术语表一致，旧名清零

### Step 5 修订记录
在修订记录表**顶部**插入新版本，五要素：版本号、日期、作者、逐条对应 R# 的变更说明、是否涉及原型。模板见 [修订记录模板](references/revision-log-template.md)。纯文案/配置类变更不升版本号时，也要留一行轻量记录。

### Step 6 脚本校验（必跑）
```bash
python3 scripts/check_inline_js.py <file.html>
python3 scripts/check_html_nesting.py <file.html>
python3 scripts/check_tables_and_terms.py <file.html> --forbid "旧术语" --require "新术语"
```
全部通过才允许交付。任一失败：先修复，再重跑，不要"带着已知错误交付"。表格在存在 `rowspan` 时列数差异默认只告警，需要阻断时加 `--strict`。

### Step 7 验收与交付
按 [评审自检清单](references/review-checklist.md) 过一遍；浏览器能起来就人工点一遍主路径，起不来（如单文件 DOM 过大）就输出**手动验收步骤**，不要把 BLOCKED 当通过。交付时给出：`computer://` 文件链接、按 R# 的变更摘要、仍需确认的开放项。

## 三分法分流

| 类型 | 判定 | 原型 | 正文 | 修订记录 |
|---|---|---|---|---|
| A 页面型 | 有界面、字段、交互或状态变化 | 必改 | 六面必查 | 升版本号 |
| B 仅后端逻辑型 | 送检/判定/接口/免检规则变化 | 跳过 | 必须写清入参、取值、缺失降级、生效范围 | 升版本号 |
| C 纯文案配置型 | 措辞、示例、默认值等无逻辑变化 | 视情况 | 局部修订 | 轻量记录，不升版本号 |

B 类不要为了"格式统一"硬塞原型占位；C 类不要为改一句话写一节新需求。

## 单文件双模式治理

- **必留锚点**：每个页面/弹窗/关键函数都有稳定 id 或函数名，供需求正文引用和后续定位。
- **按区改动**：禁止整文件重写；单次改动跨 10 个以上区块时，先拆成多轮。
- **拆分红线**：文件超过 2 万行，或页面 DOM 超过 1.5 万节点，或浏览器自动化连续两次无法交互 → 主动提议拆分（原型/需求分文件或按模块拆），并说明拆分成本。
- **图表等外部依赖**：引用了本地不存在的资源时，确认是否有降级渲染；没有就如实告知，不要假装图表正常。

## 可复用资产

- 高保真片段（列表行、弹窗骨架、表单控件、toast、日期区间）：[assets/snippets.md](assets/snippets.md)
- 术语与枚举清单：[references/terminology-and-enums.md](references/terminology-and-enums.md)
- 影响面清单模板：[references/impact-analysis-template.md](references/impact-analysis-template.md)
- 评审自检清单：[references/review-checklist.md](references/review-checklist.md)
- 修订记录模板：[references/revision-log-template.md](references/revision-log-template.md)

## 常见坑（每次开工前扫一眼）

- 加按钮没加函数 → 点击报错；加弹窗没写重置 → 上一次的勾选状态残留。
- 新增状态只改了列表徽标，漏了筛选项、导出字段、状态流转表、权限矩阵。
- 同一数据源两种叫法（如"人工视频面签/人工面签视频"）→ 先统一再改。
- 改表格行时误删容器闭合标签 → 用嵌套校验脚本兜底。
- 只改原型不改正文，或只改正文不改原型 → 评审时必被发现。
- 把"仅后端逻辑"需求做成前端页面 → 范围失控。
