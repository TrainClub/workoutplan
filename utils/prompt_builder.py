import json, os

def createprompt(body:json):
    user_data = body.get("new_member", {})
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.abspath(os.path.join(base_dir, "..", "templates", "prompt.txt"))

    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
        file.close()

    personal_data = user_data.get("personal_data", {})
    user_purpose = user_data.get("user_purpose", {})
    training_preferences = user_data.get("training_preferences", {})
    health_conditions = user_data.get("health_conditions", {})
    affected_areas = user_data.get("affected_areas", {})

    prompt = prompt.replace("{weight}", personal_data.get("weight", "Not provided"))
    prompt = prompt.replace("{height}", personal_data.get("height", "Not provided"))
    prompt = prompt.replace("{main_objective}", user_purpose.get("main_objective", "Not provided"))
    prompt = prompt.replace("{secondary_objective}", user_purpose.get("secondary_objective", "Not provided"))
    prompt = prompt.replace("{experience_level}", training_preferences.get("experience_level", "Not provided"))
    prompt = prompt.replace("{training_frequency_per_week}", str(training_preferences.get("training_frequency_per_week", "Not provided")))
    prompt = prompt.replace("{pre_diabetes}", str(health_conditions.get("pre_diabetes", "Not provided")))
    prompt = prompt.replace("{high_cholesterol}",str( health_conditions.get("high_cholesterol", "Not provided")))
    prompt = prompt.replace("{spinal_disorder}", str(health_conditions.get("spinal_disorder", "Not provided")))
    prompt = prompt.replace("{hypertension}", str(health_conditions.get("hypertension", "Not provided")))
    prompt = prompt.replace("{dizziness_or_fainting}", str(health_conditions.get("dizziness_or_fainting", "Not provided")))
    prompt = prompt.replace("{other_health_issues}", str(health_conditions.get("other_health_issues", "None")))
    prompt = prompt.replace("{knee}", str(affected_areas.get("knee", "Not provided")))
    prompt = prompt.replace("{shoulder}", str(affected_areas.get("shoulder", "Not provided")))
    prompt = prompt.replace("{elbow}", str(affected_areas.get("elbow", "Not provided")))
    prompt = prompt.replace("{spine}", str(affected_areas.get("spine", "Not provided")))
    prompt = prompt.replace("{lower_back}", str(affected_areas.get("lower_back", "Not provided")))

    return prompt