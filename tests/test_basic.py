import sys
from pathlib import Path
# -------- START of inconvenient addon block --------
# This block is not necessary if you have installed your package
# using e.g. pip install -e (requires setup.py)
# or have a symbolic link in your sitepackages (my preferend way)
sys.path.append(
    str(Path(__file__).parent.parent.resolve())
)
# It make import peak_finder possible
# This is a demo hack for the course :)
# --------  END of inconvenient addon block  --------

import peak_finder

def test_find_peaks():
    peaks = peak_finder.basic.find_peaks([0, 2, 1])
    assert peaks == [2] 

def test_find_peaks_example():
    peaks = peak_finder.basic.find_peaks([1,5,6,4,1,2,3,2])
    assert peaks == [6,3]

def test_rand_is_gr():
    peaks = peak_finder.basic.find_peaks([6,1,0])
    assert peaks == [6]

def test_None():
    peaks = peak_finder.basic.find_peaks([6,1,0, None])
    assert peaks == [6]

def test_tuple():
    peaks = peak_finder.basic.find_peaks([(20,0,0), (0,19,0), (0,0,0), (255, 255, 255)])
    assert peaks == [(0,0,0)]

