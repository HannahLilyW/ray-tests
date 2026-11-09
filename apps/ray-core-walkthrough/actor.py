import ray

ray.init()  # type: ignore


# Define the Counter actor
@ray.remote
class Counter:
    def __init__(self):
        self.i: int = 0

    def get(self):
        return self.i

    def incr(self, value: int):
        self.i += value


# Create a Counter actor instance
c = Counter.remote()

# Submit calls to the actor. These calls run asynchronously but in submission order on the remote actor process.
# "Asynchronous" here means that the main Pyuthon program doesn't wait for each call to finish before moving on to the next line.
# The actor still processes the requests one at a time, leading to an accurate result here.
for _ in range(10):
    c.incr.remote(1)  # type: ignore

# Retrieve final actor state.
print(ray.get(c.get.remote()))  # type: ignore


