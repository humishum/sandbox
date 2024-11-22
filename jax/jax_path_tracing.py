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

def length(p):
  return np.linalg.norm(p, axis=1, keepdims=True)
  
def normalize(p):
  return p/length(p)

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

# Hard coded enums for object definitions: 
OBJ_NONE=0.0
OBJ_FLOOR=0.1
OBJ_CEIL=.2
OBJ_WALL_RD=.3
OBJ_WALL_WH=.4
OBJ_WALL_GR=.5
OBJ_SHORT_BLOCK=.6
OBJ_TALL_BLOCK=.7
OBJ_LIGHT=1.0
OBJ_SPHERE=0.9

def df(obj_id, dist):
  """ object id and distance of a ray-scene intersection. This function just zips into np"""
  return np.array([obj_id, dist])

# List of SDFs : https://iquilezles.org/articles/distfunctions/

# SDF for a box: 
def udBox(p, b):
  # b = half-widths
#   return length(np.maximum(np.abs(p)-b,0.0)) idk if this is right
    return np.linalg.norm(np.maximum(np.abs(p)-b,0.0))

# Rotation operations on a point 
def rotateX(p,a):
  # We won't be using rotateX for this tutorial.
  c = np.cos(a); s = np.sin(a);
  px,py,pz=p[0],p[1],p[2]
  return np.array([px,c*py-s*pz,s*py+c*pz])

def rotateY(p,a):
  c = np.cos(a); s = np.sin(a);
  px,py,pz=p[0],p[1],p[2]
  return np.array([c*px+s*pz,py,-s*px+c*pz])

def rotateZ(p,a):
  c = np.cos(a); s = np.sin(a);
  px,py,pz=p[0],p[1],p[2]
  return np.array([c*px-s*py,s*px+c*py,pz])


# Function to compute union of two SDfs. written this way for jax-ablitily 
def opU(a,b):
  condition = np.tile(a[1,None]<b[1,None], [2])
  return np.where(condition, a, b)
    

def sdScene(p):
  # p is [3,]
  px,py,pz=p[0],p[1],p[2]
  # floor
  obj_floor = df(OBJ_FLOOR, py) # py = distance from y=0
  res = obj_floor  
  # ceiling
  obj_ceil = df(OBJ_CEIL, 4.-py)
  res = opU(res,obj_ceil)
  # backwall
  obj_bwall = df(OBJ_WALL_WH, 4.-pz)
  res = opU(res,obj_bwall)
  # leftwall
  obj_lwall = df(OBJ_WALL_RD, px-(-2))
  res = opU(res,obj_lwall)
  # rightwall
  obj_rwall = df(OBJ_WALL_GR, 2-px)
  res = opU(res,obj_rwall)
  # light
  obj_light = df(OBJ_LIGHT, udBox(p - np.array([0,3.9,2]), np.array([.5,.01,.5])))
  res = opU(res,obj_light)
  # tall block
  bh = 1.3
  p2 = rotateY(p- np.array([-.64,bh,2.6]),.15*np.pi)
  d = udBox(p2, np.array([.6,bh,.6]))
  obj_tall_block = df(OBJ_TALL_BLOCK, d)
  res = opU(res,obj_tall_block)  
  # short block
  bw = .6
  p2 = rotateY(p- np.array([.65,bw,1.7]),-.1*np.pi)
  d = udBox(p2, np.array([bw,bw,bw]))
  obj_short_block = df(OBJ_SHORT_BLOCK, d)
  res = opU(res,obj_short_block)
  return res

def dist(p):
  # return the distance-component only
  return sdScene(p)[1]

def calcNormalWithAutograd(p):
  return normalize(grad(dist)(p))