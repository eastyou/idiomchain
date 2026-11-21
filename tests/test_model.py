"""词库、接龙与出题逻辑测试。"""

import unittest
from dataclasses import FrozenInstanceError

from idiomchain.model import (
    DEFAULT_LENGTH,
    IDIOMS,
    MAX_LENGTH,
    MIN_LENGTH,
    IdiomError,
    WorksheetItem,
    build_chain,
    build_worksheet,
    chain_stats,
    check_answer,
    check_idiom,
    check_length,
    find_chains,
    idioms_ending,
    idioms_starting,
    is_chain,
    is_idiom,
    is_idiom_word,
    next_idioms,
    normalize_chain,
    previous_idioms,
    solvable_starts,
)


class DictionaryTest(unittest.TestCase):
    def test_not_empty(self):
        self.assertGreater(len(IDIOMS), 200)

    def test_all_four_chinese_chars(self):
        for word in IDIOMS:
            self.assertEqual(len(word), 4)
            self.assertTrue(all("\u4e00" <= char <= "\u9fff" for char in word))

    def test_meanings_filled(self):
        for word, meaning in IDIOMS.items():
            self.assertTrue(meaning.strip(), word)

    def test_no_duplicate_keys(self):
        self.assertEqual(len(IDIOMS), len(set(IDIOMS)))

    def test_first_index_matches(self):
        for word in IDIOMS:
            self.assertIn(word, idioms_starting(word[0]))

    def test_last_index_matches(self):
        for word in IDIOMS:
            self.assertIn(word, idioms_ending(word[-1]))

    def test_starting_sorted(self):
        words = idioms_starting("一")
        self.assertEqual(words, sorted(words))

    def test_starting_invalid(self):
        for bad in ("", "一一", 1, None):
            with self.assertRaises(IdiomError):
                idioms_starting(bad)

    def test_ending_unknown_char(self):
        self.assertEqual(idioms_ending("囧"), [])


class LookupTest(unittest.TestCase):
    def test_is_idiom(self):
        self.assertTrue(is_idiom("一心一意"))
        self.assertFalse(is_idiom("意气用事"))
        self.assertFalse(is_idiom("一二三"))

    def test_is_idiom_word(self):
        self.assertTrue(is_idiom_word("意气用事"))
        self.assertFalse(is_idiom_word("apple"))
        self.assertFalse(is_idiom_word("一二三"))
        self.assertFalse(is_idiom_word(123))

    def test_next_idioms_link(self):
        for word in next_idioms("一心一意"):
            self.assertEqual(word[0], "意")

    def test_next_idioms_unknown(self):
        with self.assertRaises(IdiomError):
            next_idioms("意气用事")

    def test_previous_idioms_link(self):
        for word in previous_idioms("一心一意"):
            self.assertEqual(word[-1], "一")

    def test_previous_idioms_unknown(self):
        with self.assertRaises(IdiomError):
            previous_idioms("苹果手机")

    def test_check_idiom_ok(self):
        check_idiom("一心一意")

    def test_check_idiom_empty(self):
        with self.assertRaises(IdiomError):
            check_idiom("")

    def test_check_idiom_not_four(self):
        with self.assertRaises(IdiomError):
            check_idiom("一心一")

    def test_check_idiom_not_in_table(self):
        with self.assertRaises(IdiomError):
            check_idiom("意气用事")

    def test_check_idiom_not_chinese(self):
        with self.assertRaises(IdiomError):
            check_idiom("abcd")


class IsChainTest(unittest.TestCase):
    def test_valid_chain(self):
        self.assertTrue(is_chain(["一心一意", "意气风发", "发扬光大"]))

    def test_single_word(self):
        self.assertTrue(is_chain(["一心一意"]))

    def test_broken_link(self):
        self.assertFalse(is_chain(["一心一意", "发扬光大"]))

    def test_repeated_word(self):
        self.assertFalse(is_chain(["一心一意", "意气风发", "意气风发"]))

    def test_wrong_word_length(self):
        self.assertFalse(is_chain(["一心一意", "意气"]))

    def test_empty(self):
        self.assertFalse(is_chain([]))

    def test_string_input(self):
        self.assertFalse(is_chain("一心一意"))

    def test_non_chinese(self):
        self.assertFalse(is_chain(["一心一意", "abcd"]))

    def test_require_known_rejects_unknown(self):
        self.assertFalse(is_chain(["一心一意", "意气用事"], require_known=True))

    def test_unknown_accepted_by_default(self):
        self.assertTrue(is_chain(["一心一意", "意气用事"]))


class BuildChainTest(unittest.TestCase):
    def test_default_length(self):
        chain = build_chain("一心一意", seed=1)
        self.assertEqual(len(chain), DEFAULT_LENGTH)

    def test_valid_chain(self):
        chain = build_chain("一心一意", 5, seed=2)
        self.assertEqual(len(chain), 5)
        self.assertTrue(is_chain(chain, require_known=True))

    def test_starts_with_given(self):
        self.assertEqual(build_chain("水到渠成", 3, seed=3)[0], "水到渠成")

    def test_deterministic(self):
        self.assertEqual(
            build_chain("一心一意", 4, seed=11),
            build_chain("一心一意", 4, seed=11),
        )

    def test_unknown_start(self):
        with self.assertRaises(IdiomError):
            build_chain("意气用事")

    def test_length_too_small(self):
        with self.assertRaises(IdiomError):
            build_chain("一心一意", 1)

    def test_length_too_large(self):
        with self.assertRaises(IdiomError):
            build_chain("一心一意", MAX_LENGTH + 1)

    def test_length_bool_rejected(self):
        with self.assertRaises(IdiomError):
            build_chain("一心一意", True)

    def test_max_length_chain(self):
        chain = build_chain("一心一意", MAX_LENGTH, seed=5)
        self.assertEqual(len(chain), MAX_LENGTH)
        self.assertTrue(is_chain(chain, require_known=True))

    def test_unsolvable_start(self):
        with self.assertRaises(IdiomError):
            build_chain("一望无际", 3)


class CheckLengthTest(unittest.TestCase):
    def test_bounds(self):
        check_length(MIN_LENGTH)
        check_length(MAX_LENGTH)

    def test_below_min(self):
        with self.assertRaises(IdiomError):
            check_length(MIN_LENGTH - 1)

    def test_above_max(self):
        with self.assertRaises(IdiomError):
            check_length(MAX_LENGTH + 1)

    def test_not_int(self):
        with self.assertRaises(IdiomError):
            check_length("4")


class FindChainsTest(unittest.TestCase):
    def test_returns_chains(self):
        chains = find_chains("一心一意", 4, limit=5)
        self.assertTrue(chains)
        for chain in chains:
            self.assertEqual(len(chain), 4)
            self.assertTrue(is_chain(chain, require_known=True))

    def test_respects_limit(self):
        chains = find_chains("一心一意", 3, limit=1)
        self.assertEqual(len(chains), 1)

    def test_sorted_unique(self):
        chains = find_chains("一心一意", 3, limit=50)
        self.assertEqual(len(chains), len({tuple(c) for c in chains}))

    def test_unknown_start(self):
        with self.assertRaises(IdiomError):
            find_chains("意气用事", 3)

    def test_invalid_limit(self):
        with self.assertRaises(IdiomError):
            find_chains("一心一意", 3, limit=0)

    def test_no_result_returns_empty(self):
        self.assertEqual(find_chains("一望无际", 3), [])


class NormalizeTest(unittest.TestCase):
    def test_arrow(self):
        self.assertEqual(
            normalize_chain("一心一意 → 意气风发 → 发扬光大"),
            ["一心一意", "意气风发", "发扬光大"],
        )

    def test_ascii_arrow(self):
        self.assertEqual(
            normalize_chain("一心一意->意气风发"),
            ["一心一意", "意气风发"],
        )

    def test_spaces_and_punctuation(self):
        self.assertEqual(
            normalize_chain("一心一意，意气风发、发扬光大"),
            ["一心一意", "意气风发", "发扬光大"],
        )

    def test_empty(self):
        self.assertEqual(normalize_chain("   "), [])

    def test_non_string(self):
        self.assertEqual(normalize_chain(None), [])


class WorksheetTest(unittest.TestCase):
    def test_answer_is_valid(self):
        item = WorksheetItem("水到渠成", 4)
        self.assertTrue(is_chain(item.answer, require_known=True))
        self.assertEqual(len(item.answer), 4)

    def test_answer_text(self):
        item = WorksheetItem("一心一意", 1 + 2)
        self.assertIn(" → ", item.answer_text)

    def test_meaning(self):
        self.assertEqual(WorksheetItem("一心一意").meaning, IDIOMS["一心一意"])

    def test_frozen(self):
        item = WorksheetItem("一心一意")
        with self.assertRaises(FrozenInstanceError):
            item.start = "水到渠成"

    def test_check_answer_ok(self):
        item = WorksheetItem("一心一意", 3)
        self.assertTrue(check_answer(item, "一心一意 → 意气风发 → 发扬光大"))

    def test_check_answer_unknown_but_valid(self):
        item = WorksheetItem("一心一意", 2)
        self.assertTrue(check_answer(item, "一心一意 意气用事"))

    def test_check_answer_wrong_start(self):
        item = WorksheetItem("一心一意", 2)
        self.assertFalse(check_answer(item, "意气风发 → 发扬光大"))

    def test_check_answer_wrong_length(self):
        item = WorksheetItem("一心一意", 4)
        self.assertFalse(check_answer(item, "一心一意 → 意气风发"))

    def test_check_answer_broken_link(self):
        item = WorksheetItem("一心一意", 2)
        self.assertFalse(check_answer(item, "一心一意 → 发扬光大"))

    def test_check_answer_empty(self):
        item = WorksheetItem("一心一意")
        self.assertFalse(check_answer(item, ""))

    def test_check_answer_non_item(self):
        self.assertFalse(check_answer(None, "一心一意"))


class BuildWorksheetTest(unittest.TestCase):
    def test_count(self):
        items = build_worksheet(6, 4, seed=1)
        self.assertEqual(len(items), 6)

    def test_unique_starts(self):
        items = build_worksheet(10, 4, seed=2)
        self.assertEqual(len({item.start for item in items}), 10)

    def test_all_solvable(self):
        for item in build_worksheet(8, 5, seed=3):
            self.assertEqual(len(item.answer), 5)

    def test_deterministic(self):
        first = build_worksheet(5, 4, seed=7)
        second = build_worksheet(5, 4, seed=7)
        self.assertEqual([item.start for item in first], [item.start for item in second])

    def test_invalid_count(self):
        for bad in (0, -1, True, "3"):
            with self.assertRaises(IdiomError):
                build_worksheet(bad)

    def test_too_many(self):
        with self.assertRaises(IdiomError):
            build_worksheet(10_000)

    def test_invalid_length(self):
        with self.assertRaises(IdiomError):
            build_worksheet(3, 1)


class SolvableTest(unittest.TestCase):
    def test_sorted(self):
        words = solvable_starts(4)
        self.assertEqual(words, sorted(words))

    def test_all_can_reach(self):
        for word in solvable_starts(3)[:40]:
            self.assertEqual(len(build_chain(word, 3, seed=1)), 3)

    def test_returns_copy(self):
        first = solvable_starts(4)
        first.clear()
        self.assertTrue(solvable_starts(4))

    def test_invalid_length(self):
        with self.assertRaises(IdiomError):
            solvable_starts(99)

    def test_stats(self):
        available, total = chain_stats(4)
        self.assertEqual(total, len(IDIOMS))
        self.assertEqual(available, len(solvable_starts(4)))


if __name__ == "__main__":
    unittest.main()
