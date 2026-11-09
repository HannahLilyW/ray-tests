import time

import ray

ray.init()


database = [
    "Learning",
    "Ray",
    "Flexible",
    "Distributed",
    "Python",
    "for",
    "Machine",
    "Learning"
]

db_object_ref = ray.put(database)

def retrieve(item):
    time.sleep(item / 10.)
    return item, database[item]

@ray.remote
def retrieve_task(item, db):
    time.sleep(item / 10.)
    return item, db[item]

@ray.remote
def follow_up_task(retrieve_result):
    original_item, _ = retrieve_result
    follow_up_result = retrieve(original_item + 1)
    return retrieve_result, follow_up_result

def print_runtime(input_data, start_time):
    print(f'Runtime: {time.time() - start_time:.2f} seconds')
    print('Data:')
    print(*input_data, sep='\n')

start = time.time()
retrieve_refs = [retrieve_task.remote(item, db_object_ref) for item in [0, 2, 4, 6]]
follow_up_refs = [follow_up_task.remote(ref) for ref in retrieve_refs]
all_data = []

while len(retrieve_refs) > 0:
    finished, retrieve_refs = ray.wait(
        retrieve_refs, num_returns=2, timeout=7.0
    )
    data = ray.get(finished)
    print_runtime(data, start)
    all_data.extend(data)

print('follow up refs:')
result = [print(data) for data in ray.get(follow_up_refs)]