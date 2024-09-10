# Download a sample file
from bgen_reader import example_filepath
bgen_file = example_filepath("example.bgen")

# Read from the file
from bgen_reader import open_bgen
bgen = open_bgen(bgen_file, verbose=False)
probs0 = bgen.read(0)   # Read 1st variant
print(probs0.shape)     # Shape of the NumPy array

probs_all = bgen.read() # Read all variants
print(probs_all.shape)  # Shape of the NumPy array