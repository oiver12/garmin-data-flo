from pathlib import Path
import json
def parse():
    bodyweight = 70000
    
    rename_dict = get_renamings()
    settings = get_settings()
    exercises = {}
    base_dir = Path(__file__).parent.parent / "data" / "jsons"
    print(f"Parsing JSON files in {base_dir}...")
    for file in base_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sset in data["exerciseSets"]:
                if sset["setType"] == "REST":
                    continue
                exercise_name = sset["exercises"][0]["name"]
                if sset["exercises"][0]["name"] is None:
                    exercise_name = sset["exercises"][0]["category"]
                if exercise_name in rename_dict.keys():
                    exercise_name = rename_dict[exercise_name]
                if sset["weight"] is None:
                    sset["weight"] = 0
                if settings["include_bw"] and exercise_name == "PULL_UP":
                    sset["weight"] += bodyweight
                date = sset["startTime"][:10]
                if exercise_name not in exercises:
                    exercises[exercise_name] = {
                        "analytics": {
                            "statistics": {
                                "rep_max": [[0, ""] for _ in range(12)]
                            },
                            "session_metrics": {

                            }

                        },
                        "sessions": {}
                    }
                if date not in exercises[exercise_name]["sessions"].keys():
                    exercises[exercise_name]["sessions"][date] = []
                    exercises[exercise_name]["analytics"]["session_metrics"][date] = {
                        "estimated_1rm": 0,
                        "estimated_5rm": 0,
                    }
                
                exercises[exercise_name]["sessions"][date].append({
                    "activityId": data["activityId"],
                    "ssetID": sset["messageIndex"],
                    "reps": sset["repetitionCount"],
                    "weight": sset["weight"],
                    "date": date,
                })

                curr_session_metrics = exercises[exercise_name]["analytics"]["session_metrics"][date]
                estimated_1rm = calculate1rm(sset["weight"], sset["repetitionCount"])
                if estimated_1rm > curr_session_metrics["estimated_1rm"]:
                    curr_session_metrics["estimated_1rm"] = estimated_1rm
                    curr_session_metrics["estimated_5rm"] = calculate5rm(sset["weight"], sset["repetitionCount"])

                rep_max = exercises[exercise_name]["analytics"]["statistics"]["rep_max"]

                if sset["weight"] is not None and sset["weight"] > rep_max[min(11, sset["repetitionCount"] - 1)][0]:
                    
                    rep_max[min(11, sset["repetitionCount"] - 1)] = [sset["weight"], date, sset["repetitionCount"] < 13]
                    for rep in range(min(10, sset["repetitionCount"] - 2), -1, -1):
                        if sset["weight"] > rep_max[rep][0]:
                            rep_max[rep] = [sset["weight"], date, False]
                        else:
                            break
 
    for exercise_name in exercises:
        exercises[exercise_name]["sessions"] = dict(sorted(exercises[exercise_name]["sessions"].items()))
    # Sort exercises my number of sets
    exercises = dict(sorted(exercises.items(), key=lambda x: sum(len(s) for s in x[1]["sessions"].values()), reverse=True))

    output_dir = Path(__file__).parent.parent / "data" / "exercise_json"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "parsed_exercises.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exercises, f, indent=2)

def get_renamings():
    renaming_path = Path(__file__).parent.parent / "settings" / "grouped_exercises.json"
    with open(renaming_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_settings():
    settings_path = Path(__file__).parent.parent / "settings" / "settings.json"
    with open(settings_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate1rm(weight, reps):
    # Using standard bryzki formula:
    return weight * (1.0 / (1.0278 - 0.0278 * reps))

def calculate5rm(weight, reps):
    # Using standard bryzki formula:

    return calculate1rm(weight, reps) * (1.0 - 0.0278 * 4)
