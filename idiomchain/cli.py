"""命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .model import (
    DEFAULT_LENGTH,
    IDIOMS,
    IdiomError,
    build_chain,
    build_worksheet,
    check_idiom,
    idioms_starting,
    next_idioms,
    previous_idioms,
)
from .render import render_worksheet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="idiomchain",
        description="成语接龙：查询词库、生成接龙与可打印练习纸",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    chain_parser = subparsers.add_parser("chain", help="从指定成语生成一条接龙")
    chain_parser.add_argument("start", help="起始成语，例如 一心一意")
    chain_parser.add_argument(
        "--length", type=int, default=DEFAULT_LENGTH, help="接龙成语数量，默认 4"
    )
    chain_parser.add_argument("--seed", type=int, default=None, help="随机种子")

    info_parser = subparsers.add_parser("info", help="查看成语释义与可接成语")
    info_parser.add_argument("idiom", help="四字成语")

    find_parser = subparsers.add_parser("find", help="按首字查找成语")
    find_parser.add_argument("char", help="单个汉字")
    find_parser.add_argument("--limit", type=int, default=20, help="最多显示数量，默认 20")

    sheet_parser = subparsers.add_parser("sheet", help="生成练习纸 HTML")
    sheet_parser.add_argument("--count", type=int, default=12, help="题目数量，默认 12")
    sheet_parser.add_argument(
        "--length", type=int, default=DEFAULT_LENGTH, help="每题的接龙数量，默认 4"
    )
    sheet_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    sheet_parser.add_argument("--title", default="成语接龙练习", help="练习纸标题")
    sheet_parser.add_argument("--answers", action="store_true", help="追加参考答案")
    sheet_parser.add_argument("--no-meaning", action="store_true", help="不显示起始成语释义")
    sheet_parser.add_argument("-o", "--output", default=None, help="输出文件")
    return parser


def _write_output(html_text: str, output: Optional[str]) -> None:
    if not output:
        print(html_text)
        return
    path = Path(output)
    if path.parent and str(path.parent) not in ("", "."):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    print("已写入 %s" % path)


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "chain":
            chain = build_chain(args.start, args.length, args.seed)
            print(" → ".join(chain))
            print("共 %d 个成语" % len(chain))
            return 0
        if args.command == "info":
            check_idiom(args.idiom)
            print("%s：%s" % (args.idiom, IDIOMS[args.idiom]))
            print("可接：%s" % ("、".join(next_idioms(args.idiom)) or "（无）"))
            print("可被接：%s" % ("、".join(previous_idioms(args.idiom)) or "（无）"))
            return 0
        if args.command == "find":
            if args.limit < 1:
                raise IdiomError("显示数量必须是正整数")
            words = idioms_starting(args.char)
            print("以「%s」开头的成语：%d 个" % (args.char, len(words)))
            for word in words[: args.limit]:
                print("%s  %s" % (word, IDIOMS[word]))
            if len(words) > args.limit:
                print("……还有 %d 个未显示" % (len(words) - args.limit))
            return 0
        items = build_worksheet(args.count, args.length, args.seed)
        _write_output(
            render_worksheet(items, args.title, args.answers, not args.no_meaning),
            args.output,
        )
        return 0
    except IdiomError as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2
    except OSError as exc:
        print("写入失败：%s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
