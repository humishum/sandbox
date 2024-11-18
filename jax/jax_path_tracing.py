# https://blog.evjang.com/2019/11/jaxpt.html

# Imports 
import jax.numpy as np
from jax import jit, grad, vmap, random, lax
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
 Differentiable scene intersection with Distance fields 
 we compute point(s) y in the scene with ray w_i, which typucally involved traversing a bounding volume hierarchy 
 y can be expressed as an eq of the origin point x and ray tracing direction w_i, with goal being to find distance t
 y = x + t*w_i 
"""
"""
Signed Distance Field 
an SDF over position p specifies the distance you can move in any direction without coming into contact with an object 

"""