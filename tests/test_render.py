"""页面渲染测试。"""

import unittest

from idiomchain.model import WorksheetItem, is_chain, normalize_chain
from idiomchain.render import render_worksheet


class RenderTest(unittest.TestCase):
    def setUp(self):
        self.items = [
            WorksheetItem("一心一意", 4),
            WorksheetItem("水到渠成", 3),
        ]

    def test_doctype(self):
        page = render_worksheet(self.items)
        self.assertTrue(page.startswith("<!DOCTYPE html>"))

    def test_language(self):
        page = render_worksheet(self.items)
        self.assertIn('lang="zh-CN"', page)

    def test_item_count(self):
        page = render_worksheet(self.items)
        self.assertEqual(page.count('class="item"'), 2)

    def test_starts_present(self):
        page = render_worksheet(self.items)
        self.assertIn("一心一意", page)
        self.assertIn("水到渠成", page)

    def test_slots_count(self):
        page = render_worksheet(self.items)
        self.assertEqual(page.count('class="slot"'), 3 + 2)

    def test_meaning_shown(self):
        page = render_worksheet(self.items)
        self.assertIn("心思专一", page)

    def test_meaning_hidden(self):
        page = render_worksheet(self.items, show_meaning=False)
        self.assertNotIn("心思专一", page)

    def test_no_answers_by_default(self):
        page = render_worksheet(self.items)
        self.assertNotIn("参考答案", page)

    def test_answers_included(self):
        page = render_worksheet(self.items, include_answers=True)
        self.assertIn("参考答案", page)
        self.assertIn('class="answers"', page)

    def test_answer_chain_valid(self):
        page = render_worksheet(self.items, include_answers=True)
        section = page.split('class="answers"', 1)[1]
        for line in section.split('<span class="ans">')[1:]:
            text = line.split("</span>", 1)[0]
            words = normalize_chain(text)
            self.assertTrue(is_chain(words, require_known=True), words)

    def test_title_escaped(self):
        page = render_worksheet(self.items, title="<成语> & 接龙")
        self.assertIn("&lt;成语&gt; &amp; 接龙", page)
        self.assertNotIn("<成语>", page)

    def test_empty_items(self):
        with self.assertRaises(ValueError):
            render_worksheet([])

    def test_custom_title(self):
        page = render_worksheet(self.items, title="周末练习")
        self.assertIn("周末练习", page)

    def test_rule_text(self):
        page = render_worksheet(self.items)
        self.assertIn("首字要与上一个成语的尾字相同", page)


if __name__ == "__main__":
    unittest.main()
