import pylotoncycle
import pprint
import json


username = 'username'
password = 'password'
conn = pylotoncycle.PylotonCycle(username, password)
user = conn.GetMe()['username']
workouts = conn.GetRecentWorkouts(5)

for workout in workouts:
    workout_id = workout['id']
    resp = conn.GetWorkoutMetricsById(workout_id, frequency=10)
    time = resp['seconds_since_pedaling_start']
    with open(f'{user}_{workout_id}.json', 'w') as json_file:
        result = pprint.pformat(resp)
        json_file.write(str(result))
        json_file.close()
    for metric in resp['metrics']:
        display_name = metric['display_name']
        avg_value = metric['average_value']
        display_unit = metric['display_unit']
        max_value = metric['max_value']
        slug = metric['slug']
        values = metric['values']
        metric_dict = {
            "Display Name": display_name,
            "Average Value": avg_value,
            "Display Unit": display_unit,
            "Slug": slug,
            "Values": values,
            "Max Values": max_value
                }
        with open(f'{user}_{workout_id}_{display_name}.json', 'w') as json_file:
            json_file.write(json.dumps(metric_dict, indent=4))
            json_file.close()
