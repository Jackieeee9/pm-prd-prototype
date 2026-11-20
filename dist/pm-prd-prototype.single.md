---
name: pm-prd-prototype
description: 把需求变更落成"一份可评审的单文件 HTML"（左侧高保真原型、右侧需求正文）。当用户要求编写或迭代 PRD、更新需求、调整原型页面、同步需求正文与原型、维护修订记录、做文档一致性检查时使用。Triggers: PRD, 需求迭代, 小版本, 原型, 修订记录, requirement update, prototype sync.
---

# 个人产品经理 · PRD 与原型一体化交付（单文件兼容版）

> 本文件是精简兼容版：模板、清单、片段已内联，不依赖 `references/`。
> 适用：只支持单条规则/指令的工具（Cursor、Windsurf、Copilot、Cline 等）。
> 支持 `SKILL.md` 的工具（Claude Code、Trae）用原多文件版体验更好。

## 0. 工具适配（首次使用后删除本节）

- **Cursor**：放到 `.cursor/rules/pm-prd-prototype.mdc`，把顶部 frontmatter 换成 `description:` + `alwaysApply: false`。
- **Windsurf**：放到 `.windsurf/rules/pm-prd-prototype.md`。
- **Copilot**：合并进 `.github/copilot-instructions.md`，或放 `.github/instructions/pm-prd.instructions.md`。
- **Claude Code / Trae**：放入对应 skills 目录，无需改动。
- **无法执行脚本时**：按第 6 节的"降级校验"人工核对，不要声称已通过。

## 1. 定位与边界

**做**：0-1 新需求与小版本迭代（迭代为主路径），产出一份单文件 HTML：左原型、右需求、顶部双模式切换。

**不做**：纯视觉稿、数据分析报告、临时草稿。UAT 计划、上线配置表、上线清单属**可选子流程**，被明确要求时才启动。

## 2. 核心原则

1. **一个真相源**：原型改了正文必须同步；正文改了原型不能自相矛盾。
2. **先定名再动手**：术语与枚举先对齐，改完扫旧名，残留必须为 0（修订记录里的更名说明除外）。
3. **需求编号贯穿**：每条需求编号 R#，出现在影响面清单、正文小标题、修订记录。
4. **不是所有需求都改原型**：按三分法分流。
5. **可运行优先**：每次改动后文档能打开、无脚本报错、标签闭合。

## 3. 八步流程（1 道门禁）

### Step 0 拆条与分流
把输入拆成 R1…Rn，逐条标注：摘要、类型（A/B/C）、是否涉及原型、是否涉及数据源/接口、是否涉及状态与权限。编号全程复用。

### Step 1 澄清歧义
只问**影响交付口径**的歧义（同物两名、两种实现、范围边界）。一次一个，先给推荐方案和理由；能自己查文档的不问。答复落成一句决策，写进影响面清单。

### Step 2 影响面清单（**唯一门禁**）
逐条填写下表，**用户确认后才开工**；确认后连续执行，只在出现新歧义时打断。

| 编号 | 需求摘要 | 类型 | 页面/弹窗 | JS 函数 | 正文章节 | 枚举/术语 | 权限/状态 | 数据源/接口 | 风险点 | 验证方式 |
|---|---|---|---|---|---|---|---|---|---|---|

补充记录：开放问题（问题 / 推荐方案 / 结论）。

### Step 3 原型改动
顺序固定：**结构/HTML → 交互/JS → 样式**，每步保持可运行。
- 用稳定锚点定位：`page-*`、`modal-*`、函数名、表格首列编号。
- 一次只改一个区块，替换串要带足上下文；同一段结构在详情页/复检页各有一份时，全量替换后两处复核。
- 新弹窗必须四件套：DOM、打开函数、提交函数、重置逻辑；新按钮先确认函数存在。

### Step 4 正文同步（六面必查）
1. 功能清单 2. 页面章节（查询条件/列表字段/交互逻辑/导出字段） 3. 状态流转（枚举、筛选项、流转表、权限表四处一致） 4. 权限矩阵 5. 数据源/接口（入参、取值、异常降级、生效范围） 6. 术语与枚举

### Step 5 修订记录
在修订记录表**顶部**插入新版本，五要素：版本号、日期、作者、逐条对应 R#、是否涉及原型。纯文案/配置不升版本号，但保留轻量记录。历史记录不篡改，更名关系写在当次记录里。

### Step 6 校验（必跑）
有脚本时：
```bash
python3 scripts/check_inline_js.py <file.html>
python3 scripts/check_html_nesting.py <file.html>
python3 scripts/check_tables_and_terms.py <file.html> --forbid "旧术语" --require "新术语"
```
**降级校验**（无脚本环境）：
1. 浏览器打开，控制台无报错；逐个点击新增按钮/弹窗。
2. 抽查每个新增/修改表格的表头列数与行单元格数。
3. 全局检索旧术语，残留为 0；新术语在筛选、列表、详情、导出、正文五处齐全。
任一项失败：先修再交付，不带已知错误交付。

### Step 7 验收与交付
按第 8 节自检；浏览器能交互就点主路径，不能（如 DOM 过大）就输出**手动验收步骤**，不把 BLOCKED 当通过。交付给出：`computer://` 链接、按 R# 的变更摘要、开放问题清单。

## 4. 三分法分流

| 类型 | 判定 | 原型 | 正文 | 修订记录 |
|---|---|---|---|---|
| A 页面型 | 界面、字段、交互或状态变化 | 必改 | 六面必查 | 升版本号 |
| B 仅后端逻辑型 | 送检/判定/接口/免检规则变化 | 跳过 | 写清入参、取值、缺失降级、生效范围 | 升版本号 |
| C 纯文案配置型 | 措辞、示例、默认值，无逻辑变化 | 视情况 | 局部修订 | 轻量记录，不升版本号 |

B 类不要硬塞原型占位；C 类不要为改一句话新开一节需求。

## 5. 单文件双模式治理

- **必留锚点**：每个页面/弹窗/关键函数有稳定 id 或函数名。
- **按区改动**：禁止整文件重写；单次跨 10 个以上区块先拆多轮。
- **拆分红线**：文件 > 2 万行，或 DOM > 1.5 万节点，或浏览器自动化连续两次无法交互 → 主动提议拆分并说明成本。
- **外部依赖**：引用了本地不存在的资源（如图表库）要确认降级表现，没有就如实告知。

## 6. 术语与枚举

**先定名再改**，维护一张术语表：术语 / 定义 / 禁用别名 / 首次出现位置。
每个枚举必须在五处齐全：筛选、列表、详情、导出、正文。

扫描示例：
```bash
grep -n "人工视频面签" <file.html>   # 除"更名"说明行外应为 0
```

高频坑：
- 名称词序不一致（A+B / B+A）只改了一处。
- 新增状态只改徽标，漏筛选项、导出字段、流转表、权限表。
- 枚举扩了但示例数据没扩，评审看不到新状态。
- 术语改了但接口字段仍是旧名，研发对不上。

## 7. 修订记录模板

| 日期 | 变更内容 | 版本号 | 作者 | 是否涉及原型 |
|---|---|---|---|---|
| 2026-11-16 | 见下 | V2.23 | 王超 | 是 |

变更内容用有序列表，一条对应一个 R#，动词开头，写结果不写过程：

1. 质检工作台：时间维度新增"自定义"，跨度含首尾不得超过 1 个月，超出即拦截；KPI、列表、导出随区间生效。
2. 通话/视频/微信/短信列表：已复检任务新增"复议"，支持修改结果、分类、说明与案例标记，提交后覆盖并留痕。
3. AI 质检接口：兴业视频人工播报送检新增"资方"传参，按资方差异化判定（仅后端逻辑，不涉及原型）。

规则：不合并条目、不写"优化若干问题"、纯后端条目注明、日期用实际交付日。

## 8. 评审自检清单

**结构**：能打开 / 控制台无错 / 标签闭合 / 弹窗可开可关 / 按钮函数存在 / 表格列数一致
**交互**：新筛选项生效 / 新状态在列表与导出可见 / 必填有提示 / 弹窗重开状态已重置 / 越界与空数据有文案
**一致**：功能清单已更新 / 页面章节与原型一致 / 状态流转与代码一致 / 权限矩阵覆盖新按钮 / 接口四要素齐全 / 导出字段一致
**术语**：旧名残留 0 / 新枚举五处齐全 / 示例数据含新状态
**修订**：版本在顶部 / 日期作者齐全 / 对应 R# / 标明是否涉及原型
**范围**：B 类没被扩成页面 / 没顺手重构无关代码 / 没为单场景引入抽象
**交付**：链接与 R# 摘要齐全 / 开放问题单列 / 浏览器不可用时给出手动步骤

## 9. 片段速查

**列表行（详情 + 复议）**
```html
<tr>
  <td><input type="checkbox" class="batch-check" value="{任务编号}"></td>
  <td>{任务编号}</td><td>{来源}</td><td>{中台人员}</td><td>{质检人员}</td>
  <td>{质检日期}</td>
  <td><span class="badge badge-success">合格</span></td>
  <td><span class="badge badge-info">已复检</span></td>
  <td>
    <button class="table-action" type="button" onclick="openTaskDetailFromRow(this)">详情</button>
    <button class="table-action" type="button" onclick="openReReviewFromRow(this)">复议</button>
  </td>
</tr>
```

**弹窗骨架**
```html
<div class="modal-overlay" id="modal{Xxx}">
  <div class="modal-box" style="max-width:560px;">
    <div class="modal-header">
      <h3>{标题}</h3>
      <button class="modal-close" type="button" onclick="closeModal('modal{Xxx}')">×</button>
    </div>
    <div class="modal-body">{表单}</div>
    <div class="modal-footer">
      <button class="filter-btn secondary" type="button" onclick="closeModal('modal{Xxx}')">取消</button>
      <button class="filter-btn primary" type="button" onclick="submit{Xxx}()">提交</button>
    </div>
  </div>
</div>
```

**表单字段**
```html
<div class="form-group">
  <label class="form-label">{字段} <span class="required">*</span></label>
  <input class="form-input" type="text" id="{id}" placeholder="{提示}">
</div>
```

**日期区间跨度校验**
```js
function applyRange() {
  var s = document.getElementById('rangeStart').value;
  var e = document.getElementById('rangeEnd').value;
  var tip = document.getElementById('rangeTip');
  if (!s || !e) { tip.style.color = '#ef4444'; tip.textContent = '请选择开始和结束日期'; return; }
  var sd = new Date(s), ed = new Date(e);
  if (sd > ed) { tip.style.color = '#ef4444'; tip.textContent = '开始日期不能晚于结束日期'; return; }
  var days = Math.round((ed - sd) / 86400000) + 1;
  if (days > 31) { tip.style.color = '#ef4444'; tip.textContent = '跨度不能超过1个月（含起止日最多31天）'; return; }
  tip.style.color = '#10b981';
  tip.textContent = '已按 ' + s + ' 至 ' + e + ' 查询（共 ' + days + ' 天）';
}
```

## 10. 常见坑

- 加按钮没加函数 → 点击报错；加弹窗没写重置 → 上次勾选残留。
- 新增状态只改徽标，漏筛选/导出/流转/权限。
- 同一数据源两种叫法，未统一就开改。
- 改表格行误删容器闭合标签。
- 只改原型不改正文，或反之。
- 把仅后端逻辑需求做成前端页面，范围失控。
- 为单个场景引入抽象或配置项。
- 带着已知校验错误交付，并声称"已通过"。
