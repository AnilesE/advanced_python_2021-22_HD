# __init__ py is required in a folder 
# to be recognized as a python module
# otherwise the import statements won't work
# the %%writefile magic allows the jupyter cell content to be stored as a file

# lets load core into the name space as well
from . import basic
