"""
peakdetect_delta -- find positive spike-like peaks, using Delta_raise and Delta_fall threshold.
"""

def peakdetect_simpleedge(ya, rdelta=1.0, fdelta=-1.0):
    """find positive peaks, using Delta_raise and Delta_fall threshold.

    ya is 1-D array-like object
    rdelta is raising delta value to identify the start of peak
    fdelta is falling delta value to identify the end of peak

    returns list of tuples, [((pvalue, pindex), (sindes, eindex)), ...], where,
      pvalue is ya[pindex]
      pindex is index detected as a peak
      sindex is start index of the peak (0 <= sindex <= len(ya)-1),
          which satisfies, 
            ya[sindex+1] - ya[sindex] > rdelta
      eindex is end index of the peak (1 <= eindex <= len(ya)), which satisfies
            ya[eindex] - ya[eindex-1] < fdelta
          this means ya[sindex:eindex] takes the detected peak
    """
    return list(_peakdetect_simpleedge_gen(ya, rdelta, fdelta))


def _peakdetect_simpleedge_gen(ya, rdelta=1.0, fdelta=-1.0):
    """find positive peaks, using Delta_raise and Delta_fall threshold.

    ya is 1-D array-like object
    rdelta is raising delta value to identify the start of peak
    fdelta is falling delta value to identify the end of peak

    yields tuples ((pvalue, pindex), (sindes, eindex)), where,
      pvalue is ya[pindex]
      pindex is index detected as a peak
      sindex is start index of the peak (0 <= sindex <= len(ya)-1),
          which satisfies, 
            ya[sindex+1] - ya[sindex] > rdelta
      eindex is end index of the peak (1 <= eindex <= len(ya)), which satisfies
            ya[eindex] - ya[eindex-1] < fdelta
          this means ya[sindex:eindex] takes the detected peak
    """

    # peak detection mode?
    pdet = False

    if len(ya) <= 1:
        return

    pidx = None
    pvalue = None
    sidx = None
    for i, (y0, y1) in enumerate(zip(ya[:-1], ya[1:])):
        dy = y1 - y0
        if pdet:
            # fall down?
            if dy < fdelta:
                yield ((pvalue, pidx), (sidx, i+2))
                pdet = False
            else:
                # update peak position?
                if pvalue < y1:
                    pidx = i+1
                    pvalue = y1
        else:
            # raise up ?
            if dy > rdelta:
                sidx = i
                pidx = i+1
                pvalue = y1
                pdet = True

    if pdet:
        # exceptional process, ya[-1] is still a part of peak
        yield ((pvalue, pidx), (sidx, len(ya)))

    return


def _peakdetect_gen(ya, rdelta=1.0, fdelta=-1.0, minimumspace=-1):
    """Find positive peaks, using Delta_raise and Delta_fall threshold.
    Peaks are seperated with minimumspace indices of intervals at least.

    ya is 1-D array-like object
    rdelta is raising delta value to identfy the start of peak
    fdelta is falling delta value to identify the end of peak
    minimusapce is minimum number of channels resides 2 individual peak curves, which means
        (eidx of i-th peak) - (sidx of i-th peak) >= minimumspace

    yields tuples, ((pvalue, pindex), (sindes, eindex)), where,
      pvalue is ya[pindex]
      pindex is index detected as a peak
      sindex is start index of the peak (0 <= sindex <= len(ya)-1),
          which satisfies, 
            ya[sindex+1] - ya[sindex] > rdelta
      eindex is end index of the peak (1 <= eindex <= len(ya)), which satisfies
            ya[eindex] - ya[eindex-1] < fdelta
          this means ya[sindex:eindex] takes the detected peak
    """

    if minimumspace <= -1:
        # merge operation is not required
        yield from _peakdetect_simpleedge_gen(ya, rdelta, fdelta)
    else:
        a = None
        for b in _peakdetect_simpleedge_gen(ya, rdelta, fdelta):
            if a is None:
                a = b
                continue
            else:
                if b[1][0] - a[1][1] < minimumspace:
                    a = _mergepeaks(a, b)
                else:
                    yield a
                    a = b
        if a is not None:
            yield a


def peakdetect(ya, rdelta=1.0, fdelta=-1.0, minimumspace=-1):
    """Find positive peaks, using Delta_raise and Delta_fall threshold.
    Peaks are seperated with minimumspace indices of intervals at least.

    ya is 1-D array-like object
    rdelta is raising delta value to identfy the start of peak
    fdelta is falling delta value to identify the end of peak
    minimusapce is minimum number of channels resides 2 individual peak curve, which means
        (eidx of i-th peak) - (sidx of i-th peak) >= minimumspace

    returns list of tuples, [((pvalue, pindex), (sindes, eindex)), ...], where,
      pvalue is ya[pindex]
      pindex is index detected as a peak
      sindex is start index of the peak (0 <= sindex <= len(ya)-1),
          which satisfies, 
            ya[sindex+1] - ya[sindex] > rdelta
      eindex is end index of the peak (1 <= eindex <= len(ya)), which satisfies
            ya[eindex] - ya[eindex-1] < fdelta
          this means ya[sindex:eindex] takes the detected peak
    """
    return list(_peakdetect_gen(ya, rdelta, fdelta, minimumspace))


def _mergepeaks(a, b):
    """merge 2 peaks to 1 peak information
    a, b are peak elements returned by peakdetect_simpleedge, consists of
        ((pvalue, pidx), (sidx, eidx)),
        pvalue is value at pidx
        pidx is positive peak value
        sidx is the start index of the peak
        eidx is the end index of the peak, y[sidx:eidx] takes whole curve
            including the peak
    return value is a tuple of peak element of
        ((max(a.pvalue, b.pvalue),
          [index of new peak]),
         (a.sidx, b.eidx))
    """
    return (max(a[0], b[0]), (a[1][0], b[1][1]))
