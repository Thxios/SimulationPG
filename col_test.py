
from circle_col import *


a = vector(3, 4)
line = Line(vector(-1, 2), (4, 4))
print(line.proj)
print(line.proj_inv)
p = line.projection(a)
print(line.un_projection(p))



