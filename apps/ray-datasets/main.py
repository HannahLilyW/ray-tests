import ray

ray.init()

items: list[dict[str, str | int]] = [{'name': str(i), 'data': i} for i in range(10000)]
ds = ray.data.from_items(items)
ds.show(5)

# The following runs synchronously:
squares = ds.map(lambda x: {'data': x['data'] ** 2})  # Map each row of ds to keep only the square value of its data entry
evens = squares.filter(lambda x: x['data'] % 2 == 0)  # Filter the squares to keep only even numbers
print(evens.count())  # This should print 5000 since we just filtered out half the numbers
cubes = evens.flat_map(lambda x: [{'data': x['data']}, {'data': x['data']**3}])  # This gives us a list where each value is followed by its cube
sample = cubes.take(10)
print(sample)

# This transforms the above example into a pipeline, which lets you overlap individual tasks:
# pipe = ds.window()  # Me: It seems like the original example already does this in ray 2.59 ? window() is not recognized anymore and I can already chain the steps.
# result = ds.map(lambda x: {'data': x['data'] ** 2}) \
#         .filter(lambda x: x['data'] % 2 == 0) \
#         .flat_map(lambda x: [{'data': x['data']}, {'data': x['data']**3}]) \
#         .take(10)
# print(result)