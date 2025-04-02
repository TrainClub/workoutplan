class DataProcessor:
    def __init__(self, event, workout_event=None):
        self.event = event or {}
        self.workout_event = workout_event or {}
        self.created_at = datetime.utcnow().isoformat()
        self.user_data = self.event.get('new_member', {}).get('user_data', {})
        self.user_id = self.user_data.get('user_id')

    def _format_map(self, data):
        """Converte um dicionário para o formato do DynamoDB."""
        if not isinstance(data, dict):
            raise ValueError("Invalid data format, expected dict")
        
        formatted = {}
        for key, value in data.items():
            if isinstance(value, str):
                formatted[key] = {'S': value}
            elif isinstance(value, int) or isinstance(value, float):
                formatted[key] = {'N': str(value)}
            elif isinstance(value, dict):
                formatted[key] = {'M': self._format_map(value)}
            elif isinstance(value, list):
                formatted[key] = {'L': [{'M': self._format_map(item)} for item in value]}
            else:
                raise ValueError(f"Unsupported data type: {type(value)} for key {key}")
        
        return formatted

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
            
            user_id = self._get_user_id()
            if not user_id:
                raise ValueError("[ERROR] User ID is None")
            
            workout_plan = self.workout_event
            workout_items = []

            for day, dia_treino in workout_plan.items():
                if not dia_treino:
                    raise ValueError("[ERROR] Missing workout plan data for a day")
                
                try:
                    item = {
                        "PK": {'S': f"USER#{user_id}"},
                        "SK": {'S': f"Treino#{day}"},
                        "Foco": {'S': dia_treino['Foco']},
                        "Aquecimento": {'M': self._format_map(dia_treino['Aquecimento'])},
                        "Exercícios": {'L': [
                            {'M': self._format_map(ex)} for ex in dia_treino['Exercícios']
                        ]},
                        "Core": {'L': [
                            {'M': self._format_map(ex)} for ex in dia_treino['Core']
                        ]},
                        "Cardio": {'M': self._format_map(dia_treino['Cardio'])},
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
