import unittest
from app.utils import KMP


class KMPTests(unittest.TestCase):
    def test_string_pattern_matching(self):
        kmp = KMP()

        pattern_1 = "abc"
        dataset_1 = "abbabbabbcbabcaabbababcababa"
        expected_1 = [11, 20]

        self.assertListEqual(kmp.search(dataset_1, pattern_1), expected_1)

        pattern_2 = "aa"
        dataset_2 = "aaaaaaaaa"
        expected_2 = [0, 1, 2, 3, 4, 5, 6, 7]

        self.assertListEqual(kmp.search(dataset_2, pattern_2), expected_2)

    def test_byte_pattern_matching(self):
        kmp = KMP()

        pattern_1 = [0x21, 0x37]
        dataset_1 = [0x22, 0x21, 0x00, 0x12, 0x83, 0x92, 0x21, 0x37, 0x69, 0x37, 0x35]
        expected_1 = [6]

        self.assertListEqual(kmp.search(dataset_1, pattern_1), expected_1)

        pattern_2 = [0x69, 0x69]
        dataset_2 = [
            0x82,
            0x91,
            0x00,
            0x00,
            0x60,
            0x69,
            0x12,
            0x45,
            0x69,
            0x69,
            0x69,
            0x99,
        ]
        expected_2 = [8, 9]

        self.assertListEqual(kmp.search(dataset_2, pattern_2), expected_2)

        #                   012345678 90123 4 567890123 456789012   3   4   5 6 7 89012
        newline_pattern = b"testtest\ntest\r\nalsotest\rmoredata\x22\x33\x44\n\r\ndadad"
        newline_n = b"\n"
        newline_r = b"\r"
        newline_nr = b"\n\r"
        newline_rn = b"\r\n"

        newline_n_expected = [8, 14, 35, 37]
        newline_r_expected = [13, 23, 36]
        newline_nr_expected = [35]
        newline_rn_expected = [13, 36]

        self.assertListEqual(kmp.search(newline_pattern, newline_n), newline_n_expected)
        self.assertListEqual(kmp.search(newline_pattern, newline_r), newline_r_expected)
        self.assertListEqual(
            kmp.search(newline_pattern, newline_nr), newline_nr_expected
        )
        self.assertListEqual(
            kmp.search(newline_pattern, newline_rn), newline_rn_expected
        )
