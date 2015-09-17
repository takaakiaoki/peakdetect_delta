=======================
peakdetect_delta
=======================

Find positive spike-like peaks from 1-D array.

example
=========

.. code-block:: python

    from peakdetect_delta import peakdetect, peakdetect_sinmpleedge

    # peak are represented as a tuple ((pvalue, pidx), (sidx, eidx))
    #   pvalue: value at pidx
    #   pidx: index of the peak
    #   sidx: index where y[sidx+1] - y[sidx] > rdelta
    #   eidx: index where y[eidx] - y[eidx-1] < fdelta 
    #   so, y[sidx:eidx] takes the detected peak

    # examples of peakdetect_simpleedge
    # case 1.1
    s = [0, 0, 1.5, 2, 0, 0]
    assert peakdetect_simpleedge(s, rdelta=1, fdelta=-1) == [((2, 3), (1, 5))]

    # case 1.2
    s = [0, 2, 0, -2, 0, -2]
    assert peakdetect_simpleedge(s, rdelta=1, fdelta=1) == [((2, 1), (0, 3)),
                                                            ((0, 4), (3, 6))]

    # example of peakdetect
    s= [0, 3, 0, 2, 0, 0, -1, 1, -2, -1]
    # same as peakdetect_simpleedge
    assert peakdetect(s, rdelta=1, fdelta=-1, minimumspace=-1)
               == [((3, 1), (0, 3)), ((2, 3), (2, 5)), ((1, 7), (6, 9))]
    # first 2 peaks are merged
    assert peakdetect(s, rdelta=1, fdelta=-1, minimumspace=0)
               == [((3, 1), (0, 5)), ((1, 7), (6, 9))]
    peakdetect(s, rdelta=1, fdelta=-1, minimumspace=2)
               == [((3, 1), (0, 9))]
