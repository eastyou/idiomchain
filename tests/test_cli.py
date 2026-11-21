"""命令行测试。"""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from idiomchain.cli import main


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class ChainCommandTest(unittest.TestCase):
    def test_default(self):
        code, out, _ = run_cli(["chain", "一心一意"])
        self.assertEqual(code, 0)
        self.assertIn(" → ", out)
        self.assertIn("共 4 个成语", out)

    def test_custom_length(self):
        code, out, _ = run_cli(["chain", "一心一意", "--length", "3"])
        self.assertEqual(code, 0)
        self.assertIn("共 3 个成语", out)

    def test_seed_reproducible(self):
        _, first, _ = run_cli(["chain", "水到渠成", "--seed", "7"])
        _, second, _ = run_cli(["chain", "水到渠成", "--seed", "7"])
        self.assertEqual(first, second)

    def test_unknown_idiom(self):
        code, _, err = run_cli(["chain", "意气用事"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_invalid_length(self):
        code, _, err = run_cli(["chain", "一心一意", "--length", "1"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_unsolvable(self):
        code, _, err = run_cli(["chain", "一望无际", "--length", "3"])
        self.assertEqual(code, 2)
        self.assertIn("无法从", err)


class InfoCommandTest(unittest.TestCase):
    def test_meaning(self):
        code, out, _ = run_cli(["info", "一心一意"])
        self.assertEqual(code, 0)
        self.assertIn("心思专一", out)

    def test_next_words(self):
        code, out, _ = run_cli(["info", "一心一意"])
        self.assertEqual(code, 0)
        self.assertIn("意气风发", out)

    def test_previous_words(self):
        code, out, _ = run_cli(["info", "一心一意"])
        self.assertEqual(code, 0)
        self.assertIn("可被接", out)

    def test_unknown(self):
        code, _, err = run_cli(["info", "意气用事"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)


class FindCommandTest(unittest.TestCase):
    def test_lists_words(self):
        code, out, _ = run_cli(["find", "一"])
        self.assertEqual(code, 0)
        self.assertIn("以「一」开头", out)
        self.assertIn("一心一意", out)

    def test_limit(self):
        code, out, _ = run_cli(["find", "一", "--limit", "2"])
        self.assertEqual(code, 0)
        self.assertIn("未显示", out)

    def test_no_words(self):
        code, out, _ = run_cli(["find", "囧"])
        self.assertEqual(code, 0)
        self.assertIn("0 个", out)

    def test_invalid_char(self):
        code, _, err = run_cli(["find", "一二"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_invalid_limit(self):
        code, _, err = run_cli(["find", "一", "--limit", "0"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)


class SheetCommandTest(unittest.TestCase):
    def test_stdout(self):
        code, out, _ = run_cli(["sheet", "--count", "2", "--seed", "1"])
        self.assertEqual(code, 0)
        self.assertIn("<!DOCTYPE html>", out)

    def test_item_count(self):
        code, out, _ = run_cli(["sheet", "--count", "5", "--length", "4", "--seed", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(out.count('class="item"'), 5)

    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as folder:
            target = os.path.join(folder, "sheet.html")
            code, out, _ = run_cli(["sheet", "--count", "3", "--seed", "3", "-o", target])
            self.assertEqual(code, 0)
            self.assertIn("已写入", out)
            with open(target, encoding="utf-8") as handle:
                page = handle.read()
            self.assertIn("成语接龙", page)

    def test_nested_output(self):
        with tempfile.TemporaryDirectory() as folder:
            target = os.path.join(folder, "a", "b", "sheet.html")
            code, _, _ = run_cli(["sheet", "--count", "1", "-o", target])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(target))

    def test_answers(self):
        code, out, _ = run_cli(["sheet", "--count", "2", "--seed", "4", "--answers"])
        self.assertEqual(code, 0)
        self.assertIn("参考答案", out)

    def test_custom_title(self):
        code, out, _ = run_cli(["sheet", "--count", "1", "--title", "成语小测"])
        self.assertEqual(code, 0)
        self.assertIn("成语小测", out)

    def test_no_meaning(self):
        code, out, _ = run_cli(["sheet", "--count", "1", "--seed", "5", "--no-meaning"])
        self.assertEqual(code, 0)
        self.assertNotIn('class="meaning"', out)

    def test_invalid_count(self):
        code, _, err = run_cli(["sheet", "--count", "0"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_invalid_length(self):
        code, _, err = run_cli(["sheet", "--length", "1"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_reproducible(self):
        _, first, _ = run_cli(["sheet", "--count", "3", "--seed", "9"])
        _, second, _ = run_cli(["sheet", "--count", "3", "--seed", "9"])
        self.assertEqual(first, second)


class HelpTest(unittest.TestCase):
    def test_help_exits_zero(self):
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
