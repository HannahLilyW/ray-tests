import ray

ray.init()  # type: ignore

## Running a Task

@ray.remote  # This indicates the task should run remotely
def square(x: int) -> int:
    return x * x

futures = [square.remote(i) for i in range(4)]

print(ray.get(futures))
