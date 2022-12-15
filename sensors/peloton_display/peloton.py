import pylotoncycle
import json


class PelotonRide:
    def __init__(self,user, workout, metrics):
        self.id = workout['id']
        self.workout_started = workout['created_at']
        self.workout_duration = workout['overall_summary']['ride']['duration']
        self.workout_finished = workout['end_time']
        self.workout_discipline = workout['fitness_discipline']
        self.workout_instructor = workout['instructor_name']
        self.workout_name = workout['name']
        self.workout_difficulty = workout['ride']['difficulty_estimate']
        self.workout_difficulty_level = workout['ride']['difficulty_level']
        self.workout_difficulty_rating_avg = workout['ride']['difficulty_rating_avg']
        self.workout_difficulty_rating_count = workout['ride']['difficulty_rating_count']
        self.workout_status = workout['overall_summary']['status']
        self.user = user
        self.metrics = metrics


class PelotonMetric:
    def __init__(self, metric, time):
        self.display_name = metric['display_name']
        self.avg_value = metric['average_value']
        self.display_unit = metric['display_unit']
        self.max_value = metric['max_value']
        self.slug = metric['slug']
        self.time = time
        self.values = metric['values']
        self.metric_dict = {
            "Display Name": self.display_name,
            "Average Value": self.avg_value,
            "Display Unit": self.display_unit,
            "Slug": self.slug,
            "Values": self.values,
            "Max Values": self.max_value,
            "Time": self.time
        }
