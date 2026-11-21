"""成语接龙练习纸页面渲染。"""

from __future__ import annotations

import html
from typing import List, Sequence

from .model import WorksheetItem

STYLE = """
@page { size: A4 portrait; margin: 14mm 13mm; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  color: #1f2937;
  font-size: 11.5pt;
  line-height: 1.7;
}
h1 { font-size: 21pt; margin: 0 0 1.5mm; letter-spacing: 1pt; }
.sub { color: #6b7280; font-size: 9.5pt; margin: 0 0 6mm; }
.rule { color: #475569; font-size: 10pt; margin: 0 0 5mm; padding: 2.5mm 3mm;
  border-left: 2.5pt solid #b45309; background: #fffbeb; }
ol.items { margin: 0; padding-left: 7mm; }
li.item { margin-bottom: 6mm; page-break-inside: avoid; }
.head { font-size: 12.5pt; font-weight: 600; }
.meaning { color: #6b7280; font-size: 9.5pt; margin-left: 2mm; font-weight: 400; }
.chain { margin-top: 1.5mm; letter-spacing: 0.5pt; }
.arrow { color: #9ca3af; margin: 0 1.5mm; }
.slot { display: inline-block; min-width: 21mm; border-bottom: 0.7pt solid #94a3b8; height: 1.25em; }
.answers { page-break-before: always; }
.answers h2 { font-size: 15pt; margin: 0 0 4mm; }
.answers ol { margin: 0; padding-left: 7mm; }
.answers li { margin-bottom: 3.2mm; }
.answers .tag { color: #b45309; font-weight: 600; margin-right: 1.5mm; }
.answers .ans { color: #0f4c81; }
.hint { color: #6b7280; font-size: 9.5pt; margin-top: 6mm; }
"""


def _escape(text: str) -> str:
    return html.escape(str(text), quote=True)


def _slots(length: int) -> str:
    parts: List[str] = []
    for _ in range(length - 1):
        parts.append('<span class="slot"></span>')
    return '<span class="arrow">→</span>'.join(parts)


def render_worksheet(
    items: Sequence[WorksheetItem],
    title: str = "成语接龙练习",
    include_answers: bool = False,
    show_meaning: bool = True,
) -> str:
    """生成 A4 接龙练习纸，可选附答案。"""
    if not items:
        raise ValueError("至少需要一道题目")
    rows: List[str] = []
    for index, item in enumerate(items, start=1):
        meaning = (
            '<span class="meaning">%s</span>' % _escape(item.meaning) if show_meaning else ""
        )
        rows.append(
            '<li class="item"><div class="head">%d. %s%s</div>'
            '<div class="chain">%s<span class="arrow">→</span>%s</div></li>'
            % (index, _escape(item.start), meaning, _escape(item.start), _slots(item.length))
        )
    body = [
        "<!DOCTYPE html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>%s</title>" % _escape(title),
        "<style>%s</style>" % STYLE,
        "</head>",
        "<body>",
        "<h1>%s</h1>" % _escape(title),
        '<p class="sub">姓名：__________　班级：__________　日期：__________</p>',
        '<p class="rule">规则：从给出的成语开始，每个成语的首字要与上一个成语的尾字相同，'
        "同一题中不要重复使用成语。</p>",
        '<ol class="items">',
        "\n".join(rows),
        "</ol>",
        '<p class="hint">提示：先想清楚尾字，再从常用成语入手，必要时可以换一条路线。</p>',
    ]
    if include_answers:
        body.extend(_answer_section(items))
    body.extend(["</body>", "</html>"])
    return "\n".join(body)


def _answer_section(items: Sequence[WorksheetItem]) -> List[str]:
    rows: List[str] = []
    for index, item in enumerate(items, start=1):
        chain = item.answer
        text = " → ".join(chain)
        rows.append(
            '<li><span class="tag">%d.</span><span class="ans">%s</span></li>'
            % (index, _escape(text))
        )
    return [
        '<section class="answers">',
        "<h2>参考答案</h2>",
        "<ol>",
        "\n".join(rows),
        "</ol>",
        '<p class="hint">接龙答案不唯一，只要首尾相接、不重复即可。</p>',
        "</section>",
    ]
