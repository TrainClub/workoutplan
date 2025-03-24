from datetime import datetime
import random
import json

class DataProcessor:
    def __init__(self, event, workout_event=None):
        self.event = event
        self.workout_event = workout_event
        self.created_at = datetime.utcnow().isoformat()
        self.user_data = event.get('new_member', {}).get('user_data', {})
        self.user_id = self.user_data.get('user_id')

    def _get_user_id(self):
        try:
            if not self.user_id:
                raise ValueError("[ERROR] Missing user_id in event")
            return self.user_id
        except Exception as err:
            print(err)

    def _workout_create_status(self):
        print('trava')
        try:
            return {
                "PK": {'S': f"USER#{self._get_user_id()}"},
                "SK": {'S': f"Treino#StatusCreated"},
                "status": {'S': 'Criado'},
                "created_at": {'S': self.created_at}

            }
        except Exception as err:
            print(err)
    
    def _create_workout_plans(self):
        if not self.workout_event:
            raise ValueError("[ERROR] Missing workout_event for workout_plans")

        workout_plan = self.workout_event.get('training_plan')
        if not workout_plan:
            raise ValueError("[ERROR] Missing workout plan data in workout_event")

        workout_items = []
        for day_plan in workout_plan:
            dia_treino = day_plan.get('day')
            if not dia_treino:
                raise ValueError("[ERROR] Missing 'day' in workout plan")

            for exercicio in day_plan.get('exercises', []):
                if not all(key in exercicio for key in ['name', 'muscle_groups', 'sets', 'reps', 'tips', 'alternatives', 'affected_muscles']):
                    raise ValueError("[ERROR] Missing required fields in exercise data")

                item = {
                    "PK": {'S': f"USER#{self._get_user_id()}"},
                    "SK": {'S': f"Treino#{dia_treino}#Exercicio#{exercicio['name']}"},
                    "MuscleGroups": {'S': exercicio['muscle_groups']},
                    "Sets": {'N': str(exercicio['sets'])},
                    "Reps": {'S': str(exercicio['reps'])},
                    "Tips": {'S': exercicio['tips']},
                    "Alternatives": {'S': json.dumps(exercicio['alternatives'], ensure_ascii=False)},  # UTF-8
                    "AffectedMuscles": {'S': json.dumps(exercicio['affected_muscles'], ensure_ascii=False)},  # UTF-8
                    "created_at": {'S': self.created_at}
                }
                workout_items.append(item)
        return workout_items

    def create_record(self, record_type):
        record_map = {
            'workout_create_status': self._workout_create_status,
            'workout_plans': self._create_workout_plans,
        }

        if record_type not in record_map:
            raise ValueError(f"[ERROR] Invalid record_type: {record_type}")

        try:
            return record_map[record_type]()
        except Exception as e:
            print(f"[ERROR] Error creating {record_type}: {e}")
            return None