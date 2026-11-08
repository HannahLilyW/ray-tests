from ray import tune
import math
import time
import datetime


start = datetime.datetime.now()

# Simulated expensive training function that depends on 2 hyperparameters, x and y, read from a config.
def training_function(config):
    x, y = config['x'], config['y']
    time.sleep(10)
    score = objective(x, y)
    tune.report({'score': score})


def objective(x, y):
    return math.sqrt((x**2 + y**2)/2)


result = tune.run(
    training_function,
    config={
        # This guarantees that every hyperparameter combination will be sampled.
        'x': tune.grid_search([-1, -.5, 0, .5, 1]),
        'y': tune.grid_search([-1, 0.5, 0, .5, 1])
    }
)


# The best config reported by this should end up being {'x': 0, 'y': 0} since that minimizes the score.
print(result.get_best_config(metric='score', mode='min'))

end = datetime.datetime.now()

time_taken = end - start

print(time_taken.seconds)