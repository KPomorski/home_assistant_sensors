import pylotoncycle
import json
import dotenv
import os
import database
from peloton import PelotonRide, PelotonMetric


dotenv.load_dotenv()
conn = pylotoncycle.PylotonCycle(os.environ['USERNAME'], os.environ['PASSWORD'])
workouts = conn.GetRecentWorkouts(5)

for workout in workouts:
    metrics = conn.GetWorkoutMetricsById(workout['id'], frequency=10)
    peloton_workout = PelotonRide(user=conn.GetMe()['username'], workout=workout, metrics=metrics)
    with open(f'{peloton_workout.user}_workout_{peloton_workout.id}.json', 'w') as json_file:
        json_file.write(json.dumps(workout, indent=4))
        json_file.close()
    with open(f'{peloton_workout.user}_metrics_{peloton_workout.id}.json', 'w') as json_file:
        json_file.write(json.dumps(metrics, indent=4))
        json_file.close()
        time = metrics['seconds_since_pedaling_start']
    for metric in metrics['metrics']:
        peloton_metric = PelotonMetric(metric, time)
        with open(f'{peloton_workout.user}_{peloton_workout.id}_{peloton_metric.display_name}.json', 'w') as json_file:
            json_file.write(json.dumps(peloton_metric.metric_dict, indent=4))
            json_file.close()
