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

import Protein


from collections import deque
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path

def test_creates_object():
    P = Protein.Protein.Protein()
    assert isinstance(P, Protein.Protein.Protein) 

def test_attributes():
    P = Protein.Protein.Protein()
    ID = "P32249"
    name = "G-protein coupled receptor 183"
    P.ID = ID
    P.name = name
    assert [P.ID, P.name] == ["P32249", "G-protein coupled receptor 183"]

def test_None_aattributes():
    P = Protein.Protein.Protein()
    assert [P.ID, P.name, P.metrics, P.AAsequence, P.fasta_file, P.identifier, P.df] == [None, None, None, None, None, None, None]

def test_create_df():
    aa_df = pd.read_csv("../data/amino_acid_properties.csv")
    aa_df = aa_df.set_index("1-letter code", drop = False)
    metrics = aa_df.to_dict()
    P = Protein.Protein.Protein(fasta_file = "P32249.fasta", metrics = metrics)
    assert len(P.create_df) == len(P.AAsequence)