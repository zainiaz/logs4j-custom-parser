import json

def dictionaries_to_json(indexes, summaries):
    json_object = {}
    
    json_object['summaries'] = summaries
    json_object['indexes'] = indexes
    
    return json.dumps(json_object, indent=4)