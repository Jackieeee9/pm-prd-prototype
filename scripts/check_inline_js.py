#!/usr/bin/env python3
"""提取 HTML 中的内联 <script> 并用 node --check 校验语法。

用法:
    python3 check_inline_js.py <file.html>

退出码: 0 全部通过; 1 存在语法错误; 2 用法错误或环境缺失。
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 check_inline_js.py <file.html>")
        return 2

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"[FAIL] 文件不存在: {path}")
        return 2
    if not shutil.which("node"):
        print("[FAIL] 未找到 node，无法校验内联脚本")
        return 2

    html = open(path, encoding="utf-8").read()
    # 跳过带 src 的外链脚本
    blocks = re.findall(
        r"<script(?![^>]*\bsrc\s*=)[^>]*>(.*?)</script>", html, re.S | re.I
    )
    if not blocks:
        print("[OK] 未发现内联脚本")
        return 0

    tmpdir = tempfile.mkdtemp(prefix="inline_js_")
    failures = 0
    checked = 0

    for idx, code in enumerate(blocks, 1):
        if not code.strip():
            continue
        checked += 1
        tmp = os.path.join(tmpdir, f"block_{idx}.js")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(code)
        proc = subprocess.run(
            ["node", "--check", tmp], capture_output=True, text=True
        )
        if proc.returncode != 0:
            failures += 1
            print(f"[FAIL] 第 {idx} 个内联脚本语法错误")
            err = (proc.stderr or "").strip().splitlines()
            for line in err[:8]:
                print("       " + line)
        else:
            print(f"[OK]   第 {idx} 个内联脚本")

    print(f"\n共校验 {checked} 个内联脚本，失败 {failures} 个")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
