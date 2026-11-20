#!/usr/bin/env python3
"""检查 HTML 标签嵌套是否闭合正确。

用法:
    python3 check_html_nesting.py <file.html>

说明:
    - 忽略 void 元素（br、img、input 等）与自闭合写法
    - 对允许省略闭合的标签（p、li、tr、td 等）做宽松处理
    - 退出码: 0 通过; 1 存在嵌套错误或未闭合标签; 2 用法错误
"""
import sys
from html.parser import HTMLParser

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
OPTIONAL_CLOSE = {
    "p", "li", "tr", "td", "th", "option", "thead", "tbody", "tfoot",
    "dt", "dd", "colgroup",
}


class NestingChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        if tag in OPTIONAL_CLOSE and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(("多余闭合", tag, self.getpos(), None))
            return
        if self.stack[-1][0] != tag:
            self.errors.append(
                ("标签不匹配", tag, self.getpos(), self.stack[-1])
            )
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            return
        self.stack.pop()


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 check_html_nesting.py <file.html>")
        return 2

    path = sys.argv[1]
    checker = NestingChecker()
    try:
        checker.feed(open(path, encoding="utf-8").read())
    except FileNotFoundError:
        print(f"[FAIL] 文件不存在: {path}")
        return 2

    if checker.errors:
        print(f"[FAIL] 发现 {len(checker.errors)} 处嵌套问题:")
        for kind, tag, pos, extra in checker.errors[:15]:
            if extra:
                print(
                    f"       第 {pos[0]} 行 <{tag}> {kind}，"
                    f"期望闭合 <{extra[0]}>（开于第 {extra[1][0]} 行）"
                )
            else:
                print(f"       第 {pos[0]} 行 <{tag}> {kind}")
        if len(checker.errors) > 15:
            print(f"       ……其余 {len(checker.errors) - 15} 处省略")

    if checker.stack:
        print(f"[FAIL] 有 {len(checker.stack)} 个标签未闭合:")
        for tag, pos in checker.stack[:15]:
            print(f"       第 {pos[0]} 行 <{tag}>")
        return 1

    if checker.errors:
        return 1

    print("[OK] HTML 标签嵌套正确")
    return 0


if __name__ == "__main__":
    sys.exit(main())
