# 可复用高保真片段

> 与需求文档同款的视觉基线：主色 `#2563eb`，圆角 10px，字号 13/14px。占位符用 `{...}`，复制后按需替换。

## 1. 列表行（详情 + 复检/复议 + 转单）

```html
<tr>
  <td><input type="checkbox" class="batch-check" value="{任务编号}"></td>
  <td>{任务编号}</td>
  <td>{来源/类型}</td>
  <td>{中台人员}</td>
  <td>{质检人员}</td>
  <td>{质检日期}</td>
  <td><span class="badge badge-success">合格</span></td>
  <td><span class="badge badge-success">已复检</span></td>
  <td>
    <button class="table-action" type="button" onclick="openTaskDetailFromRow(this)">详情</button>
    <button class="table-action" type="button" onclick="openReReviewFromRow(this)">复议</button>
  </td>
</tr>
```

状态徽标：`badge-success` 合格/已完成，`badge-warning` 待复检，`badge-info` 已复检，`badge-muted` 待质检。

## 2. 弹窗骨架

```html
<div class="modal-overlay" id="modal{Xxx}">
  <div class="modal-box" style="max-width:560px;">
    <div class="modal-header">
      <h3>{标题}</h3>
      <button class="modal-close" type="button" onclick="closeModal('modal{Xxx}')">×</button>
    </div>
    <div class="modal-body">
      <!-- 说明 callout（可选） -->
      <div class="callout" style="margin-bottom:16px;padding:10px 14px;border-left:3px solid var(--warning-color);background:var(--bg-secondary);border-radius:4px;font-size:13px;color:var(--text-secondary);">
        {一句话说明这个弹窗解决什么问题}
      </div>
      {表单内容}
    </div>
    <div class="modal-footer">
      <button class="filter-btn secondary" type="button" onclick="closeModal('modal{Xxx}')">取消</button>
      <button class="filter-btn primary" type="button" onclick="submit{Xxx}()">提交</button>
    </div>
  </div>
</div>
```

配套 JS：`openModal` / `closeModal` 已存在；新增 `open{Xxx}FromRow(btn)` + `submit{Xxx}()`，并在打开时**重置表单状态**。

## 3. 表单控件

```html
<div class="form-group">
  <label class="form-label">{字段名} <span class="required">*</span></label>
  <input class="form-input" type="text" id="{fieldId}" placeholder="{提示}">
</div>

<div class="form-group">
  <label class="form-label">{单选名} <span class="required">*</span></label>
  <div class="form-radio-group">
    <label class="form-radio"><input type="radio" name="{group}" value="pass" checked> 合格</label>
    <label class="form-radio"><input type="radio" name="{group}" value="fail"> 不合格</label>
  </div>
</div>

<div class="form-group">
  <label class="form-label">{多选名}</label>
  <div class="form-radio-group" style="flex-direction:column;gap:6px;">
    <label class="form-radio"><input type="checkbox" class="{klass}" name="{group}" value="{值}"> {选项}</label>
  </div>
  <div id="{noteId}" style="display:none;font-size:12px;color:var(--text-muted);margin-top:6px;">{联动提示}</div>
</div>

<div class="form-group">
  <label class="form-label">{长文本} <span class="required">*</span></label>
  <textarea class="form-textarea" id="{fieldId}" placeholder="{提示}">{默认值}</textarea>
</div>
```

## 4. 从行取数并打开弹窗

```js
function open{Xxx}FromRow(btn) {
  var tr = btn.closest('tr');
  if (!tr) return;
  var check = tr.querySelector('.batch-check');
  var id = check ? check.value : (tr.cells[1] ? tr.cells[1].textContent.trim() : '');
  document.getElementById('{idField}').value = id;
  document.getElementById('{metaField}').value = '当前用户 / ' + formatNowTime();
  openModal('modal{Xxx}');
}
```

## 5. 日期区间（跨度校验）

```html
<div id="dateRange" style="display:none;margin-top:8px;">
  <input type="date" class="filter-input" id="rangeStart">
  <span>至</span>
  <input type="date" class="filter-input" id="rangeEnd">
  <button class="filter-btn primary" type="button" onclick="applyRange()">查询</button>
  <span id="rangeTip" style="font-size:12px;"></span>
</div>
```

```js
function applyRange() {
  var s = document.getElementById('rangeStart').value;
  var e = document.getElementById('rangeEnd').value;
  var tip = document.getElementById('rangeTip');
  if (!s || !e) { tip.style.color = '#ef4444'; tip.textContent = '请选择开始和结束日期'; return; }
  var sd = new Date(s), ed = new Date(e);
  if (sd > ed) { tip.style.color = '#ef4444'; tip.textContent = '开始日期不能晚于结束日期'; return; }
  var days = Math.round((ed - sd) / 86400000) + 1;
  if (days > 31) { tip.style.color = '#ef4444'; tip.textContent = '日期跨度不能超过1个月（含起止日最多31天）'; return; }
  tip.style.color = '#10b981';
  tip.textContent = '已按 ' + s + ' 至 ' + e + ' 查询（共 ' + days + ' 天）';
  // 按 days 分桶渲染，并用真实日期覆盖展示标签
}
```

## 6. 提交反馈

```js
function submit{Xxx}() {
  if (!validate()) return;
  closeModal('modal{Xxx}');
  showPanelToast('{动作}已提交：{关键字段}已更新');
}
```

校验失败用 toast 或行内红字提示，不要 `alert`（导出/删除这类不可逆操作除外）。
