import pylotoncycle
import json
import dotenv
import os
from database import DBHelper
from peloton import PelotonRide, PelotonMetric


dotenv.load_dotenv()
db = DBHelper()
pylo = pylotoncycle.PylotonCycle(os.environ['USERNAME'], os.environ['PASSWORD'])
pylo.GetMe()
workouts = pylo.GetRecentWorkouts(5)

for workout in workouts:
    peloton_metrics = pylo.GetWorkoutMetricsById(workout['id'], frequency=10)
    peloton_workout = PelotonRide(pylo, workout=workout, metrics=peloton_metrics)
    peloton_workout.save_workout_as_json()
    peloton_workout.save_new()
    for metric in peloton_metrics['metrics']:
        peloton_metric = PelotonMetric(pylo, workout, metric, time=peloton_metrics['seconds_since_pedaling_start'])
        peloton_metric.save_new()
        with open(f'{peloton_workout.username}_{peloton_workout.workout_id}_{peloton_metric.display_name}.json', 'w') as json_file:
            json_file.write(json.dumps(peloton_metric.metric_dict, indent=4))
            json_file.close()
