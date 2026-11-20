# pm-prd-prototype

个人产品经理的 **PRD 与高保真原型一体化交付** skill：把一个批次的需求变更，落成一份可评审的单文件 HTML（左侧原型、右侧需求正文），并保证两者始终同步。

## 解决什么问题

- 需求散落在聊天记录里，缺少拆条、编号和验收口径
- 原型改了，需求正文没改；正文改了，原型对不上
- 同一概念多种叫法、枚举漏改（新增状态只改徽标，漏筛选项/导出/流转表）
- 交付前没有可执行的校验，靠肉眼把关

## 工作流

拆条编号 → 澄清歧义 → **影响面清单（唯一门禁）** → 原型改动 → 正文六面同步 → 修订记录 → 脚本校验 → 验收交付

需求按变更类型分流：**A 页面型**（全流程）、**B 仅后端逻辑型**（跳过原型，只补正文与接口说明）、**C 纯文案配置型**（轻量记录，不升版本号）。

## 目录结构

```
SKILL.md      流程、门禁、三分法、单文件治理与常见坑
references/   影响面清单、术语与枚举、评审自检、修订记录模板
scripts/      内联 JS 语法、HTML 标签嵌套、表格行列与术语残留校验
assets/       可复用高保真片段（列表行、弹窗、表单、日期区间）
dist/         单文件兼容版，给只支持单条规则的工具
```

## 安装

克隆到所用工具的 skills 目录：

```bash
git clone <repo-url> ~/.trae-cn/skills/pm-prd-prototype
```

- Claude Code：`~/.claude/skills/` 或项目内 `.claude/skills/`
- Trae：`~/.trae-cn/skills/`
- Cursor / Windsurf / Copilot：使用 `dist/pm-prd-prototype.single.md`，按文件第 0 节改写 frontmatter 后放入对应 rules 目录

## 校验脚本

```bash
python3 scripts/check_inline_js.py <file.html>
python3 scripts/check_html_nesting.py <file.html>
python3 scripts/check_tables_and_terms.py <file.html> --forbid "旧术语" --require "新术语"
```

需要 `python3`；第一个脚本另需 `node`。无执行环境时，按 `references/review-checklist.md` 人工核对。

## 触发方式

出现 PRD、需求迭代、小版本、原型同步、修订记录等场景时使用，或直接说「按 pm-prd-prototype 更新这版需求」。
