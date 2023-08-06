# importing :
from sahirPyStd import standard_deviation as s_d

# Usage - standard_error(x)
# Input - x: array of doubles
# Output - standard error of input array x
# Example = standard_error([1,2,3])
standard_error = lambda x: s_d.standard_deviation(x)/len(x)**0.5
