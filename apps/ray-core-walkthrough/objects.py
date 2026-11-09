# Passing Objects

"""
3 ways to work with objects in Ray:
1. Implicit creation: What tasks and actors return values, they are automatically stored in Ray's distributed object store, returning object references that can be later retrieved.
2. Explicit creation: Use `ray.put` to directly place objects in the store.
3. Passing references: Pass object references to other tasks and actors, avoiding unnecessary data copying and enabling lazy execution.
"""

import numpy as np

import ray

# Define a task that sums the values in a matrix
@ray.remote
def sum_matrix(matrix):
    return np.sum(matrix)

# Call the task with a literal argument value
print(
    ray.get(
        sum_matrix.remote(
            np.ones((100, 100))
        )
    )
)

# Put a large array into the object store
matrix_ref = ray.put(np.ones((1000,1000)))

# Call the task with the object reference as an argument
print(ray.get(sum_matrix.remote(matrix_ref)))
