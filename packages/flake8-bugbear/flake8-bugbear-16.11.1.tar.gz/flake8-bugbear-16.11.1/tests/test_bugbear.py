from pathlib import Path
import unittest

from bugbear import BugBearChecker
from bugbear import (
    B001,
    B002,
    B003,
    B004,
    B005,
    B006,
    B301,
    B302,
    B303,
    B304,
    B305,
    B306,
    B901,
    B950,
)


class BugbearTestCase(unittest.TestCase):
    maxDiff = None

    def test_b001(self):
        filename = Path(__file__).absolute().parent / 'b001.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B001(8, 0), B001(40, 4)],
        )

    def test_b002(self):
        filename = Path(__file__).absolute().parent / 'b002.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B002(13, 8), B002(17, 12)],
        )

    def test_b003(self):
        filename = Path(__file__).absolute().parent / 'b003.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B003(10, 0)],
        )

    def test_b004(self):
        filename = Path(__file__).absolute().parent / 'b004.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B004(3, 7), B004(5, 7)],
        )

    def test_b005(self):
        filename = Path(__file__).absolute().parent / 'b005.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B005(4, 0), B005(7, 0), B005(10, 0), B005(13, 0), B005(16, 0),
             B005(19, 0)],
        )

    def test_b006(self):
        filename = Path(__file__).absolute().parent / 'b006.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B006(8, 24), B006(12, 29), B006(16, 19), B006(20, 19)],
        )

    def test_b301_b302_b305(self):
        filename = Path(__file__).absolute().parent / 'b301_b302_b305.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B301(37, 4), B301(38, 4), B301(39, 4), B301(40, 4)] +
            [B302(41, 4), B302(42, 4), B302(43, 4), B302(44, 4)] +
            [B305(45, 4), B305(46, 4)]
        )

    def test_b303_b304(self):
        filename = Path(__file__).absolute().parent / 'b303_b304.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B303(21, 4), B304(38, 4)],
        )

    def test_b306(self):
        filename = Path(__file__).absolute().parent / 'b306.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B306(9, 10)],
        )

    def test_b901(self):
        filename = Path(__file__).absolute().parent / 'b901.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B901(8, 8), B901(35, 4)]
        )

    def test_b950(self):
        filename = Path(__file__).absolute().parent / 'b950.py'
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            [B950(6, 87, message='B950: line too long (87 > 79 characters)')],
        )


if __name__ == '__main__':
    unittest.main()
