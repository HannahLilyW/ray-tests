# MapReduce has 3 steps:
# 
# 1. map phase: takes a set of documents and "maps" its elements (for example the words contained in them) according to a function. Produces key-value pairs.
# 2. shuffle phase:  collect and group all the outputs of the map phase according to their key.
# 3. reduce phase: aggregate or "reduce" the elements from the shuffle step.

# This is an example of MapReduce in Ray.

import subprocess

import ray

zen_of_python = subprocess.check_output(["python", "-c", "import this"])

# List of words
corpus = zen_of_python.split()

# Split the list into 3 partitions
num_partitions = 3
chunk = len(corpus) // num_partitions
partitions = [
    corpus[i * chunk: (i + 1) * chunk] for i in range(num_partitions)
]

### Map/shuffle phase
def map_function(document):
    for word in document.lower().split():
        yield word, 1

@ray.remote
def apply_map(corpus, num_partitions=3):

    # This task will return <num_partitions> results.
    map_results = [list() for _ in range(num_partitions)]

    for document in corpus:
        for result in map_function(document):

            # Assign each (word, 1) pair to a partition by using the ord() function to generate a word_index.
            # This ensures that each occurrence of a word gets shuffled to the same partition.
            first_letter = result[0].decode('utf-8')[0]
            word_index = ord(first_letter) % num_partitions

            map_results[word_index].append(result)
    return map_results

map_results = [
    apply_map
    .options(num_returns=num_partitions)  # Tells Ray to return <num_partitions> values.
    .remote(data, num_partitions=3)  # type: ignore
    for data in partitions
]

### For illustration purposes, here's what we have before the reduce phase
# for i in range(num_partitions):
#     mapper_results = ray.get(map_results[i])
#     for j, result in enumerate(mapper_results):
#         print(f'Mapper {i}, return value {j}: {result}')

### Reduce phase
@ray.remote
def apply_reduce(*results):
    reduce_results = dict()
    for res in results:
        for key, value in res:
            if key not in reduce_results:
                reduce_results[key] = 0
            reduce_results[key] += value
    return reduce_results

outputs = []
for i in range(num_partitions):
    outputs.append(
        apply_reduce.remote(*[partition[i] for partition in map_results])
    )

counts = {k: v for output in ray.get(outputs) for k, v in output.items()}

sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
for count in sorted_counts:
    print(f'{count[0].decode('utf-8')}: {count[1]}')