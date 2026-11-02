import ray

# This is called the "Ray Client"
ray.init()

# Define the square task.
@ray.remote
def square(x: int) -> int:
    return x * x

# Launch four parallel square tasks.
futures = [square.remote(i) for i in range(4)]

# Retrieve results.
print(ray.get(futures))
# -> [0, 1, 4, 9]
