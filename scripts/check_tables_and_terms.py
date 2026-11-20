#!/usr/bin/env python3
"""检查表格行列一致性与术语残留。

用法:
    python3 check_tables_and_terms.py <file.html> \
        [--forbid "旧术语"] [--require "新术语"] [--strict]

规则:
    - --forbid: 该词出现即失败；含"更名"字样的行视为更名说明，跳过
    - --require: 该词必须至少出现一次，否则失败
    - 表格: 以表头列数为基准检查每行单元格数（含 colspan 计算）；
      含 rowspan 的表格只告警，不计失败；--strict 时告警也失败

退出码: 0 通过; 1 存在失败项; 2 用法错误
"""
import argparse
import sys
from html.parser import HTMLParser


class TableCounter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "table":
            t = {
                "line": self.getpos()[0],
                "header": None,
                "rows": [],
                "has_rowspan": False,
            }
            self.tables.append(t)
            self.stack.append(t)
        elif tag == "tr" and self.stack:
            self.stack[-1]["_row"] = {
                "cells": 0,
                "line": self.getpos()[0],
                "has_th": False,
            }
        elif tag in ("td", "th") and self.stack:
            row = self.stack[-1].get("_row")
            if row is None:
                return
            try:
                colspan = int(attr.get("colspan", 1) or 1)
            except ValueError:
                colspan = 1
            row["cells"] += colspan
            if tag == "th":
                row["has_th"] = True
            try:
                if int(attr.get("rowspan", 1) or 1) > 1:
                    self.stack[-1]["has_rowspan"] = True
            except ValueError:
                pass

    def handle_endtag(self, tag):
        if tag == "tr" and self.stack:
            row = self.stack[-1].pop("_row", None)
            if row is None:
                return
            t = self.stack[-1]
            if t["header"] is None:
                t["header"] = row["cells"]
            else:
                t["rows"].append(row)
        elif tag == "table" and self.stack:
            self.stack.pop()


def check_terms(html: str, forbid, require):
    lines = html.splitlines()
    failures = 0

    for term in forbid:
        hits = []
        for i, line in enumerate(lines, 1):
            if term in line and "更名" not in line:
                hits.append(i)
        if hits:
            failures += 1
            preview = ", ".join(str(x) for x in hits[:10])
            print(f"[FAIL] 禁用术语仍残留 {len(hits)} 处: “{term}” 行 {preview}")
        else:
            print(f"[OK]   禁用术语残留为 0: “{term}”")

    for term in require:
        count = html.count(term)
        if count == 0:
            failures += 1
            print(f"[FAIL] 必需术语缺失: “{term}”")
        else:
            print(f"[OK]   必需术语存在: “{term}”（{count} 处）")

    return failures


def check_tables(parser: TableCounter, strict: bool):
    warn = 0
    fail = 0
    for idx, t in enumerate(parser.tables, 1):
        header = t["header"]
        if not header:
            warn += 1
            print(f"[WARN] 第 {idx} 个表格（第 {t['line']} 行）未识别到表头")
            continue
        bad = [r for r in t["rows"] if r["cells"] != header]
        if not bad:
            print(f"[OK]   第 {idx} 个表格 {header} 列，{len(t['rows'])} 行一致")
            continue
        if t["has_rowspan"]:
            warn += 1
            print(
                f"[WARN] 第 {idx} 个表格（第 {t['line']} 行）存在 rowspan，"
                f"列数差异可能正常：表头 {header} 列，"
                f"异常行 {[r['line'] for r in bad[:5]]}"
            )
        else:
            fail += 1
            print(
                f"[FAIL] 第 {idx} 个表格（第 {t['line']} 行）列数不一致："
                f"表头 {header} 列，异常行 "
                f"{[(r['line'], r['cells']) for r in bad[:5]]}"
            )

    if warn and strict:
        return fail + warn
    return fail


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--forbid", action="append", default=[])
    ap.add_argument("--require", action="append", default=[])
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    try:
        html = open(args.file, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"[FAIL] 文件不存在: {args.file}")
        return 2

    term_fail = check_terms(html, args.forbid, args.require)

    parser = TableCounter()
    parser.feed(html)
    table_fail = check_tables(parser, args.strict)

    total = term_fail + table_fail
    print(
        f"\n共 {len(parser.tables)} 个表格；术语失败 {term_fail} 项，"
        f"表格失败 {table_fail} 项"
    )
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
