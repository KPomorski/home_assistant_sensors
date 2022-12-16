import pylotoncycle
import json
import datetime
from database import DBHelper


class PelotonRide:
    def __init__(self, pyloton, workout, metrics):
        self.workout = workout
        self.db = DBHelper()
        self.workout_id = workout['id']
        self.workout_name = workout['name']
        self.workout_title = workout['ride']['title']
        self.workout_description = workout['ride']['description']
        self.workout_image_url = workout['ride']['image_url']
        self.userid = pyloton.userid
        self.username = pyloton.username
        self.workout_discipline = workout['fitness_discipline']
        self.workout_started_at = datetime.datetime.fromtimestamp(workout['created_at'])
        self.workout_ended_at = datetime.datetime.fromtimestamp(workout['end_time'])
        self.workout_duration = int(workout['overall_summary']['ride']['duration'])
        self.workout_instructor = workout['instructor_name']
        self.workout_difficulty = workout['ride']['difficulty_estimate']
        self.workout_difficulty_level = workout['ride']['difficulty_level']
        self.workout_difficulty_rating_avg = workout['ride']['difficulty_rating_avg']
        self.workout_difficulty_rating_count = workout['ride']['difficulty_rating_count']
        self.workout_status = workout['overall_summary']['status']
        self.metrics = metrics

    def save_new(self):
        print(f"Saving workout {self.workout_id} for user {self.username}")
        # check to see if the record already exists:
        exist_query = f"select workout_id from peloton.workouts where workout_id = '{self.workout_id}' and user_id = '{self.userid}';"
        self.db.fetch(exist_query)
        if self.db.cur.rowcount == 0:
            query = "INSERT INTO peloton.workouts " \
                    "(workout_id, workout_name, workout_title, workout_image_url, discipline, user_id, username," \
                    " workout_started_at, workout_ended_at, duration," \
                    " instructor," \
                    " difficulty_est, difficulty_level, difficulty_rating_avg, difficulty_rating_count," \
                    " workout_status)" \
                    " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            values = (self.workout_id,
                      self.workout_name,
                      self.workout_title,
                      self.workout_image_url,
                      self.workout_discipline,
                      self.userid,
                      self.username,
                      self.workout_started_at,
                      self.workout_ended_at,
                      self.workout_duration,
                      self.workout_instructor,
                      self.workout_difficulty,
                      self.workout_difficulty_level,
                      self.workout_difficulty_rating_avg,
                      self.workout_difficulty_rating_count,
                      self.workout_status)
            self.db.insert(query, values)
        else:
            print(f"Workout {self.workout_id} already exists.")

    def save_workout_as_json(self):
        with open(f'{self.username}_workout_{self.workout_id}.json', 'w') as json_file:
            json_file.write(json.dumps(self.workout, indent=4))
            json_file.close()
        with open(f'{self.username}_metrics_{self.workout_id}.json', 'w') as json_file:
            json_file.write(json.dumps(self.metrics, indent=4))
            json_file.close()


class PelotonMetric:
    def __init__(self, pyloton, workout, metric, time):
        self.db = DBHelper()
        self.userid = pyloton.userid
        self.username = pyloton.username
        self.workoutid = workout['id']
        self.display_name = metric['display_name']
        self.avg_value = metric['average_value']
        self.max_value = metric['max_value']
        self.display_unit = metric['display_unit']
        self.slug = metric['slug']
        self.time = str(time)
        self.values = str(metric['values'])
        self.metric_dict = {
            "Display Name": self.display_name,
            "Average Value": self.avg_value,
            "Display Unit": self.display_unit,
            "Slug": self.slug,
            "Values": self.values,
            "Max Values": self.max_value,
            "Time": self.time
        }

    def save_new(self):
        print(f"Saving {self.display_name} metrics for workout {self.workoutid} for user {self.username}")
        # check to see if the record already exists:
        exist_query = f"select workout_id from peloton.metrics where workout_id = '{self.workoutid}' and user_id = '{self.userid}' and metric_name = '{self.display_name}';"
        self.db.fetch(exist_query)
        if self.db.cur.rowcount == 0:
            query = "INSERT INTO peloton.metrics " \
                    "(workout_id, user_id, metric_name, metric_avg, max_value, display_unit, slug, metric_values, time_values)" \
                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            values = (self.workoutid,
                      self.userid,
                      self.display_name,
                      self.avg_value,
                      self.max_value,
                      self.display_unit,
                      self.slug,
                      self.values,
                      self.time
                      )
            print(values)
            self.db.insert(query, values)
        else:
            print(f"Metric for workout {self.workoutid} already exists.")
