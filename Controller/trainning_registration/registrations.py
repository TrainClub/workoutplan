from datetime import datetime
import json

class DataProcessor:
    def __init__(self, event, workout_event=None):
        self.event = event or {}
        self.workout_event = workout_event or {}
        self.created_at = datetime.utcnow().isoformat()
        self.user_data = self.event.get('new_member', {}).get('user_data', {})
        self.user_id = self.user_data.get('user_id')
    
    def _get_user_id(self):
        try:
            if not self.user_id:
                raise ValueError("[ERROR] Missing user_id in event")
            return self.user_id
        except Exception as err:
            print(f"[ERROR] _get_user_id: {err}")
            return None
    
    def _workout_create_status(self):
        try:
            user_id = self._get_user_id()
            if not user_id:
                raise ValueError("[ERROR] User ID is None")
            
            return {
                "PK": {'S': f"USER#{user_id}"},
                "SK": {'S': "Treino#StatusCreated"},
                "status": {'S': "Criado"},
                "created_at": {'S': self.created_at}
            }
        except Exception as err:
            print(f"[ERROR] _workout_create_status: {err}")
            return None
    
    def _create_workout_plans(self):
        try:
            if not self.workout_event:
                raise ValueError("[ERROR] Missing workout_event for workout_plans")
            
            workout_plan = self.workout_event.get('training_plan')
            if not workout_plan:
                raise ValueError("[ERROR] Missing workout plan data in workout_event")
            
            user_id = self._get_user_id()
            if not user_id:
                raise ValueError("[ERROR] User ID is None")
            
            workout_items = []
            for day_plan in workout_plan:
                dia_treino = day_plan.get('day')
                if not dia_treino:
                    raise ValueError("[ERROR] Missing 'day' in workout plan")
                
                for exercicio in day_plan.get('exercises', []):
                    required_keys = ['name', 'muscle_groups', 'sets', 'reps', 'tips', 'alternatives', 'affected_muscles']
                    if not all(key in exercicio for key in required_keys):
                        raise ValueError(f"[ERROR] Missing required fields in exercise data: {exercicio}")
                    
                    try:
                        item = {
                            "PK": {'S': f"USER#{user_id}"},
                            "SK": {'S': f"Treino#{dia_treino}#Exercicio#{exercicio['name']}"},
                            "MuscleGroups": {'S': exercicio['muscle_groups']},
                            "Sets": {'N': str(int(exercicio['sets']))},
                            "Reps": {'S': str(int(exercicio['reps']))},
                            "Tips": {'S': exercicio['tips']},
                            "Alternatives": {'S': json.dumps(exercicio['alternatives'], ensure_ascii=False)},
                            "AffectedMuscles": {'S': json.dumps(exercicio['affected_muscles'], ensure_ascii=False)},
                            "created_at": {'S': self.created_at}
                        }
                        workout_items.append(item)
                    except (TypeError, ValueError) as parse_err:
                        print(f"[ERROR] Parsing exercise data: {parse_err}")
                        continue
            
            return workout_items
        except Exception as err:
            print(f"[ERROR] _create_workout_plans: {err}")
            return None
    
    def create_record(self, record_type):
        record_map = {
            'workout_create_status': self._workout_create_status,
            'workout_plans': self._create_workout_plans,
        }
        
        if record_type not in record_map:
            print(f"[ERROR] Invalid record_type: {record_type}")
            return None
        
        try:
            return record_map[record_type]()
        except Exception as e:
            print(f"[ERROR] Error creating {record_type}: {e}")
            return None
