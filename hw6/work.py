import numpy as np
import pandas

a = [0, 0.2, 0.3, 0.6, 0.85, 0.44, 1]
b = pandas.qcut(a,4)

print b[6]