# -*- coding: utf-8 -*-
import sympy

# %%
x = sympy.Symbol('x')
f = 1

# %%
for t in range(1,5):
    f = f*(1-t*x)
f = 1 - f
print(f)

# %%
x_solv = sympy.nsolve(f,x,0.9)