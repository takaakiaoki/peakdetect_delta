import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from peakdetect_delta import peakdetect_simpleedge, peakdetect

class TestPeakdetectSimpleedge(object):
    def test_nulllist(self):
        assert peakdetect_simpleedge([]) == []

    def test_singlelist(self):
        assert peakdetect_simpleedge([1]) == []

    def test_3points(self):
        s = [0, 2, 0]
        assert peakdetect_simpleedge(s) == [((s[1], 1), (0, 3))]

    def test_tailing_excess_values(self):
        s = [0, 2, 0, -1]
        assert peakdetect_simpleedge(s) == [((s[1], 1),  (0, 3))]

    def test_heading_excess_values(self):
        s = [-0.5, 0, 2, 0]
        assert peakdetect_simpleedge(s) == [((s[2], 2), (1, 4))]

    def test_small_raise_before_peak(self):
        s = [0, 1.5, 2, 0]
        assert peakdetect_simpleedge(s) == [((s[2], 2), (0, 4))]

    def test_small_fall_after_peak(self):
        s = [0, 2, 1.5, 0]
        assert peakdetect_simpleedge(s) == [((s[1], 1), (0, 4))]

    def test_double_peaks(self):
        s = [0, 2, 0, 2, 0]
        assert peakdetect_simpleedge(s) == [((s[1], 1), (0, 3)), ((s[3], 3), (2, 5))]

    def test_double_peaks2(self):
        s = [0, 2, 0, -2, 0, -2]
        assert peakdetect_simpleedge(s) == [((s[1], 1), (0, 3)), ((s[4], 4), (3, 6))]


class TestPeakdetect(object):
    def test_nomerge(self):
        s = [0, 3, 0, 2, 0]
        assert peakdetect(s) == [((s[1], 1), (0, 3)), ((s[3], 3), (2, 5))]

    def test_merge1(self):
        s = [0, 3, 0, 2, 0, 0]
        assert peakdetect(s, minimumspace=0) == [((s[1], 1), (0, 5))]

    def test_merge2(self):
        s = [0, 3, 0, 2, 0, 0, -1, 1, -2, -1]
        assert peakdetect(s, minimumspace=0) == [((s[1], 1), (0, 5)), ((s[7], 7), (6, 9))]
