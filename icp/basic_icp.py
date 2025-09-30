import numpy as np 
import matplotlib.pyplot as plt


source = np.loadtxt('data/bunny_part1.xyz')
target = np.loadtxt('data/bunny_part2.xyz')
print(f"Shape of source: {source.shape}")
print(f"Shape of target: {target.shape}")

def find_closest_point(point_xyz, target_pointset):
    return np.argmin(np.linalg.norm(target_pointset - point_xyz, axis=1))

def find_transformation_matrix(source, target):
    """
    Kabsch algorithm used to find the transformation matrix that best aligns the source point to the target point
    source, target: Nx3 arrays of corresponding points
    Returns R (3x3), t (3,)
    """
    # get the centroid of each point set 
    centroid_source = np.mean(source, axis=0)
    centroid_target = np.mean(target, axis=0)

    # subtract the centroids
    source_centered = source - centroid_source
    target_centered = target - centroid_target

    # compute covariance matrix
    H = source_centered.T @ target_centered

    # SVD
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # handle reflection case
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # compute translation
    t = centroid_target - R @ centroid_source

    return R, t


def icp(source, target, num_iterations=10):
    # iterate 10 times 
    for i in range(num_iterations): 
        print(f"Iteration {i}")
        correspondences = []
        for point in source:
            # find the closest point in the target point set 
            closest_point_index = find_closest_point(point, target)
            correspondences.append(target[closest_point_index])
        correspondences = np.array(correspondences)
        
        # find the transformation matrix that best aligns the source point to the target point 
        R, t = find_transformation_matrix(source, correspondences)

        # apply the transformation matrix to the source point
        source = (R @ source.T).T + t

        current_error = np.linalg.norm(source - correspondences) / np.sqrt(source.shape[0])
        print(f"Current RMSE: {current_error}")

    # compute the error between the source point and the correspondences
    # the reason we use correspondence and not the target point set here 
    # is 1) the order of the source and target isn't the same. the correspondence here is sorted by the "closest" point to the source point. 
    # 2) we also don't know that they are the exact same shape. 
    final_error = np.linalg.norm(source - correspondences) / np.sqrt(source.shape[0])
    return source, final_error

source_original = source.copy()
target_original = target.copy()
transformed_source, final_error = icp(source, target, num_iterations=10)
print(f"Final error: {final_error}")


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(source_original[:,0][::100], source_original[:,1][::100], source_original[:,2][::100], color='red')
ax.scatter(target_original[:,0][::100], target_original[:,1][::100], target_original[:,2][::100], color='blue')
ax.scatter(transformed_source[:,0][::100], transformed_source[:,1][::100], transformed_source[:,2][::100], color='green')
plt.show()

