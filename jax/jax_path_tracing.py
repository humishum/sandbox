# https://blog.evjang.com/2019/11/jaxpt.html

# Imports 
import jax.numpy as np
import jax.numpy as jnp

from jax import jit, grad, vmap, random, lax
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
 Differentiable scene intersection with Distance fields 
 we compute point(s) y in the scene with ray w_i, which typically involved traversing a bounding volume hierarchy 
 y can be expressed as an eq of the origin point x and ray tracing direction w_i, with goal being to find distance t
 y = x + t*w_i 
"""
"""
Signed Distance Field 
an SDF over position p specifies the distance you can move in any direction without coming into contact with an object 
SDFs wont ever overshoot the object 
any 3d object can be SDF'd basically. 
composable, i.e. you can do union and intersections 

"""

def sd_floor(p): 
    """ Example functiom for the signed distance field for a place that passes through origin 
    and is perpendicular to y axis"""
    return p.y

# Ray marching algorithm
def raymarch(ro, rd, sdf_fn, max_steps = 10): 
    t = 0
    for _ in range(max_steps): 
        p = ro + t*rd
        t = t+sdf_fn(p)
    return t

### Example SDF functions I got from chat gbt
def sdf_sphere(p, center=jnp.array([0.0, 0.0, 0.0]), radius=1.0):
    return jnp.linalg.norm(p - center) - radius
# for a plane y = 0 
def sdf_plane(p):
    return p[1]  # y-component gives the perpendicular distance
# for an axis aligned box cneteredn at c with half dimensions b
def sdf_box(p, center=jnp.array([0.0, 0.0, 0.0]), bounds=jnp.array([1.0, 1.0, 1.0])):
    q = jnp.abs(p - center) - bounds
    return jnp.linalg.norm(jnp.maximum(q, 0.0)) + jnp.minimum(jnp.max(q), 0.0)
# unuion of shapes 
def sdf_union(sdf1, sdf2, p):
    return jnp.minimum(sdf1(p), sdf2(p))
# Scene with sphere and plane  THIS IS SICK!!
def sdf_scene(p):
    sphere_distance = sdf_sphere(p, center=jnp.array([0.0, 1.0, 0.0]), radius=1.0)
    plane_distance = sdf_plane(p)
    return jnp.minimum(sphere_distance, plane_distance)  # Combine with a union

