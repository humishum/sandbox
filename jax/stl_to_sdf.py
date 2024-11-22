# yat yi b t 


import numpy as np
from stl import mesh

def plane_sdf(point, triangle):
    """
    Calculate the Signed Distance Function for a planar surface of a triangle.
    
    Parameters:
    - point: (N, 3) numpy array of points where SDF is evaluated.
    - triangle: (3, 3) numpy array representing the vertices of the triangle.
    
    Returns:
    - sdf: (N,) numpy array of SDF values.
    """
    # Triangle vertices
    v0, v1, v2 = triangle
    
    # Normal of the triangle plane
    normal = np.cross(v1 - v0, v2 - v0)
    normal = normal / np.linalg.norm(normal)  # Normalize
    
    # Point on the plane
    p0 = v0
    
    # Signed distance from points to plane
    sdf = np.dot(point - p0, normal)
    return sdf

def union_sdfs(sdfs):
    """
    Union of SDFs: point-wise minimum.
    """
    return np.min(sdfs, axis=0)

def calculate_sdf_for_stl(filename, points):
    """
    Calculate the SDF for an STL file and take the union of all planar SDFs.
    
    Parameters:
    - filename: Path to the STL file.
    - points: (N, 3) numpy array of query points for SDF evaluation.
    
    Returns:
    - combined_sdf: (N,) numpy array of SDF values after union.
    """
    # Load STL mesh
    stl_mesh = mesh.Mesh.from_file(filename)
    
    # Prepare array to collect all SDFs
    sdfs = []
    
    for triangle in stl_mesh.vectors:
        sdf = plane_sdf(points, triangle)
        sdfs.append(sdf)
    
    # Stack and combine SDFs
    sdfs = np.stack(sdfs, axis=0)
    combined_sdf = union_sdfs(sdfs)
    
    return combined_sdf

# Example usage
if __name__ == "__main__":
    # Generate a grid of query points
    grid_size = 50
    x = np.linspace(-10, 10, grid_size)
    y = np.linspace(-10, 10, grid_size)
    z = np.linspace(-10, 10, grid_size)
    xv, yv, zv = np.meshgrid(x, y, z)
    query_points = np.stack([xv.ravel(), yv.ravel(), zv.ravel()], axis=-1)

    # Input STL file
    stl_file = "example.stl"

    # Calculate SDF
    sdf = calculate_sdf_for_stl(stl_file, query_points)
    
    # Reshape SDF to match the grid
    sdf = sdf.reshape(grid_size, grid_size, grid_size)
    print("SDF Calculated and Combined.")
